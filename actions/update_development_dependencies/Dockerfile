FROM python:3.13-alpine@sha256:38042d48d2ca487ac6f6561dbd7a2096fdd528d8ad6802ad5ec195b30bd821c9

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
