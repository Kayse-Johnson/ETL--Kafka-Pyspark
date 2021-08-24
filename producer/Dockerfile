FROM python:3.7
ADD requirements.txt /
RUN pip install -r requirements.txt
ADD producer.py /
CMD ["python" , "producer.py"]
