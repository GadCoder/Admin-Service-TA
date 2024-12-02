FROM python:3.12

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["fastapi", "run", "src/app/adapters/entrypoints/application.py", "--host", "0.0.0.0", "--port", "8080"]