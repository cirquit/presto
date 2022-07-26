import gc
import os
import shlex
import subprocess as sp
import pathlib
import sys
import time
import tensorflow as tf

def drop_io_cache(page_cache=True, dentries_and_inodes=False):
    '''Drops the virtual memory cache so we don't have any accidental cache hits from multiple runs with `run_profiled`
    '''
    code = 0
    if page_cache:
        code += 1
    if dentries_and_inodes:
        code += 2

    drop_cmd = "echo {} > /drop_caches".format(code)
    cmd_array = ["bash", "-c", drop_cmd]

    try:
        sp.run(cmd_array, check=True)
    except sp.CalledProcessError as e:
        print("ERROR: could not drop caches.", e)


def run_profiled(runs_total: int
               , results_directory: pathlib.Path
               , sample_count: int
               , system_cache_enabled: bool
               , enable_tracing: bool
               , function
               , args):
    '''Runs dstat while executing the function(args) (cachestat also working but not necessary)
    Ignores the result of the function

    Problems with `sudo`? Follow this tutorial: https://askubuntu.com/questions/155791/how-do-i-sudo-a-command-in-a-script-without-being-asked-for-a-password

    :param runs_total: int
    :param results_directory: pathlib.Path (will be created if it does not exist)
    :param sample_count: int, used for naming of the files
    :param system_cache_enabled: bool - if enabled, will not drop the cache after run=0
    :param enable_tracing: bool - enable tensorflow tracing for tensorboard
    :param function: function pointer
    :param args: function arguments
    '''

    # generally start the experiment with a clear cache
    drop_io_cache(page_cache=True, dentries_and_inodes=True)

    results_directory.mkdir(exist_ok = True, parents = True)

    _DSTAT_CMD_TPL = "/usr/bin/python2 /usr/bin/dstat -T -ay -m --vm --fs --lock --output {filename}"
    # -T - time counter in seconds
    # -
    _PCT_CMD_TPL = "sudo bash -c" + os.getcwd() + "/bin/cachestat {filename}"

    if enable_tracing:
        options = tf.profiler.experimental.ProfilerOptions(host_tracer_level = 3)

    print("Run finished: ", flush=True, end="")
    for run_id in range(runs_total):

        # if we want to test system level caching, we will not drop the cache over epochs
        if not system_cache_enabled:
            drop_io_cache(page_cache=True, dentries_and_inodes=True)

        if enable_tracing:
            tf.profiler.experimental.start(str(results_directory) ,options=options)

        dstat_csv = results_directory / f"dstat_run-{run_id}_samples-{sample_count}.csv"
        pct_csv = results_directory / f"pc_run-{run_id}_samples-{sample_count}.csv"
        dstat_proc = None
        pct_proc = None
        try:
            dstat_proc = sp.Popen(
                shlex.split(_DSTAT_CMD_TPL.format(filename=dstat_csv)),
                stdout=sp.DEVNULL,
                stderr=sp.DEVNULL
            )
            # pct_proc = sp.Popen(
            #     shlex.split(_PCT_CMD_TPL.format(filename=pct_csv)),
            #     stdout=sp.DEVNULL,
            #     stderr=sp.DEVNULL
            # )
        except Exception as e:
            print(e)

        try:
            # with open(results_directory / f"out_{experiment_id}_{run_id}.csv", "w") as out_file:
            function(run_id, *args)
        finally:
            if dstat_proc is not None:
                dstat_proc.kill()
            if pct_proc is not None:
                # pct_proc.kill()
                os.system(f"sudo kill {pct_proc.pid}")
            if dstat_proc is not None:
                dstat_proc.wait()
            if pct_proc is not None:
                pct_proc.wait()
    
        if enable_tracing:
            tf.profiler.experimental.stop()

        if run_id == runs_total - 1:
            print(f"#{run_id}", flush=True)
        else:
            print(f"#{run_id}, ", end="", flush=True)
            
        # clean up
        gc.collect()
        time.sleep(5)

