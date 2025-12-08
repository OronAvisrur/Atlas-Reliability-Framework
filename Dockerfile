FROM python:3.14-slim

WORKDIR /app

RUN pip install --no-cache-dir fastapi==0.104.1 uvicorn[standard]==0.24.0 prometheus-client==0.19.0 httpx==0.27.0 pydantic==2.10.12

COPY app/ ./app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]