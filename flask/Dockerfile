FROM ubuntu:22.04

# Set environment variables to avoid tzdata prompt
ENV DEBIAN_FRONTEND=noninteractive

# Install basic dependencies
RUN apt update \ 
  && apt install -y \
    wget \
    fontconfig \
    libfontforge4 \
    poppler-utils \
    xpdf \
    ghostscript \
    libpng-dev \
    libjpeg-dev \
    libtiff-dev \
    libxml2-dev \
    libpoppler-cpp-dev \
    python3 \
    python3-pip \
    python3-venv \
  && apt clean \
  && rm -rf /var/lib/apt/lists/*

# Copy your .deb file into container (assume it's in the same directory)
COPY pdf2htmlEX-0.18.8.rc1-master-20200630-Ubuntu-bionic-x86_64.deb /tmp/pdf2htmlex.deb

# Install it (use `apt` or `dpkg` then fix deps)
RUN dpkg -i /tmp/pdf2htmlex.deb || apt -f install -y

# Install requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# Add source code
WORKDIR app

# Set environment variables
ENV FLASK_APP=app.py

# Run
# CMD [ "flask", "run", "--host=0.0.0.0", "--port=5000" ]
