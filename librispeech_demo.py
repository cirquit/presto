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

from librispeech_pipeline import pipeline_definition

thread_shard_count = int(sys.argv[1])
compression_type   = str(sys.argv[2])
sample_count       = int(sys.argv[3])
runs               = int(sys.argv[4])

storage_type = "remote"
source_path  = "/dataset/LibriSpeech/train-clean-100"
target_path  = "/tmp"
log_path     = "/logs"

# define pipeline with the source path
librispeech_pipeline = pipeline_definition(source_path = source_path)
librispeech_pipeline_steps = list(range(len(librispeech_pipeline)))
del librispeech_pipeline_steps[1] # remove the 1-list-files strategy from profiling

thread_counts = [thread_shard_count]
shard_counts  = [thread_shard_count]
thread_shard_counts = zip(thread_counts, shard_counts)

strategies = [ Strategy(
                  pipeline = librispeech_pipeline
                , split_position = None if step == 0 else step
                , shard_count = shard_count
                , thread_count = thread_count
                , shard_directory_prefix = f"{target_path}/librispeech-split"
                , compression_type = compression_type
                , storage_type = storage_type)
             for thread_count, shard_count in thread_shard_counts
                 for step in librispeech_pipeline_steps]

sample_counts = [sample_count]
runs_total = runs

for sample_count in sample_counts:
    for strategy in strategies:
        strategy.profile_strategy(sample_count = sample_count
                                , runs_total = runs_total
                                , system_cache_enabled = True)
        strategy.print_stats()

strategy_dfs = [strat.profile_as_df()       for strat in strategies]
dstat_dfs    = [strat.profile_as_dstat_df() for strat in strategies]

strat_analysis = StrategyAnalysis(strategy_dataframes = strategy_dfs
                                , dstat_dataframes = dstat_dfs)

strat_analysis.save_dfs_as_csv(path=log_path, prefix=f"librispeech")
