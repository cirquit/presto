#!/bin/bash
cd analysis
ipython -c "%run misc-plots.ipynb"
ipython -c "%run synthetic-data-read-analysis.ipynb"
ipython -c "%run synthetic-data-multithreading-analysis.ipynb"
# ipython -c "%run synthetic-data-processing-analysis.ipynb"
