#python
FROM python:3.6.8
RUN pip install -r requirements.txt
CMD ["python", "flask run"]
#-------------------------------------------------------------
