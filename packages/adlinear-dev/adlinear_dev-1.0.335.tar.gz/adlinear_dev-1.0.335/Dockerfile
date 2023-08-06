FROM python:3.9-slim

# Mount: install directory
COPY . /adlinear
WORKDIR /adlinear/
# Install requirements first, that can avoid some conflicts sometimes (don't ask me why)
RUN apt-get update && apt-get install -y python3-tk
RUN pip install -U pip && pip install -r requirements.txt && pip install .