FROM python:3.13-slim@sha256:6cbc4355e9cff50d6ae679b08435b355d388b62d32aa701d08ac9f77bd7c287c

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
