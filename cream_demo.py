import os
import sys
import time
import numpy as np
import pandas as pd
import seaborn as sns
import tensorflow as tf
import matplotlib.pylab as plt
from pathlib import Path

from presto          import pipeline
from presto.analysis import StrategyAnalysis
from presto.strategy import Strategy

from cream_pipeline import pipeline_definition

thread_shard_count = int(sys.argv[1])
sample_count       = int(sys.argv[2])
compression_type   = str(sys.argv[3])
storage_type       = str(sys.argv[4])

# dataset path
home_path = str(Path.home())

source_path_local = f"{home_path}/Downloads/datasets/cream/"
target_path_local = "."
source_path_vm_local = f"{home_path}/cream/"
target_path_vm_local = f"{home_path}/dataset-profiles"
source_path_ceph = f"{home_path}/rbgstorage/nilm/i13-dataset/CREAM/X8"
target_path_ceph = f"{home_path}/rbgstorage/temp/isenko/dataset-profiles"

if storage_type == "ceph-hdd":
    source_path = source_path_ceph
    target_path = target_path_ceph
elif storage_type == "local-vm-ssd":
    source_path = source_path_vm_local
    target_path = target_path_vm_local
elif storage_type == "local-ssd":
    source_path = source_path_local
    target_path = target_path_local
else:
    print("Pick a valid storage_type: ceph-hdd, local-vm-ssd, local-ssd")
    sys.exit(0)

# define pipeline with the source path
cream_pipeline = pipeline_definition(source_path = source_path)
cream_pipeline_steps = list(range(len(cream_pipeline)))
del cream_pipeline_steps[1] # remove the 1-voltage-+-current-extraction-6.4kHz strategy for application level cache
del cream_pipeline_steps[0] # remove the 0-fully-online strategy for compression

thread_counts = [thread_shard_count]
shard_counts  = [thread_shard_count]
thread_shard_counts = zip(thread_counts, shard_counts)

strategies = [ Strategy(
                  pipeline = cream_pipeline
                , split_position = None if step == 0 else step 
                , shard_count = shard_count
                , thread_count = thread_count
                , shard_directory_prefix = f"{target_path}/cream-split"
                , compression_type = compression_type
                , storage_type = storage_type)
             for thread_count, shard_count in thread_shard_counts
                 for step in cream_pipeline_steps]

sample_counts = [sample_count]
runs_total = 1

for sample_count in sample_counts:
    for strategy in strategies:
        strategy.profile_application_cached_strategy(sample_count = sample_count
                                , runs_total = runs_total)
        strategy.print_stats()
        
strategy_dfs = [strat.profile_as_df()       for strat in strategies]
dstat_dfs    = [strat.profile_as_dstat_df() for strat in strategies]

strat_analysis = StrategyAnalysis(strategy_dataframes = strategy_dfs
                                , dstat_dataframes = dstat_dfs)

strat_analysis.save_dfs_as_csv(path="./logs", prefix=f"cream-application-cache")
