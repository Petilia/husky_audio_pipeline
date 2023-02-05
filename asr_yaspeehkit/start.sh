#!/bin/bash

cd "$(dirname "$0")"

workspace_dir=$PWD

desktop_start() {
    xhost +local:
    docker run -it -d --rm \
        --gpus all \
        --ipc host \
        --network host \
        --env="DISPLAY" \
        --env="QT_X11_NO_MITSHM=1" \
        --privileged \
        --name asr_speechkit \
        --device /dev/snd \
        --group-add=audio \
        -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
        -v $workspace_dir/:/home/appuser/src:rw \
        ${ARCH}/asr_speechkit:latest
    xhost -
}


main () {
    ARCH="$(uname -m)"
    desktop_start;
}

main;