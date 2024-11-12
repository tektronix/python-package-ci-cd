FROM python:3.12-alpine@sha256:18e32de1f6fb7bf902b19965c6657d0521fb1ab2a36df7843fe9f78efa91a3c0

# Copy over necessary files
COPY requirements.txt /requirements.txt
COPY main.py /main.py

# Install dependencies
RUN python -m pip install --no-cache-dir --requirement /requirements.txt

# Run the Python script as the entrypoint
CMD ["python", "-u", "/main.py"]
