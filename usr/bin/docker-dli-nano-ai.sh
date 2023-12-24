#!/bin/bash

VERSION=v2.0.2-r32.7.1

sudo systemctl restart nvargus-daemon 

docker run \
	--runtime nvidia \
	-it --rm \
	--network host \
        --volume ~/jetson_tweaks/home/nvdli-data:/nvdli-nano/data \
	--volume ~/jetson_tweaks/home/jupyter_notebooks:/nvdli-nano/jupyter_notebooks \
	--volume /tmp/argus_socket:/tmp/argus_socket \
        --device /dev/video0 \
        --device /dev/video1 \
        nvcr.io/nvidia/dli/dli-nano-ai:$VERSION \
	$*
