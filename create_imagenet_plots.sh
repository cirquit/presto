#!/bin/bash
cd analysis
ipython -c "%run imagenet-analysis.ipynb"
ipython -c "%run imagenet-greyscale-analysis.ipynb"
