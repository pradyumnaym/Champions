FROM mcr.microsoft.com/mirror/docker/library/python:3.8-slim as requirements-stage

# Pin Poetry to a specific version to make Docker builds reproducible.
ENV POETRY_VERSION 1.1.13

# Set ENV variables that make Python more friendly to running inside a container.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

# By default, pip caches copies of downloaded packages from PyPI. These are not useful within
# a Docker image, so disable this to reduce the size of images.
ENV PIP_NO_CACHE_DIR 1

# Set /tmp as the current working directory.
# Here's where we will generate the file requirements.txt
WORKDIR /tmp

# Install Poetry into the global environment to isolate it from the venv. This prevents Poetry
# from uninstalling parts of itself.
RUN pip install "poetry==${POETRY_VERSION}"

# Copy in project dependency specification.
COPY pyproject.toml poetry.lock ./

# Generate the requirements.txt file.
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes


# ------------- #
# Final Staging #
# ------------- #
# This is the final stage, anything here will be preserved in the final container image.
FROM mcr.microsoft.com/mirror/docker/library/python:3.8-slim

# Set the current working directory to /code.
WORKDIR /code

# Copy the requirements.txt file to the /code directory.
# This file only lives in the previous Docker stage, that's why we use --from-requirements-stage to copy it.
COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

# Install the package dependencies in the generated requirements.txt file.
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the app directory to the /code directory.
COPY ./app /code/app

#Expose 3000
EXPOSE 3000

# Run the uvicorn command, telling it to use the app object imported from app.main.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3000"]
