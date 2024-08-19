FROM python:3.12-slim-bullseye

# Copy over necessary files
COPY requirements.txt /requirements.txt
COPY update_development_dependencies.py /update_development_dependencies.py

# Install dependencies
RUN echo 'APT::Install-Recommends "0";' > /etc/apt/apt.conf.d/00-docker && \
    apt-get update --quiet && \
    apt-get install --quiet --assume-yes --no-install-recommends git && \
    apt-get clean && \
    rm --force --recursive /var/lib/apt/lists/*
RUN python -m pip install --no-cache-dir --requirement /requirements.txt

# Run the updater script as the entrypoint
CMD ["python", "-u", "/update_development_dependencies.py"]
