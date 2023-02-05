#!/bin/bash

cd "$(dirname "$0")"
# cd ..

workspace_dir=$PWD

# -v $workspace_dir/../data:/home/docker_current/data:rw \
# -v $workspace_dir/../py_files:/home/docker_current/py_files:rw \

desktop_start() {
    xhost +local:
    docker run -it -d --rm \
        --gpus all \
        --ipc host \
        --network host \
        --env="DISPLAY" \
        --env="QT_X11_NO_MITSHM=1" \
        --privileged \
        --name vad_pyannote \
        --device /dev/snd \
        --group-add=audio \
        -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
        -v $workspace_dir/../:/home/docker_current/catkin_ws/src/vad_ros1:rw \
        ${ARCH}/vad_pyannote:latest
    xhost -``
}

/usr/local/share/ca-certificates


main () {
    ARCH="$(uname -m)"

    if [ "$ARCH" = "x86_64" ]; then
        desktop_start;
    elif [ "$ARCH" = "aarch64" ]; then
        arm_start;
    fi

}

main;
