FROM python:3.12-alpine@sha256:7130f75b1bb16c7c5d802782131b4024fe3d7a87ce7d936e8948c2d2e0180bc4

# Copy over necessary files
COPY requirements.txt /requirements.txt
COPY main.py /main.py

# Install dependencies
RUN python -m pip install --no-cache-dir --requirement /requirements.txt

# Run the Python script as the entrypoint
CMD ["python", "-u", "/main.py"]
