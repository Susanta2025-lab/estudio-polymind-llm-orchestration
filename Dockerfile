FROM python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HF_HOME=/tmp/polymind-cache/huggingface \
    SENTENCE_TRANSFORMERS_HOME=/tmp/polymind-cache/sentence-transformers \
    TRANSFORMERS_OFFLINE=1 \
    HF_HUB_OFFLINE=1 \
    MODEL_ARTIFACT_DIR=/opt/polymind/models \
    MODEL_OFFLINE_MODE=true \
    TMPDIR=/tmp

COPY requirements.txt requirements-ml-cpu.txt ./

RUN pip install \
    --no-cache-dir \
    --no-deps \
    -r requirements-ml-cpu.txt \
    && pip install \
    --no-cache-dir \
    -r requirements.txt

COPY config/__init__.py config/model_artifacts.py config/
COPY scripts/fetch_models.py scripts/fetch_models.py

# Network access is deliberately enabled only for the immutable build step.
# Runtime loaders use these local paths with local_files_only=True.
RUN PYTHONPATH=/app TRANSFORMERS_OFFLINE=0 HF_HUB_OFFLINE=0 \
    python scripts/fetch_models.py /opt/polymind/models \
    && rm -rf /opt/polymind/cache /root/.cache

# Keep the image non-root by default, including outside Kubernetes. Runtime
# caches use the explicit temporary path; the user has no writable home.
RUN groupadd --gid 10001 polymind \
    && useradd --uid 10001 --gid 10001 --no-create-home --home-dir /nonexistent polymind

COPY --chown=10001:10001 . .

EXPOSE 8001

USER 10001:10001

CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8001"]
