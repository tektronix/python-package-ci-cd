FROM python:3.12-alpine@sha256:edd1d8559c585e1e9a9b79de44ac27f8ac32cb0c7323e112ae6870ceeecd8dbf

# Copy over necessary files
COPY requirements.txt /requirements.txt
COPY main.py /main.py

# Install dependencies
RUN apk update && \
    apk add --no-cache git && \
    rm -rf /var/cache/apk/*
RUN python -m pip install --no-cache-dir --requirement /requirements.txt

# Run the Python script as the entrypoint
CMD ["python", "-u", "/main.py"]
