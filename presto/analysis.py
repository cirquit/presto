import pathlib
import pandas as pd
import numpy as np
import tensorflow as tf
from typing import Optional

def strat_analysis_from_csv(path_to_cum_df: str
                          , path_to_cum_dstat_df: str):
        '''Helper to create a StrategyAnalysis object from the csv's saved 
        :param path_to_cum_df: str - path to the csv file
        :param path_to_cum_dstat_df: str - path to the csv file
        :return StrategyAnalysis:
        '''

        cum_df_dtypes ={ 
            "offline_processing_and_save_time_s": np.float32
          , "shard_count": np.int32
          , "thread_count": np.int32
          , "shard_cum_size_MB": np.float32
          , "sample_count": np.int32
          , "online_processing_time_s": np.float32
          , "throughput_sps": np.float32
          , "runs_count": np.int32
          , "runs_total": np.int32
          , "ueid": str
          , "split_name": str
          , "creation_timestamp": str
          , "compression_type": str
          , "storage_type": str
        }

        cum_dstat_df_dtypes = {
            "rel_time_s": np.float32
          , "disk_read_mbs": np.float32
          , "disk_write_mbs": np.float32
          , "net_read_mbs": np.float32
          , "net_write_mbs": np.float32
          , "run": np.int32
          , "sample_count": np.int32
          , "shard_count": np.int32
          , "thread_count": np.int32
          , "ueid": str
          , "split_name": str
          , "creation_timestamp": str
          , "cpu_usr_in_percent": np.float32
          , "cpu_sys_in_percent": np.float32
          , "cpu_idle_in_percent": np.float32
          , "cpu_wait_in_percent": np.float32
          , "system_interrupts_per_s": np.float32
          , "system_context_switches_per_s": np.float32
          , "memory_free_mb": np.float32
          , "memory_buffered_mb": np.float32
          , "memory_used_mb": np.float32
          , "memory_cached_mb": np.float32
          , "vm_major_pagefaults": np.float32
          , "vm_minor_pagefaults": np.float32
          , "vm_allocated_mb": np.float32
          , "vm_free_mb": np.float32
          , "filesystem_files": np.float32
          , "filesystem_inodes": np.float32
          , "filelocks_posix": np.float32
          , "filelocks_lock": np.float32
          , "filelocks_read": np.float32
          , "filelocks_write": np.float32
          , "compression_type": str
          , "storage_type": str
        }


        cum_df = pd.read_csv(path_to_cum_df, dtype=cum_df_dtypes)
        cum_dstat_df = pd.read_csv(path_to_cum_dstat_df, dtype=cum_dstat_df_dtypes) 
        return StrategyAnalysis(strategy_dataframes = []
                                     , dstat_dataframes = []
                                     , cum_df = cum_df
                                     , cum_dstat_df = cum_dstat_df)

class StrategyAnalysis:
    '''Used the analyse multiple logs from different Strategy strategies.
    Takes their dataframes as input. Can save them to disk as well as load em back with the helper function `strat_analysis_from_csv`
    '''

    def __init__(self
              , strategy_dataframes: [pd.DataFrame]
              , dstat_dataframes: [pd.DataFrame]
              , cum_df: Optional[pd.DataFrame] = None
              , cum_dstat_df: Optional[pd.DataFrame] = None):
        '''
        :param strategy_dataframes: list(pd.DataFrames)
        :param dstat_dataframes: list(pd.DataFrames)
        :param cum_df: Optional[pd.DataFrame] = None - to load already summarized dataframes
        :param cum_dstat_df: Optional[pd.DataFrame] = None - to load already summarized dataframes
        '''
        self._preprocessing_time_key     = "preprocessing_time_s"
        self._online_processing_time_key = "per_epoch_processing_time_s"
        self._storage_consumption_key    = "storage_consumption_mb"
        self._throughput_key             = "throughput_sps"
        self._strategy_name_key          = "strategy"
        self._threads_key                = "threads"
        self._sample_count_key           = "sample_count"

        self._strategy_dataframes = strategy_dataframes
        self._dstat_dataframes = dstat_dataframes
        self._average_sample_size_KB = 0

        if isinstance(cum_df, pd.DataFrame):
            self._cum_df = cum_df
        else:
            self._cum_df = self.to_cum_df()
        if isinstance(cum_dstat_df, pd.DataFrame):
            self._cum_dstat_df = cum_dstat_df
        else:
            self._cum_dstat_df = self.to_cum_dstat_df()

        self._dataframe_creation_timestamp = self._get_df_creation_timestamp()


    def _get_file_size_KB(self, filepath):
        '''
        :param filepath: (str)
        :return: (float) - size in KiloByte of the file
        '''
        return pathlib.Path(filepath).stat().st_size / 1000

    def _get_df_creation_timestamp(self):
        '''Returns the timestamp from the first indexed strategy dataframe row
        :return: str
        '''
        return self._cum_df["creation_timestamp"][0]

    def to_cum_df(self):
        '''Return the cumulative dataframe of common meta data of all strategies
        :return: pd.DataFrame
        '''
        if len(self._strategy_dataframes) == 0:
            return self._cum_df
        else:
            return pd.concat(self._strategy_dataframes, ignore_index=True)

    def to_cum_dstat_df(self):
        '''Return the cumulative dstat dataframe of all strategies
        :return: pd.DataFrames
        '''
        if len(self._dstat_dataframes) == 0:
            return self._cum_dstat_df
        else:
            return pd.concat(self._dstat_dataframes, ignore_index=True)

    def save_dfs_as_csv(self
                      , path: str
                      , prefix: Optional[str] = None):
        '''Saves both cum_df and cum_dstat_df as csvs
        :param path: str - path where to save the dataframes to ('/' is added automatically)
        :param prefix: Optional[str] - optional prefix string added to the front of the file
        '''

        cum_df = self.to_cum_df()
        cum_dstat_df = self.to_cum_dstat_df()

        small_sep = "-"
        big_sep = "_"

        cum_df_text = [self._dataframe_creation_timestamp, "cum-df"]
        cum_dstat_df_text = [self._dataframe_creation_timestamp, "cum-dstat-df"]

        def samples_text():
            text = ["samples"] + [str(sample_count) for sample_count in cum_df.sample_count.unique()]
            return small_sep.join(text)

        def threads_text():
            text = ["threads"] + [str(sample_count) for sample_count in cum_df.thread_count.unique()]
            return small_sep.join(text)

        cum_df_text += [samples_text(), threads_text()]
        cum_dstat_df_text += [samples_text(), threads_text()]
        if prefix != None:
            cum_df_text = [prefix] + cum_df_text
            cum_dstat_df_text = [prefix] + cum_dstat_df_text

        full_cum_df_filename = big_sep.join(cum_df_text) + ".csv"
        full_cum_dstat_df_filename = big_sep.join(cum_dstat_df_text) + ".csv"

        cum_df_path = pathlib.Path(path) / full_cum_df_filename
        cum_dstat_df_path = pathlib.Path(path) / full_cum_dstat_df_filename

        cum_df.to_csv(cum_df_path, index=False)
        cum_dstat_df.to_csv(cum_dstat_df_path, index=False)

    def calculate_avg_sample_size_KB(self
                                   , loading_pipeline: tf.data.Dataset
                                   , sample_count: Optional[int] = None):
        '''Only calculated once and saved in the member _average_sample_size_KB
        :param loading_pipeline: (tf.data.DataSet) - returns the paths to the samples
        :param sample_count: (Optional[int]) - how many samples are consumed from this dataset. If None, iterating through all
        :return: (float) - size of the average sample size in KB
        '''

        if self._average_sample_size_KB == 0:

            if sample_count == None:
                files = loading_pipeline
            else:
                files = loading_pipeline.take(sample_count)

            total_size_KB = 0

            for file_counter, file in enumerate(files):
                filepath = str(file.numpy().decode())
                total_size_KB += self._get_file_size_KB(filepath = filepath)
            print(f"{total_size_KB / 1000**2}")
            if sample_count == None:
                sample_count = file_counter + 1

            self._average_sample_size_KB = total_size_KB / float(sample_count)

        return self._average_sample_size_KB

    def extrapolate_by_size(self
                          , total_dataset_size_GB: float
                          , average_sample_size_KB: float):
        '''Extrapolate the profiling dataframe by the full dataset size

        !!! PREMISE !!! - we assume that the samples are representative of the whole dataset. Evaluated for the Imagenet dataset, but may not be true for others
        
        :param total_dataset_size_GB: (float) - check the original dataset size from paper 
        :param average_sample_size: (float) - calculate that with `self.calculate_avg_sample_size`
        :return: pd.DataFrame
        '''

        extrapolated_cols = [ "offline_processing_and_save_time_s"
                            , "offline_save_time_s"
                            , "shard_cum_size_MB"
                            , "online_processing_time_s"]

        full_pd_extra = self._cum_df.copy(deep = True)


        print(f"{total_dataset_size_GB}GB")
        total_dataset_size_KB      = total_dataset_size_GB * 1000**2
        print(f"{total_dataset_size_KB}KB")
        total_dataset_sample_count = total_dataset_size_KB / average_sample_size_KB 
        print(f"{total_dataset_sample_count} total dataset sample count")
        sample_count               = self._cum_df["sample_count"][0]
        print(f"{sample_count} sample count")
        # extrapolation factor is multiplied, e.g sps = 4.5, 10 samples, 100 total -> sps * (100 / 10) = 45
        extrapolation_factor       = total_dataset_sample_count / sample_count
        print(f"{extrapolation_factor} extrapolation factor")

        for col in self._cum_df.columns:
            if col in extrapolated_cols:
                full_pd_extra[col] = full_pd_extra[col] * extrapolation_factor

        return full_pd_extra

    def summary(self):
        '''Returns a dataframe with 4 columns:
        * preprocessing_time - (mean) in sec
        * storage_consumption - (mean) in MB
        * throughput - (mean) in samples per second
        * strategy - names of the steps
        :return: pd.DataFrame
        '''

        summarized_dict = dict()

        summarized_dict[self._preprocessing_time_key]        = []
        summarized_dict[self._storage_consumption_key]       = []
        summarized_dict[self._throughput_key]                = []
        summarized_dict[self._online_processing_time_key]    = []
        summarized_dict[self._strategy_name_key]             = []
        summarized_dict[self._threads_key]                   = []
        summarized_dict[self._sample_count_key]              = []

        cum_df = self._cum_df

        def avg(df, key):
            return df.describe()[key][1]

        for split_name in cum_df.split_name.unique():

            for threads in cum_df.thread_count.unique():

                for sample_count in cum_df.sample_count.unique():

                    preprocessing_time = avg(df  = cum_df.query(f"split_name=='{split_name}' and thread_count=='{threads}' and sample_count=='{sample_count}'")
                                           , key = "offline_processing_and_save_time_s")
                    summarized_dict[self._preprocessing_time_key].append(preprocessing_time)

                    online_processing_time = avg(df  = cum_df.query(f"split_name=='{split_name}' and thread_count=='{threads}' and sample_count=='{sample_count}'")
                                           , key = "online_processing_time_s")
                    summarized_dict[self._online_processing_time_key].append(online_processing_time)

                    storage_consumption = avg(df  = cum_df.query(f"split_name=='{split_name}' and thread_count=='{threads}' and sample_count=='{sample_count}'")
                                            , key = "shard_cum_size_MB")
                    summarized_dict[self._storage_consumption_key].append(storage_consumption)

                    throughput = avg(df  = cum_df.query(f"split_name=='{split_name}' and thread_count=='{threads}' and sample_count=='{sample_count}'")
                                                      , key = "throughput_sps")
                    summarized_dict[self._throughput_key].append(throughput)

                    summarized_dict[self._strategy_name_key].append(split_name)

                    summarized_dict[self._threads_key].append(threads)

                    summarized_dict[self._sample_count_key].append(sample_count)

        return pd.DataFrame(summarized_dict)


    def normalized_summary(self
                         , summarized_df: Optional[pd.DataFrame] = None):
        '''Returns a dataframe with 4 columns:
        * preprocessing_time - (mean) 0-1 normalized, higher is faster
        * storage_consumption - (mean) 0-1 normalized, higher is **smaller**
        * throughput - (mean) 0-1 normalized, higher is faster
        * strategy - names of the steps
        :summarized_df: Optional[pd.DataFrame] - will call self.summary() if None
        :return: pd.DataFrame
        '''

        if summarized_df == None:
            summarized_df = self.summary()

        def normalize(row):
            return (row - row.min()) / (row.max() - row.min())

        def inv_normalize(row):
            return 1 - normalize(row)

        summarized_df[self._preprocessing_time_key]  = inv_normalize(summarized_df[self._preprocessing_time_key])
        summarized_df[self._storage_consumption_key] = inv_normalize(summarized_df[self._storage_consumption_key])
        summarized_df[self._throughput_key]          = normalize(summarized_df[self._throughput_key])

        return summarized_df


    def weighted_summary(self
                       , preprocessing_time_weight: float
                       , storage_consumption_weight: float
                       , throughput_weight: float
                       , normalized_df: Optional[pd.DataFrame] = None):
        '''Return the ranked strategies
        :return: pd.DataFrame
        '''

        ranked_strategies = dict()
        ranked_strategies["strategy"] = []
        ranked_strategies["score"]    = []

        if normalized_df == None:
            normalized_df = self.normalized_summary()

        for strategy in normalized_df[self._strategy_name_key].unique():
            for threads in normalized_df[self._threads_key].unique():
                for sample_count in normalized_df[self._sample_count_key].unique():

                    full_strategy_name = strategy + f"-threads-{threads}-samples-{sample_count}"
                    ranked_strategies["strategy"].append(full_strategy_name)

                    preprocessing_time_score = preprocessing_time_weight * \
                                                normalized_df.query(f"{self._strategy_name_key}=='{strategy}' and {self._threads_key}=='{threads}' and {self._sample_count_key}=='{sample_count}'") \
                                                    .reset_index(drop=True)[self._preprocessing_time_key][0]
                                         
                    storage_consumption_score = storage_consumption_weight * \
                                                 normalized_df.query(f"{self._strategy_name_key}=='{strategy}' and {self._threads_key}=='{threads}' and {self._sample_count_key}=='{sample_count}'") \
                                                    .reset_index(drop=True)[self._storage_consumption_key][0]

                    throughput_score = throughput_weight * \
                                        normalized_df.query(f"{self._strategy_name_key}=='{strategy}' and {self._threads_key}=='{threads}' and {self._sample_count_key}=='{sample_count}'") \
                                            .reset_index(drop=True)[self._throughput_key][0]

                    score = preprocessing_time_score + storage_consumption_score + throughput_score
                    ranked_strategies["score"].append(score)

        ranked_df = pd.DataFrame(ranked_strategies)

        return ranked_df.sort_values(by="score")

    def extended_summary(self):
        '''Returns a dataframe with 4 columns:
        * preprocessing_time - (mean) in sec
        * storage_consumption - (mean) in MB
        * throughput - (mean) in samples per second
        * strategy - names of the steps
        :return: pd.DataFrame
        '''

        extended_summary_dict = dict()

        extended_summary_dict[self._preprocessing_time_key]  = []
        extended_summary_dict[self._storage_consumption_key] = []
        extended_summary_dict[self._throughput_key]          = []
        extended_summary_dict[self._strategy_name_key]       = []
        extended_summary_dict[self._threads_key]             = []
        extended_summary_dict[self._sample_count_key]        = []

        cum_df = self._cum_df

        def avg(df, key):
            return df.describe()[key][1]

        for split_name in cum_df.split_name.unique():

            for threads in cum_df.thread_count.unique():

                for sample_count in cum_df.sample_count.unique():

                    preprocessing_time = avg(df  = cum_df.query(f"split_name=='{split_name}' and thread_count=='{threads}' and sample_count=='{sample_count}'")
                                           , key = "offline_processing_and_save_time_s")
                    summarized_dict[self._preprocessing_time_key].append(preprocessing_time)

                    storage_consumption = avg(df  = cum_df.query(f"split_name=='{split_name}' and thread_count=='{threads}' and sample_count=='{sample_count}'")
                                            , key = "shard_cum_size_MB")
                    summarized_dict[self._storage_consumption_key].append(storage_consumption)

                    throughput = avg(df  = cum_df.query(f"split_name=='{split_name}' and thread_count=='{threads}' and sample_count=='{sample_count}'")
                                                      , key = "throughput_sps")
                    summarized_dict[self._throughput_key].append(throughput)

                    summarized_dict[self._strategy_name_key].append(split_name)

                    summarized_dict[self._threads_key].append(threads)

                    summarized_dict[self._sample_count_key].append(sample_count)

        return pd.DataFrame(summarized_dict)
        
