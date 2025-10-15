FROM python:3.14-slim@sha256:5cfac249393fa6c7ebacaf0027a1e127026745e603908b226baa784c52b9d99b

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
