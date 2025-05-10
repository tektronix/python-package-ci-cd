FROM python:3.13-alpine@sha256:f50e1ca5ac620527f8a8acc336cab074dc8a418231380cd6d9eafb4103931f91

# Copy over necessary files
COPY requirements.txt /requirements.txt
COPY main.py /main.py

# Install dependencies
RUN apk update && \
    apk add --no-cache git && \
    rm -rf /var/cache/apk/* && \
    python -m pip install --no-cache-dir --requirement /requirements.txt

# Run the Python script as the entrypoint
CMD ["python", "-u", "/main.py"]
