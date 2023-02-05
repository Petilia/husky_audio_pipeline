FROM python:3.8

COPY . .
RUN pip install -r requirements.txt

# # create a non-root user
# ARG USER=appuser
# ARG UID=1000
# ARG GID=1000
# # default password
# ARG PW=user
# RUN useradd -m ${USER} --uid=${UID} && echo "${USER}:${PW}" | chpasswd && adduser ${USER} sudo
# RUN chown -R ${UID}:${GID} /home
# USER ${UID}:${GID}

# WORKDIR /home/${USER}c