import os
import re
import sys
import time
import uuid
import copy
import glob
import pathlib
import numpy as np
import pandas as pd
import tensorflow as tf

from typing import Optional
from datetime import datetime

from presto import pipeline as pipeline_helper
from presto.profile import run_profiled, drop_io_cache
 
class Strategy:
    '''Strategy class that splits a pipeline into an *offline** and **online** part
    Can execute both the parts of the pipeline and profile each while logging stats like:
    * cumulative shard size
    * online processing time
    * offline processing time
    * throughput (samples/s)

    The logs are can be loaded by `profile_as_df()` and `profile_dstat_as_df()`.
    For a summary of different strategy dataframes, please use the class `StrategyAnalysis`
    '''
    def __init__(self
               , pipeline
               , split_position: Optional[int] = None
               , shard_count: int = 1
               , thread_count: int = 1
               , shard_directory_prefix: str = "./shards"
               , compression_type: str = "none"
               , storage_type: str = "local-ssd"):
        '''
        :param pipeline: dict of a pipeline see imagenet_pipeline.py in the `/examples`
        :param split_position: Optional[int], index of position BEFORE the split will be inserted. If not provided, no split is made and it defaults to preprocess everything **online**
        :param shard_count: int, how many files does this **offline** parts has to be saved in 
        :param thread_count: int, how many threads operate on all the tf.Dataset ops
        :param shard_directory_prefix: str (default = "./shards"), directory where to save the temporary shards
        :param compression_type: str (default = ""), compression type for the intermediate representations (offline only). Possible parameters: ZLIB, GZIP, or "" for no compression
        :param storage_type: str (default = "local-ssd"), just using this parameter to add it to the dataframes for future parsing. Makes no difference in the execution
        '''

        self._validated_compression_or_exit(compression_type)

        self._split_pipeline(pipeline, split_position)
        self._split_position = split_position
        self._shard_count = shard_count
        self._thread_count = thread_count
        self._ueid = self._get_ueid()
        self._creation_timestamp = self._get_timestamp()
        self._compression_type = "" if not compression_type in ["ZLIB", "GZIP"] else compression_type
        self._storage_type = storage_type
        self._shard_directory = shard_directory_prefix + "_" + \
                                self._creation_timestamp + "_" + \
                                self._get_last_strategy_step_name() + "_" + \
                                self._get_shard_infix() + "_" + \
                                self._get_thread_count_infix() + "_" + \
                                self._ueid + "/"
        self.meta_info = {
            "offline_processing_and_save_time_s": []
          , "shard_count": self._shard_count
          , "thread_count": self._thread_count
          , "shard_cum_size_MB": []
          , "sample_count": []
          , "online_processing_time_s": []
          , "throughput_sps": []
          , "runs_count": []
          , "runs_total": 0
          , "ueid": self._ueid
          , "split_name": self._get_last_strategy_step_name()
          , "creation_timestamp": self._creation_timestamp
          , "compression_type": self._get_compression_type_for_dataframe()
          , "storage_type": self._storage_type
          , "application_cache_enabled": False
          , "system_cache_enabled": False
          , "batch_count": None
          , "prefetch_count": None
        }

    def _set_application_cache_flag(self, value):
        '''Sets the flag in the meta dict for export
        '''
        self.meta_info["application_cache_enabled"] = value

    def _set_system_cache_flag(self, value):
        '''Sets the flag in the meta dict for export
        '''
        self.meta_info["system_cache_enabled"] = value

    def _set_batch_count_flag(self, value):
        '''Sets the flag in the meta dict for export
        '''
        self.meta_info["batch_count"] = value

    def _set_prefetch_count_flag(self, value):
        '''Sets the flag in the meta dict for export
        '''
        self.meta_info["prefetch_count"] = value

    def _validated_compression_or_exit(self, compression_type):
        '''Checks for 
        :param compression_type: str
        '''
        if not compression_type in ["none","GZIP","ZLIB"]:
            print("compression_type is not known, please pick one of the following: 'none', 'GZIP', 'ZLIB'")
            sys.exit(0)
    
    def _get_compression_type_for_dataframe(self):
        '''Changing the empty string, which stands for no compression in tensorflow.data to "none"
        :return: str (none, ZLIB, GZIP)
        '''
        if self._compression_type == "":
            return "none"
        else:
            return self._compression_type


    def _split_pipeline(self
                      , pipeline
                      , split_position):
        '''Splits the pipeline and saves the **offline** and **online** part in private members
        :param split_position: Optional[int] - if None, everything is processed **online**
        '''

        if split_position == None:
            self._offline_pipeline = []
            self._online_pipeline  = pipeline
        else:
            offline_pipeline, online_pipeline = pipeline_helper.serialized_split(pipeline, split_position)
            self._offline_pipeline = offline_pipeline
            self._online_pipeline  = online_pipeline
    
    def _get_timestamp(self):
        '''Returns a timestamp formatted in a way that respects the naive ordering of the shell and sorts experiments by time
        :return: str
        '''
        now = datetime.now()
        timestamp_format = "%Y-%m-%d-%H:%M:%S"
        return now.strftime(timestamp_format)

    def _get_ueid(self):
        '''Returns a md5-like hash with 6 characters for the (U)nique (E)xperiment (I)(D)
        :return: str
        '''
        return uuid.uuid4().hex[:6]

    def _get_last_strategy_step_name(self):
        '''Returns the name of the last step that is materialized based on the `self._offline_pipeline`**
        Replaces whitespace with `-` and returns lowercase letters

        :return: str
        '''

        if self._split_position == None:
            return "0-fully-online"
        else:
            # get last step before serialization
            last_materialized_step_name = str(self._split_position) + "-" + self._offline_pipeline[-2]["name"]
            return last_materialized_step_name.replace(' ', '-').lower()

    def _get_shard_infix(self):
        '''Returns the shard infix for the shard directory
        :return: str
        '''
        return "shards-" + str(self._shard_count)

    def _get_thread_count_infix(self):
        '''Returns the shard infix for the shard directory
        :return: str
        '''
        return "threads-" + str(self._thread_count)

    def _delete_temp_files(self):
        '''Deletes the temporary files in the `self._shard_directory` which are matching "*.tfrecord"
        '''
        temp_files = [pathlib.Path(filepath) for filepath in glob.glob(self._shard_directory + "*.tfrecord")]
        for file in temp_files:
            file.unlink()

    def _increment_run_counter(self):
        '''Increments the run counter in the meta_info dict in a way so that the resulting pandas dataframe works correctly
        '''
        runs_count = self.meta_info["runs_count"]
        if runs_count == []:
            self.meta_info["runs_count"].append(0)
        else:
            new_run_counter = runs_count[-1] + 1
            self.meta_info["runs_count"].append(new_run_counter)

        self.meta_info["runs_total"] = len(self.meta_info["runs_count"])

    def execute_offline_pipeline(self
                               , sample_count: int):
        '''Runs the offline part of the pipeline and saves it as as `.tfrecord` files
        
        :param sample_count (int): datasamples count
        '''

        start = time.time()
        offline_dataset = pipeline_helper.build_pipeline(self._offline_pipeline, compressed_parallelism=self._thread_count) \
                                         .take(sample_count)
                                         # .apply(tf.data.experimental.ignore_errors()) \

        pipeline_helper.save_ds_parallel(
            dataset=offline_dataset
          , shard_count=self._shard_count
          , shard_directory=self._shard_directory
          , compression_type=self._compression_type)
        end = time.time()
        self.meta_info["offline_processing_and_save_time_s"].append(end - start)
        
        shard_sizes_b = [pathlib.Path(fp).stat().st_size for fp in glob.glob(self._shard_directory + "*.tfrecord")]
        self.meta_info["shard_cum_size_MB"].append(np.sum(shard_sizes_b) / 1000**2)


    def create_online_pipeline(self):
        '''Creates the online part of the pipeline that returns a tf.Dataset
        Datasat is lazily created, you need to `.take(n)` from it when using the data for training

        :param parallel_reads: (int) amount of thread_count given to tf.data.TFRecordDataset
        :return: tf.Dataset
        '''

        online_pipeline = copy.copy(self._online_pipeline)

        # if the pipeline is split, insert the loading of tfrecords step
        if self._split_position != None:
            online_pipeline.insert(0, {
                "name": "load TFRecord shards",
                "type": "op",
                "op": tf.data.TFRecordDataset(
                    tf.data.Dataset.list_files(self._shard_directory + "*.tfrecord"
                                             , seed = 42)
                  , num_parallel_reads=self._thread_count
                  , compression_type=self._compression_type
                ),
                "output_schema": online_pipeline[0]["input_schema"]
            })

        online_dataset = pipeline_helper.build_pipeline(online_pipeline, compressed_parallelism=self._thread_count)

        return online_dataset


    def execute_full_pipeline(self
                            , run_id: int
                            , sample_count: int
                            , runs_total: int
                            , batch_count: int = None
                            , prefetch_count: int = None
                            , system_cache_enabled: bool = False
                            , application_cache_enabled: bool = False):
        '''Executes both pipelines and simulates the "processing" by a sink with a for loop that checks the shape of each sample

        :param run_id: (int)
        :param sample_count: (int)
        :param runs_total: (int)
        :param batch_count: (int) - if none, no custom loop to iterate over batches
        :param prefetch_count: (int) - how many batches to prefetch
        :param application_cache_enabled: (bool) - run twice and only count the application cache time? 
        :returns: tf.data.Dataset - already evaluated with `.take(sample_count)`
        '''

        self._increment_run_counter()

        # do we want to test system cache?
        if system_cache_enabled:
            # if we run for the first time, we need to create the dataset
            if run_id < 1:
                # if we have offline steps
                if self._split_position != None:
                    self.execute_offline_pipeline(sample_count)
                # if we run online online
                else:
                    # create directory as the shard creating part of the offline pipeline wont for the logs
                    pathlib.Path(self._shard_directory).mkdir(exist_ok = True, parents = True)
                    self.meta_info["offline_processing_and_save_time_s"].append(0)
                    self.meta_info["shard_cum_size_MB"].append(0)
            # for runs=1+, we only read the files from memory, no need for preprocessing
            else:
                self.meta_info["offline_processing_and_save_time_s"].append(0)
                self.meta_info["shard_cum_size_MB"].append(0)
        # no system caching test? run normally each run
        else:
            # do we have offline steps?
            if self._split_position != None:
                self.execute_offline_pipeline(sample_count)
            # if we don't, create dir + logs
            else:
                # create directory as the shard creating part of the offline pipeline wont for the logs
                pathlib.Path(self._shard_directory).mkdir(exist_ok = True, parents = True)
                self.meta_info["offline_processing_and_save_time_s"].append(0)
                self.meta_info["shard_cum_size_MB"].append(0)

        # testing system level caching?
        if system_cache_enabled:
            # drop only at the first run, then never again
            if run_id < 1:
                # its necessary to drop the cache here to simulate that the offline processing was done "offline", and we *need* to read from disk
                drop_io_cache(page_cache=True, dentries_and_inodes=True)
        # not testing system caching? drop every run
        else:
            # its necessary to drop the cache here to simulate that the offline processing was done "offline", and we *need* to read from disk
            drop_io_cache(page_cache=True, dentries_and_inodes=True)

        start = time.time()
        ds = self.create_online_pipeline().take(sample_count)
        if batch_count != None and prefetch_count != None:
            ds = ds.batch(batch_count).prefetch(prefetch_count)
        elif batch_count != None and prefetch_count == None:
            ds = ds.batch(batch_count)
        else: # batch_count == None and prefetch_count == None
            ds = ds

        # if we enable application cache, we need to iterate twice in one run, as we construct the pipeline newly each call
        if application_cache_enabled:
            ds = ds.cache()

        def evaluate_loop():
            # forced evaluation by checking the shape
            x_dimension = 0
            # if batch iteration, need to iterate over the internal batches
            if batch_count != None:
                for i, batch in enumerate(ds):
                    for j, sample in enumerate(batch):
                        if isinstance(sample, tuple):
                            x_dimension += sample[0].shape[0]
                        else:
                            x_dimension += sample.shape[0]
            # if no batch interation, counting samples is enough
            else:
                for j, sample in enumerate(ds):
                    if isinstance(sample, tuple):
                        x_dimension += sample[0].shape[0]
                    else:
                        x_dimension += sample.shape[0]

        # consume the dataset once
        evaluate_loop()
        # if we test application cache, we restart the timer and consume the dataset again
        if application_cache_enabled:
            start = time.time()
            evaluate_loop()

        end = time.time()
        self.meta_info["sample_count"].append(sample_count)
        online_processing_time_s = end - start
        self.meta_info["online_processing_time_s"].append(online_processing_time_s)
        self.meta_info["throughput_sps"].append(sample_count / online_processing_time_s)

        # testing system level caching?
        if system_cache_enabled:
            # is it the last run? delete files, otherwise not
            if (run_id + 1) == runs_total:
                self._delete_temp_files()
        # no testing caching -> delete files every run
        else:
            self._delete_temp_files()

        return ds

    def profile_strategy(self
                       , sample_count: int
                       , runs_total: int
                       , batch_count: int = None
                       , enable_tracing: bool = False
                       , prefetch_count: int = None
                       , system_cache_enabled: bool = False
                       , application_cache_enabled: bool = False):
        '''Runs the strategy multiple times and populates the meta info about the runs in private members
        In parallel at least `dstat` is running and also writes the data to disk. 

        :param sample_count: (int) how many samples are used from the dataset
        :param runs_total: (int) how often is each experiment reproduced
        :param batch_count: (int) how big is the batch size
        '''

        self._set_application_cache_flag(value=application_cache_enabled)
        self._set_system_cache_flag(value=system_cache_enabled)
        self._set_batch_count_flag(value=batch_count)
        self._set_prefetch_count_flag(value=prefetch_count)

        run_profiled(
              runs_total = runs_total
            , results_directory = pathlib.Path(self._shard_directory)
	        , sample_count = sample_count
            , system_cache_enabled = system_cache_enabled
            , enable_tracing = enable_tracing
            , function = self.execute_full_pipeline
            , args = [sample_count, runs_total, batch_count, prefetch_count, system_cache_enabled, application_cache_enabled])

    def print_stats(self):
        '''Simple stdout logger to check the self.meta_info dict
        '''
        print(f"Strategy {self._shard_directory}")
        for k,v in self.meta_info.items():
            if k in ["ueid", "creation_timestamp", "split_name", "compression_type", "storage_type", "system_cache_enabled", "application_cache_enabled", "batch_count", "prefetch_count"]:
                print(f"  - {k} = {v}")
            elif k in ["runs_count", "runs_total"]:
                print(f"  - {k} = {v}")
            else:
                if v == []:
                    print(f"  - {k} = 0 +/- 0")
                else:
                    print(f"  - {k} = {round(np.mean(v), 3)} +/- {round(np.std(v), 2)}")

    def profile_as_df(self):
        '''Converts the meta_info dictionary to a pandas DataFrame
        :return: pd.DataFrame
        '''
        local_profile_df = pd.DataFrame(self.meta_info)
        return local_profile_df

    def profile_as_dstat_df(self):
        '''Converts the logged stats via dstat while doing the profiling to a pandas DataFrame
        :return: pd.DataFrame
        '''
        dstat_filepaths = [fp for fp in glob.glob(self._shard_directory + "dstat_*.csv")]
    
        def get_path_info(filepath: str):
            '''See profile.py for the definition of the destructioning pattern
            '''
            destructioning_pattern = re.compile(r"dstat_run-(?P<run>\d+)_samples-(?P<samples>\d+).csv")
            run_index, sample_count,  = destructioning_pattern.search(filepath).groups()
            return run_index, sample_count

        def prepare_columns(columns):
            '''Some magic for dstat logs
            '''
            last = None
            for (l1, l2) in columns:
                if not l1.startswith("Unnamed"):
                    last = l1
                yield (last, l2)

        def load_dstats_file(csv_path: str):
            '''Loads the multi-column dstats file and adds normalized timesteps
            '''
            df = pd.read_csv(csv_path, header=[4,5])
            
            df.columns = pd.MultiIndex.from_tuples(prepare_columns(df.columns))
            
            df = df.loc[:, ~df.columns.duplicated()]

            # convert to int
            df["epoch", "epoch"] = df["epoch", "epoch"].astype(int)
            # get unique timestamps
            df_unique_epochs = df["epoch", "epoch"].drop_duplicates()
           # no way to remove duplicates in a multi-index pd frame, therefore reusing index to filter
            df = df[df.index.isin(df_unique_epochs.index.to_numpy())]
            # need to create new index now
            df.reindex(range(0, df.shape[0]))
            # add normalized time
            df["t"] = df["epoch", "epoch"]
            df["t"] -= df.t.min()
            
            return df

        dstat_dict = {
            "rel_time_s": []
           ,"disk_read_mbs": []
           ,"disk_write_mbs": []
           ,"net_read_mbs": []
           ,"net_write_mbs": []
           ,"run": []
           ,"sample_count": []
           ,"shard_count": int(self._shard_count)
           ,"thread_count": int(self._thread_count)
           ,"ueid": self._ueid
           ,"split_name": self._get_last_strategy_step_name()
           ,"creation_timestamp": self._creation_timestamp
           ,"cpu_usr_in_percent": []
           ,"cpu_sys_in_percent": []
           ,"cpu_idle_in_percent": []
           ,"cpu_wait_in_percent": []
           ,"system_interrupts_per_s": []
           ,"system_context_switches_per_s": []
           ,"memory_free_mb": []
           ,"memory_buffered_mb": []
           ,"memory_used_mb": []
           ,"memory_cached_mb": []
           ,"vm_major_pagefaults": []
           ,"vm_minor_pagefaults": []
           ,"vm_allocated_mb": []
           ,"vm_free_mb": []
           ,"filesystem_files": []
           ,"filesystem_inodes": []
           ,"filelocks_posix": []
           ,"filelocks_lock": []
           ,"filelocks_read": []
           ,"filelocks_write": []
           ,"compression_type": self._get_compression_type_for_dataframe()
           ,"storage_type": self._storage_type
           ,"application_cache_enabled": self.meta_info["application_cache_enabled"]
           ,"system_cache_enabled": self.meta_info["system_cache_enabled"]
           ,"batch_count": self.meta_info["batch_count"]
           ,"prefetch_count": self.meta_info["prefetch_count"]
          }

        for dstat_fp in dstat_filepaths:

            df = load_dstats_file(dstat_fp)

            for index, row in df.iterrows():

                rel_time_s = row["t"][0]
                disk_read_mbs  = row["dsk/total", "read"] / 1000**2
                disk_write_mbs = row["dsk/total", "writ"] / 1000**2
                net_read_mbs   = row["net/total", "recv"] / 1000**2
                net_write_mbs  = row["net/total", "send"] / 1000**2
                cpu_usr_in_percent = row["total cpu usage", "usr"]
                cpu_sys_in_percent = row["total cpu usage", "sys"]
                cpu_idle_in_percent = row["total cpu usage", "idl"]
                cpu_wait_in_percent = row["total cpu usage", "wai"]
                system_interrupts_per_s = row["system", "int"]
                system_context_switches_per_s = row["system", "csw"]
                memory_free_mb = round(row["memory usage", "free"] / 1000**2, 2)
                memory_buffered_mb = round(row["memory usage", "buff"] / 1000**2, 2)
                memory_used_mb = round(row["memory usage", "used"] / 1000**2, 2)
                memory_cached_mb = round(row["memory usage", "cach"] / 1000**2, 2)
                vm_major_pagefaults = row["virtual memory", "majpf"]
                vm_minor_pagefaults = row["virtual memory", "minpf"]
                vm_allocated_mb = round(row["virtual memory", "alloc"] / 1000**2, 2)
                vm_free_mb = round(row["virtual memory", "free"] / 1000**2, 2)
                filesystem_files = row["filesystem", "files"]
                filesystem_inodes = row["filesystem", "inodes"]
                filelocks_posix = row["file locks", "pos"]
                filelocks_lock = row["file locks", "lck"]
                filelocks_read = row["file locks", "rea"]
                filelocks_write = row["file locks", "wri"]
                
                run, sample_count = get_path_info(dstat_fp)
                
                dstat_dict["rel_time_s"].append(rel_time_s)
                dstat_dict["disk_read_mbs"].append(disk_read_mbs)
                dstat_dict["disk_write_mbs"].append(disk_write_mbs)
                dstat_dict["net_read_mbs"].append(net_read_mbs)
                dstat_dict["net_write_mbs"].append(net_write_mbs)
                dstat_dict["run"].append(run)
                dstat_dict["sample_count"].append(sample_count)
                dstat_dict["cpu_usr_in_percent"].append(cpu_usr_in_percent)
                dstat_dict["cpu_sys_in_percent"].append(cpu_sys_in_percent)
                dstat_dict["cpu_idle_in_percent"].append(cpu_idle_in_percent)
                dstat_dict["cpu_wait_in_percent"].append(cpu_wait_in_percent)
                dstat_dict["system_interrupts_per_s"].append(system_interrupts_per_s)
                dstat_dict["system_context_switches_per_s"].append(system_context_switches_per_s)
                dstat_dict["memory_free_mb"].append(memory_free_mb)
                dstat_dict["memory_buffered_mb"].append(memory_buffered_mb)
                dstat_dict["memory_used_mb"].append(memory_used_mb)
                dstat_dict["memory_cached_mb"].append(memory_cached_mb)
                dstat_dict["vm_major_pagefaults"].append(vm_major_pagefaults)
                dstat_dict["vm_minor_pagefaults"].append(vm_minor_pagefaults)
                dstat_dict["vm_allocated_mb"].append(vm_allocated_mb)
                dstat_dict["vm_free_mb"].append(vm_free_mb)
                dstat_dict["filesystem_files"].append(filesystem_files)
                dstat_dict["filesystem_inodes"].append(filesystem_inodes)
                dstat_dict["filelocks_posix"].append(filelocks_posix)
                dstat_dict["filelocks_lock"].append(filelocks_lock)
                dstat_dict["filelocks_read"].append(filelocks_read)
                dstat_dict["filelocks_write"].append(filelocks_write)
                
        return pd.DataFrame(dstat_dict)
