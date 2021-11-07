import re
import numpy as np
import math
import matplotlib.pylab as plt


def show_values_on_catplot(plot, axiscount, height, rotation='10', skip=None):
    '''Shows values on a cat(bar)plot
    '''
    for i in range(0,axiscount):
        ax = plot.facet_axis(0,i)
        for i, p in enumerate(ax.patches):
            if skip != None:
                if i % skip == 0:
                    continue
            additional_height = height if i % 2 == 0 else height*2
            org_height = p.get_height()
            if org_height > 1000:
                text = str(round(org_height / 1000,1)) + "K"
            else:
                text = str(int(org_height))          
            ax.text(p.get_x() - 0.01, 
                    p.get_height() + additional_height, 
                    text,
                    color='black', 
                    rotation=rotation, 
                    size='large')



def show_values_on_bars(axs, h_v="v", space=0.4, rotation=25, additional_space=None,
additional_x_space=None, round_to=0, postfix=None):
    '''Shows values from bars. Adapted from some SO answer about this issue
    '''
    def _show_on_single_plot(ax):
        if h_v == "v":
            for i, p in enumerate(ax.patches):
                _x = p.get_x() + p.get_width() / 2
                _y = p.get_y() + p.get_height() + float(space)
                if additional_space != None:
                    _y += additional_space[i]
                if additional_x_space != None:
                    _x += additional_x_space[i]
                if round_to != 0:
                    value = round(p.get_height, round_to)
                else:
                    if math.isnan(p.get_height()):
                        height = 0
                    else:
                        height = p.get_height()
                    value = int(height)
                    value_str = str(value)
                    if postfix==None:
                        value_str_pretty = make_big_number_pretty(value_str)
                    else:

                        value_str_pretty = make_big_number_pretty(value_str) + postfix
                ax.text(_x, _y, value_str_pretty, ha="center", rotation=rotation) 
        elif h_v == "h":
            for p in ax.patches:
                _x = p.get_x() + p.get_width() + float(space)
                _y = p.get_y() + p.get_height()
                value = int(p.get_width())
                ax.text(_x, _y, value, ha="left")

    if isinstance(axs, np.ndarray):
        for idx, ax in np.ndenumerate(axs):
            _show_on_single_plot(ax)
    else:
        _show_on_single_plot(axs)


def save_figure(name, local_fig_dir, dpi=300, file_type="pdf"):
    '''Save matplotlib figures at a local directory based on the full hardcoded path
    :param name: str - name of the pdf figure (e.g., "throughput")
    :param local_fig_dir: str - plots are saved under a subdirectory based on the pipeline (e.g., "image-pipeline")
    '''
    figure_path   = "/home/asa/Documents/github-repos/thesis/sigmod-2022-submission/figures"
    full_fig_dir  = figure_path + "/" + local_fig_dir
    full_fig_path = full_fig_dir + "/" + name + "." + file_type
    plt.savefig(full_fig_path, dpi=dpi, bbox_inches = "tight")


def make_big_number_pretty(value: str):
    return re.sub(r'(?<!^)(?=(\d{3})+$)', r',', value)
