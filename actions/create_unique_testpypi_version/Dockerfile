FROM python:3.13-alpine@sha256:610020b9ad8ee92798f1dbe18d5e928d47358db698969d12730f9686ce3a3191

# Copy over necessary files
COPY requirements.txt /requirements.txt
COPY main.py /main.py

# Install dependencies
RUN python -m pip install --no-cache-dir --requirement /requirements.txt

# Run the Python script as the entrypoint
CMD ["python", "-u", "/main.py"]
