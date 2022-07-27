# PRESTO Reproducibility Guide

### Prerequisites

* A Linux box with `unzip` and `tar` installed 
* One or more Linux boxes with 8 cores and 80GB memory and `unzip` + `tar` installed
* Storage with at least 1-2TB space (advisable to have this as a remote storage with 10G up/downlink to run experiments in parallel)
* Installed `docker` with `sudo` rights - [Link](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04)
* Kaggle account and credentials to download a dataset - [Link](https://www.kaggle.com/account/login?phase=startRegisterTab)

### Step 1 - Download datasets

After cloning the repository to the above described node:
* Modify the environment variables in presto/bin/00-environment-variables.sh to point to
  * `DATASETS_PATH` the ~ 1TB storage for the datasets (will take up less after the compressed files are removed
  * `TEMP_PATH` - takes up XX storage for the temporary dataset representations
  * `LOG_PATH` - takes up 10-20GB of storage for the generated logs for all experiments
  * `SUBMISSION_FIGURES_PATH` - TODO
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


### Step 5 - Compile the paper

```
cd bin
./05-compile-paper.sh
scp <target-vm>:<presto-path>/paper/main.pdf .
```

