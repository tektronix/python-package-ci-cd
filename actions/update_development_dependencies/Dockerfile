FROM python:3.13-alpine@sha256:f66b117ec7379d205d7e67adc0ba5df1e4a1e98a7e17076b0e1075fde65feb04

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
