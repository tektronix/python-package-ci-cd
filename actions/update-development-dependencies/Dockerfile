FROM python:3.12-alpine

# Copy over necessary files
COPY requirements.txt /requirements.txt
COPY update_development_dependencies.py /update_development_dependencies.py

# Install dependencies
RUN apk update && \
    apk add --no-cache git && \
    rm -rf /var/cache/apk/*
RUN python -m pip install --no-cache-dir --requirement /requirements.txt

# Run the updater script as the entrypoint
CMD ["python", "-u", "/update_development_dependencies.py"]
