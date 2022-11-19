FROM python:3.8.3
WORKDIR /app
ADD . /app
COPY ./requirements.txt /app/requirements.txt
RUN python3 -m pip install -r requirements.txt
EXPOSE 5000
CMD ["python3","app.py"]
