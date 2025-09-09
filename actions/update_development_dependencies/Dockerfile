FROM python:3.13-slim@sha256:f71edd78ba248161f59959d8cac0bafb58b0bbe10819e21f46499a8b9e9f28f0

# Copy over necessary files
COPY requirements.txt /requirements.txt
COPY main.py /main.py

# Install dependencies
RUN apt-get update --quiet && \
    apt-get install --quiet --yes --no-install-recommends \
        cargo \
        git \
        rustc \
    && \
    rm --force --recursive /var/lib/apt/lists/* && \
    python -m pip install --no-cache-dir --requirement /requirements.txt

# Run the Python script as the entrypoint
CMD ["python", "-u", "/main.py"]
