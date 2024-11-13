FROM python:3.12-alpine@sha256:45447e901056ff27645aa8362ff5bba99f6de346ef0a4dd34160d1ee60c08d35

# Copy over necessary files
COPY requirements.txt /requirements.txt
COPY main.py /main.py

# Install dependencies
RUN python -m pip install --no-cache-dir --requirement /requirements.txt

# Run the Python script as the entrypoint
CMD ["python", "-u", "/main.py"]
