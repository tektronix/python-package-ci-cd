FROM python:3.13-alpine@sha256:40241d5dec48a0bc7a070e2244309fb409cd25509c56fef871494a9bbc57d51e

# Copy over necessary files
COPY requirements.txt /requirements.txt
COPY main.py /main.py

# Install dependencies
RUN python -m pip install --no-cache-dir --requirement /requirements.txt

# Run the Python script as the entrypoint
CMD ["python", "-u", "/main.py"]
