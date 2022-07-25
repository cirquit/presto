#!/bin/bash

sysbench --test=memory --memory-block-size=1M --memory-total-size=5G run
