FROM python:3.10.12-alpine3.18

WORKDIR /app

COPY fast-api/requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY fast-api/ .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]