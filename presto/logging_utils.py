import os
import re

import pandas as pd
import seaborn as sns


def destructuring_enumerate(root_path, name_pattern, glob_pattern="*"):
    dirs = root_path.glob(glob_pattern)
    
    for dir in dirs:
        matcher = re.match(name_pattern, dir.name)
        if matcher:
            yield dir, matcher.groupdict()


def load_stats(data_root):
    dstats_df = load_dstats_files(data_root).set_index(("epoch", "epoch"))
    pc_df = load_pc_files(data_root).set_index("epoch")
    
    df = dstats_df.join(pc_df, how="inner")
    
    df = df.reset_index()
    df["second"] = (df.set_index("exp_run")["index"] - df.groupby("exp_run").min()["index"]).reset_index()["index"]
    
    return df


def _prepare_columns(columns):
    last = None
    for (l1, l2) in columns:
        if not l1.startswith("Unnamed"):
            last = l1
        yield (last, l2)


def load_dstats_file(csv_path):
    df = pd.read_csv(csv_path, header=[4,5])
    
    df.columns = pd.MultiIndex.from_tuples(_prepare_columns(df.columns))
    
    df = df.loc[:, ~df.columns.duplicated()]
    
    df["epoch", "epoch"] = df["epoch", "epoch"].astype(int)
    # add normalized time
    df["t"] = df["epoch", "epoch"]
    df["t"] -= df.t.min()
    
    return df


def load_dstats_files(data_root, **additional_tags):
    def load(csv_path, run_nr):
        df = load_dstats_file(csv_path)
        df["exp_run"] = run_nr
        return df
    
    dfs = [load(path, i) for i, path in enumerate(sorted(data_root.glob("dstat*.csv")))]
    df = pd.concat(dfs)
    
    for field, value in additional_tags.items():
        df[field] = value
    
    return df


def load_pc_files(data_root):
    def load(csv_path, run_nr):
        df = pd.read_csv(csv_path)
        df[" hit_ratio"] = df[" hit_ratio"].map(lambda s: float(s.replace("%", "")) / 100.0)
        df["exp_run"] = run_nr
        return df
    
    dfs = [load(path, i) for i, path in enumerate(sorted(data_root.glob("pc*.csv")))]
    return pd.concat(dfs)


def load_outputs(data_root, **additional_tags):
    def load(csv_path, run_nr):
        df = pd.read_csv(csv_path)
        df["exp_run"] = run_nr
        return df
    
    dfs = pd.concat([load(path, i) for i, path in enumerate(sorted(data_root.glob("out*.csv")))])
    
    dfs.columns = [c.strip() for c in dfs.columns]
    
    for field, value in additional_tags.items():
        dfs[field] = value
    
    return dfs


def cm(cm_val1, cm_val2=None):
    if cm_val2 is None:
        return cm_val1 / 2.54
    else:
        return cm_val1 / 2.54, cm_val2 / 2.54
    
    
def save_figure(figure, name, root="plots", format="pdf"):
    figure.savefig(os.path.join(root, name + "." + format), bbox_inches="tight")
    
    
def delta_chart(df, order, attribute="throughput_docs", grouping_attribute="strategy"):
    avg_tps = df.groupby(grouping_attribute)[attribute].mean().to_frame().loc[order]
    improvements = avg_tps.diff().iloc[1:].reset_index()
    improvements.columns = [grouping_attribute, "delta"]
    chart = sns.barplot(x=grouping_attribute, y="delta", data=improvements)
    return chart