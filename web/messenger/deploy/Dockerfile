FROM python:3.9

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_ENV=production

COPY . .

EXPOSE 8080

CMD ["flask", "run", "--port=8080"]