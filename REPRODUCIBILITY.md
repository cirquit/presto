# PRESTO Reproducibility Guide

### Prerequisites

* One or more Linux boxes with 8 cores and 80GB memory and `unzip`, `tar`, `make` and `sed` installed
  - We used KVM virtualization without Docker on with a Intel Xeon E5-2630 v3 8x@2.4 GHz and DDR4 memory
* Storage with at least 1-2TB space (advisable to have this as a remote storage with 10G up/downlink to run experiments in parallel)
* Installed `docker` with `sudo` rights - [Link](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04)
* Kaggle account and credentials to download a dataset - [Link](https://www.kaggle.com/account/login?phase=startRegisterTab)

### TLDR - takes X days to run sequentially

```
cd presto/bin
# modify the storage paths
source 00-environment-variables.sh
./0-download-datasets.sh && ./02-run-experiments.sh all && ./03-collect-logging-data.sh all && ./04-plot-figures.sh all && ./05-compile-paper.sh
```

Copy the paper from `presto/paper/main.pdf` to your local PC.


### Step 1 - Download datasets

After cloning the repository to the above described node:
* Modify the environment variables in presto/bin/00-environment-variables.sh to point to
  * `DATASETS_PATH` the ~ 1TB storage for the datasets (will take up less after the compressed files are removed
  * `TEMP_PATH` - takes up XX storage for the temporary dataset representations
  * `LOG_PATH` - takes up 10-20GB of storage for the generated logs for all experiments
* Move your downloaded `kaggle.json` to `presto/bin/kaggle.json`

```bash
cd presto/bin
source 00-environment-variables.sh
./01-download-datasets.sh # Follow instructions
```

### Step 2 - Run experiments

The bash script takes one argument that specifies which experiments to run:
- `all` - runs all experiments sequentially
- `imagenet`
- `cubepp`
- `owt`
- `cream`
- `commonvoice`
- `librispeech`
- `synthetic`

As some of these take weeks to run, it's advisable to run them in parallel on multiple machines with shared storage.
Or copy the results from the individual `LOG_PATH` to the machine that will do the final analysis and plots.

```bash
cd presto/bin
source 00-environment-variables.sh
./02-run-experiments.sh <argument>
```

**WARNING**:
We call `rm -rf` on the `TEMP_PATH` to delete the temporary files with wildcards like `$TEMP_PATH/imagenet*`.
Be sure not to put anything important on that path.

### Step 3 - Collect logging data

Same command line arguments as step 2.

```bash
cd presto/bin
source 00-environment-variables.sh
./03-collect-logging-data.sh <argument>
```

### Step 4 - Visualize and plot data

Same command line arguments as step 2.

```bash
cd presto/bin
source 00-environment-variables.sh
./04-plot-figures.sh <arguments>
```

### Step 5 - Compile the paper

```
cd presto/bin
./05-compile-paper.sh
# from your local PC
scp <target-vm>:<presto-path>/paper/main.pdf .
```

### Step 6 - Compare results

The entire paper topic is to profile your individual hardware bottlenecks, so your results mights differ a lot in absolute numbers.
Also, we ran every experiment 5 times to amortize slight outliers due to hardware effects, but would take a lot more time to reproduce, so we setup our scripts to run once.

However, the relative differences should be similar to our results:
* Figure 6
  - the dotted throughput line has the same trend
  - the storage consumption should be identical
* Figure 7 - same trend
* Figure 8
  - if you stick to 80GB memory per node, same trend
  - if not, the strategies that fit into memory will be faster compared to epoch 0
* Figure 9
  - same trend, i.e. *app-cache* is much faster than *no-cache* at 20.5MB, but similar at 0.01MB
* Figure 10
  - storage consumption should be close to identical
  - compression performance should be similar (same trend, i.e., at subfigure 'e' compression should
    be better than no compression, but may be different for hardware specific reasons)
    - We noticed that this particular plot at the "resized" strategy can be volatile sometimes and have equal performance to "none" compression at a single run
* Figure 11
  - same trend
* Figure 12
  - same trend
* Figure 13
  - same trend (numpy has a slowdown, tensorflow has a speedup)
* Figure 14
  - same trend, subfigure 'a' at *applied-greyscale* is faster than at subfigure 'b'

The remaining figures and tables were made "manually" from the results and reflect the actual profiling for our hardware.
We include their generation, but do not substitute the numbers, as the findings might show different bottlenecks due to different hardware. (e.g. Fig.3, Fig.4, Tab.3, Tab.5)
