FROM python:3.12-alpine@sha256:72d7e22643cd021335da692b63ff338cd3461f8a830183730148618ceac90840

# Copy over necessary files
COPY requirements.txt /requirements.txt
COPY main.py /main.py

# Install dependencies
RUN python -m pip install --no-cache-dir --requirement /requirements.txt

# Run the Python script as the entrypoint
CMD ["python", "-u", "/main.py"]
