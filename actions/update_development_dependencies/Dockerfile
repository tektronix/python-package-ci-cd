FROM python:3.13-alpine@sha256:a9bceef1fb20825c4f4c28eca616e5c1497bec444ea31205cc667b0b962fd9df

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
