#!/bin/bash

IMAGE=nvcr.io/nvidia/l4t-ml
VERSION=r32.5.0-py3
WORKDIR=/home

docker run \
	--runtime nvidia \
	-it --rm \
	--network host \
        --volume ~/jetson_tweaks/home/nvdli-data:$WORKDIR/data \
	--volume ~/jetson_tweaks/home/jupyter_notebooks:$WORKDIR/jupyter_notebooks \
	--volume /tmp/argus_socket:/tmp/argus_socket \
        --device /dev/video0 \
        --device /dev/video1 \
        $IMAGE:$VERSION \
	$*
