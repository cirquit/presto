FROM ubuntu:18.04
RUN apt update
# installing necessary packages for python preprocessing
RUN apt install wget dstat unzip build-essential libsndfile-dev ffmpeg software-properties-common python3.7-distutils -y
WORKDIR /root/
# setting up anaconda for python 3.7 on ubuntu18.04
ENV PATH="/root/miniconda3/bin:${PATH}"
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && chmod +x Miniconda3-latest-Linux-x86_64.sh && ./Miniconda3-latest-Linux-x86_64.sh -b
RUN rm Miniconda3-latest-Linux-x86_64.sh
RUN conda create --name presto python=3.7 -y
SHELL ["conda", "run", "--no-capture-output", "-n", "presto", "/bin/bash", "-c"]
RUN python --version
COPY requirements.txt /root/requirements.txt
RUN pip install -r requirements.txt
RUN pip install --upgrade setuptools
# run the experiments over the mounted /root/ <-> presto/ directory
ENV PATH="/opt/conda/envs/presto/bin:${PATH}"
WORKDIR /root/presto
CMD ["conda", "run", "--no-capture-output", "-n", "presto", "./create_imagenet_plots.sh"]
