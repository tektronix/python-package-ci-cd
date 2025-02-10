FROM python:3.13-alpine@sha256:bb2c06f24622d10187d0884b5b0a66426a9c8511c344492ed61b5d382bd6018c

# Copy over necessary files
COPY requirements.txt /requirements.txt
COPY main.py /main.py

# Install dependencies
RUN python -m pip install --no-cache-dir --requirement /requirements.txt

# Run the Python script as the entrypoint
CMD ["python", "-u", "/main.py"]
