#!/bin/bash

VERSION=v2.0.1-r32.5.0

docker run --runtime nvidia -it --rm \
        --network host \
        --volume ~/nvdli-data:/nvdli-nano/data \
        --volume /tmp/argus_socket:/tmp/argus_socket \
        --device /dev/video0 \
        --device /dev/video1 \
        nvcr.io/nvidia/dli/dli-nano-ai:$VERSION
