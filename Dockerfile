FROM python:3.8-slim

WORKDIR /app

ADD . /app

# Update package lists and install necessary packages
RUN apt-get update && apt-get install -y \
    git \
    unzip

# Create a virtual environment and activate it
# RUN python3 -m venv myenv
# RUN /bin/bash -c "source myenv/bin/activate"

# Install dependencies
RUN pip install flask requests gunicorn bs4

# Make port 18888 available to the world outside this container
EXPOSE 18888


# Command to run the application
CMD ["python", "-m", "gunicorn", "--workers=4", "--bind=0.0.0.0:18888", "app:app"]
