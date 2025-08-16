FROM python:3.13-alpine@sha256:a70b35b575e33d951e3f9d3fe94163ef0fd338c22552bc587a1b098a87ed6184

# Copy over necessary files
COPY requirements.txt /requirements.txt
COPY main.py /main.py

# Install dependencies
RUN python -m pip install --no-cache-dir --requirement /requirements.txt

# Run the Python script as the entrypoint
CMD ["python", "-u", "/main.py"]
