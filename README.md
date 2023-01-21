# PRESTO

**Pre**processing **St**rategy **O**ptimizer is a library for TensorFlow that automates the generic pipelines’ profiling process.
> Published at SIGMOD '22
> [Where Is My Training Bottleneck? Hidden Trade-Offs in Deep Learning Preprocessing Pipelines](https://dl.acm.org/doi/10.1145/3514221.3517848)

```
@inbook{10.1145/3514221.3517848,
author = {Isenko, Alexander and Mayer, Ruben and Jeffrey, Jedele and Jacobsen, Hans-Arno},
title = {Where Is My Training Bottleneck? Hidden Trade-Offs in Deep Learning Preprocessing Pipelines},
year = {2022},
isbn = {9781450392495},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
url = {https://doi.org/10.1145/3514221.3517848},
booktitle = {Proceedings of the 2022 International Conference on Management of Data},
numpages = {15}
}
```

# Reproducibility

* Fully automated via Docker and Bash
* [**REPRODUCIBILITY README**](REPRODUCIBILITY.md)

---
### How to use Presto for your own experiments

There are basically two things needed:
* A definition of your pipeline (take [`imagenet_pipeline.py`](imagenet_pipeline.py) as an example)
* Generate the different strategies based on the pipeline, see [`imagenet_demo.py`](imagenet_demo.py)
* Run the experiments with `.profile_strategy(...)` with all the possible configuration options (see [`presto/strategy.py`](presto/strategy.py) as reference)
* Load the logs, saved as `pd.Dataframes` into a [`StrategyAnalysis`](presto/analysis.py) and analyze the data with, e.g., a `weighted_summary(...)` call
* The scores are presorted, you can decide on which strategy you want to decide, or automatically pick the highest one. The corresponding strategy is a valid `tf.data.Dataset` pipeline, so you can just reuse it in your pipeline.
