FROM python:3.6
ADD . / code/
WORKDIR /code
RUN pip install -r components.txt
CMD ["python", "app.py"]

