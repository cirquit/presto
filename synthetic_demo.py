import warnings
warnings.filterwarnings('ignore')
import os
import sys
import time
import numpy as np
import pandas as pd
import seaborn as sns
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
import matplotlib.pylab as plt
from pathlib import Path

from presto          import pipeline
from presto.analysis import StrategyAnalysis
from presto.strategy import Strategy


thread_shard_count = int(sys.argv[1])
sample_count       = int(sys.argv[2])
runs               = int(sys.argv[3])
data_type          = str(sys.argv[4])
shape              = int(sys.argv[5])
pipeline_mod       = str(sys.argv[6])

storage_type = "remote"
target_path = "/tmp"

if data_type == "uint8":
    log_path = "/logs/uint8":
else: # data_type == "float32"
    if pipeline_mod == "read-experiment":
        log_path = "/logs/float32"
    elif pipeline_mod == "sys-caching-read":
        log_path = "/logs/float32/sys-caching"
    elif pipeline_mod == "app-caching-read":
        log_path = "/logs/float32/app-caching"
    elif pipeline_mod == "parallelism":
        log_path = "/logs/float32/parallelism"
    elif pipeline_mod == "tf-computation":
        log_path = "/logs/float32/tensorflow"
    elif pipeline_mod == "np-computation":
        log_path = "/logs/float32/numpy"
    else:
       print(f"Picked impossible setting: data_type={data_type} and pipeline_mod={pipeline_mod}, check synthetic_demo.py for valid combinations")
       sys.exit(0)

# with float32, shape=1 => 0.01MB size
sample_shape = [2500,shape]

if pipeline_mod == "read-experiment" or pipeline_mod == "sys-caching-read" or pipeline_mod == "app-caching-read":
    from synthetic_pipeline_reading import pipeline_definition
    type_pipeline = pipeline_definition(shape=sample_shape
                                      , sample_count=sample_count
                                      , data_type=data_type)
    type_pipeline_steps = list(range(len(type_pipeline)))
    del type_pipeline_steps[0] # no need to profile fully-online with a generated dataset from memory
    del type_pipeline_steps[1] # no need to profile creating the dataset
else: # pipeline_mod == 'tf-computation' or pipeline_mod == 'np-computation'
    from synthetic_pipeline_processing import pipeline_definition
    type_pipeline = pipeline_definition(shape=sample_shape
                                      , sample_count=sample_count
                                      , data_type=data_type
                                      , computation_type=pipeline_mod)
    type_pipeline_steps = list(range(len(type_pipeline)))
    del type_pipeline_steps[0] # no need to profile fully-online with a generated dataset from memory
    del type_pipeline_steps[1] # no need to profile creating the dataset
    del type_pipeline_steps[3] # no need to profile reading fully processed dataset


#del type_pipeline_steps[2] # remote reading startegy, need only processing
#del type_pipeline_steps[0] # remove the 0-fully-online strategy, we only need the read from dataset performance

thread_counts = [thread_shard_count]
shard_counts  = [thread_shard_count]
thread_shard_counts = zip(thread_counts, shard_counts)

strategies = [ Strategy(
                  pipeline = type_pipeline
                , split_position = None if step == 0 else step
                , shard_count = shard_count
                , thread_count = thread_count
                , shard_directory_prefix = f"{target_path}/synthetic-split"
                , compression_type = compression_type
                , storage_type = storage_type)
             for thread_count, shard_count in thread_shard_counts
                 for step in type_pipeline_steps]

sample_counts = [sample_count]
runs_total = runs

for sample_count in sample_counts:
    for strategy in strategies:
        strategy.profile_strategy(sample_count = sample_count
                                , runs_total = runs_total
                                , system_caching_enabled = True)
        strategy.print_stats()

strategy_dfs = [strat.profile_as_df()       for strat in strategies]
dstat_dfs    = [strat.profile_as_dstat_df() for strat in strategies]

strat_analysis = StrategyAnalysis(strategy_dataframes = strategy_dfs
                                , dstat_dataframes = dstat_dfs)

strat_analysis.save_dfs_as_csv(path=log_path, prefix=f"synthetic-{data_type}-{pipeline_mod}")
