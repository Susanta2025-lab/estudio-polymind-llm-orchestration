FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install \
    --no-cache-dir \
    -r requirements.txt

# The Helm chart runs the application as this non-root identity. A real passwd
# entry is required by Python/ML libraries that resolve the current user.
RUN groupadd --gid 10001 polymind \
    && useradd --uid 10001 --gid 10001 --create-home polymind

COPY . .

EXPOSE 8001

CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8001"]
