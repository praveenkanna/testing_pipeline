FROM python:3.8.2-slim-buster

LABEL maintainer="Praveen Kumar Kanna"

ENV LIBGIT_VERSION 1.0.0

# Cmake is a dependency for building libgit2
RUN apt-get update && apt-get install -y git libssl-dev wget cmake

# Downloading and building libgit2
RUN wget https://github.com/libgit2/libgit2/archive/v${LIBGIT_VERSION}.tar.gz \
    && tar xzf v${LIBGIT_VERSION}.tar.gz \
    && rm -rf v${LIBGIT_VERSION}.tar.gz \
    && cd libgit2-${LIBGIT_VERSION} \
    && cmake . \ 
    && make \
    && make install \
    # Required for updating the libs
    && ldconfig \
    && pip install pygit2==1.2.1

# Copy all the code into the image
ADD . /pygit2_testing

WORKDIR /pygit2_testing

# run the command while starting the container
CMD [ "python", "git_update.py" ]
