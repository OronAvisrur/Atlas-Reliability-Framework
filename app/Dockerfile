FROM python:3.11-slim
WORKDIR /code
RUN pip install --no-cache-dir \
    fastapi==0.104.1 \
    uvicorn[standard]==0.24.0.post1 \
    httpx==0.25.1 \
    prometheus-client==0.19.0 \
    psycopg2-binary==2.9.9 \
    python-jose[cryptography]==3.3.0 \
    passlib[bcrypt]==1.7.4 \
    bcrypt==4.0.1 \
    pydantic-settings==2.1.0
COPY . /code/app
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
