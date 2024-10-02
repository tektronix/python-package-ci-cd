FROM python:3.12-alpine@sha256:6666ea354f193c7a296dc2ce0188f318c9d69cb572eceaac1f7dbebd6791431f

# Copy over necessary files
COPY requirements.txt /requirements.txt
COPY main.py /main.py

# Install dependencies
RUN python -m pip install --no-cache-dir --requirement /requirements.txt

# Run the Python script as the entrypoint
CMD ["python", "-u", "/main.py"]
