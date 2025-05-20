FROM python:3.13-slim


WORKDIR /app

ADD requirements.txt .
RUN pip install -r requirements.txt

ADD app .
ADD binary/converter /converter
ADD templates templates
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "32", "app:app"]
