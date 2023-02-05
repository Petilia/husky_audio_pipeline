#!/bin/bash

docker exec --user "docker_current" -it vad_pyannote \
    /bin/bash -c "source /opt/ros/noetic/setup.bash; cd /home/docker_current; /bin/bash"
        
