FROM python:3.13-alpine@sha256:f80206d96683c1b27cd522dc300f791a48362b895ad5c0bdd26f78f853c76fa5

# Copy over necessary files
COPY requirements.txt /requirements.txt
COPY main.py /main.py

# Install dependencies
RUN python -m pip install --no-cache-dir --requirement /requirements.txt

# Run the Python script as the entrypoint
CMD ["python", "-u", "/main.py"]
