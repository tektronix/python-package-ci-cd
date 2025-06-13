FROM python:3.13-alpine@sha256:bd8f7ae071e5aad0b84264df205f5a156a777652cf4a20583c9f765883f424b9

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
