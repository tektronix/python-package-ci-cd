FROM python:3.13-alpine@sha256:97990f8cff85f0a25eef434f77f265d63d3767d15f59bfd19860de0b7f702ead

# Copy over necessary files
COPY requirements.txt /requirements.txt
COPY main.py /main.py

# Install dependencies
RUN python -m pip install --no-cache-dir --requirement /requirements.txt

# Run the Python script as the entrypoint
CMD ["python", "-u", "/main.py"]
