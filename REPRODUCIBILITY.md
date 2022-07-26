# PRESTO Reproducibility Guide

### Prerequisites

* A Linux box with `unzip` and `tar` installed 
* Storage with at least 1-2TB space
* Installed `docker` with `sudo` rights - [Link](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04)
* Kaggle account and credentials to download a datasets - [Link](https://www.kaggle.com/account/login?phase=startRegisterTab)

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


