FROM python:3.9
ENV PYTHONUNBUFFERED 1
RUN mkdir /urlshortner
WORKDIR /urlshortner
COPY requirements.txt /urlshortner/
RUN pip install -r requirements.txt
COPY . /urlshortner/ 
