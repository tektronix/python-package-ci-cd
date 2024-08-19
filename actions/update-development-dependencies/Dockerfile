FROM python:3.12-slim

# Copy over necessary files
COPY requirements.txt /requirements.txt
COPY update_development_dependencies.py /update_development_dependencies.py

# Install dependencies
RUN python -m pip install --no-cache-dir --requirement /requirements.txt

# Run the updater script as the entrypoint
CMD ["python", "/update_development_dependencies.py"]
