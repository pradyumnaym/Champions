FROM mcr.microsoft.com/mirror/docker/library/python:3.10-slim

# Copy the requirements.txt file to the /code directory.
# This file only lives in the previous Docker stage, that's why we use --from-requirements-stage to copy it.
#COPY requirements.txt /code/requirements.txt

# Copy the app directory to the /code directory.
COPY ./app /code/app

# Set the current working directory to /code.
WORKDIR /code

# Install the package dependencies in the generated requirements.txt file.
RUN pip install --no-cache-dir --upgrade -r /code/app/requirements.txt

#Expose 3000
EXPOSE 3000

# Run the uvicorn command, telling it to use the app object imported from app.main.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3000"]
