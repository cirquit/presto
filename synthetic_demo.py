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

from type_pipeline import pipeline_definition

thread_shard_count = int(sys.argv[1])
sample_count       = int(sys.argv[2])
data_type          = str(sys.argv[3])
shape              = int(sys.argv[4])
pipeline_mod       = str(sys.argv[5])

storage_type = "remote"
target_path = "/tmp"
log_path = "/log"

# with float32, shape=1 => 0.01MB size
sample_shape = [2500,shape]

type_pipeline = pipeline_definition(shape=sample_shape
                                  , sample_count=sample_count
                                  , data_type=data_type
                                  , computation_type="tensorflow-fn-wrapped")
type_pipeline_steps = list(range(len(type_pipeline)))
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
                , shard_directory_prefix = f"{target_path}/type-split"
                , compression_type = compression_type
                , storage_type = storage_type)
             for thread_count, shard_count in thread_shard_counts
                 for step in type_pipeline_steps]

sample_counts = [sample_count]
runs_total = 2

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

strat_analysis.save_dfs_as_csv(path=log_path, prefix="synthetic")
