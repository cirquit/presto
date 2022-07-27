FROM python:3.7

WORKDIR /tmp/

RUN pip install kaggle

RUN mkdir -p /root/.kaggle
COPY ./kaggle.json /root/.kaggle/kaggle.json
RUN chmod 600 /root/.kaggle/kaggle.json
RUN ls -la /root/.kaggle/

CMD ["kaggle", "competitions", "download", "-c", "imagenet-object-localization-challenge"]
