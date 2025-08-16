FROM python:3.13-alpine@sha256:8e4890b7d6e736b52bee1424d1bfaaa05145abbe626ea876d6770441e2bdf587

# Copy over necessary files
COPY requirements.txt /requirements.txt
COPY main.py /main.py

# Install dependencies
RUN apk update && \
    apk add --no-cache \
        cargo \
        git \
        rust \
    && \
    rm -rf /var/cache/apk/* && \
    python -m pip install --no-cache-dir --requirement /requirements.txt

# Run the Python script as the entrypoint
CMD ["python", "-u", "/main.py"]
