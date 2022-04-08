FROM python:3.7-alpine
WORKDIR /dockerimage
COPY . /dockerimage
RUN pip install -r requirements.txt
EXPOSE 80
CMD ["python", "main.py"]
