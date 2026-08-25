FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install \
    --no-cache-dir \
    -r requirements.txt

# Keep the image non-root by default, including outside Kubernetes. The home
# directory remains writable for current Python/ML runtime caches.
RUN groupadd --gid 10001 polymind \
    && useradd --uid 10001 --gid 10001 --create-home polymind

COPY --chown=10001:10001 . .

EXPOSE 8001

USER 10001:10001

CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8001"]
