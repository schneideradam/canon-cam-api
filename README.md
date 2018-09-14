# DSLR Controller - Raspberry Pi / Deb Linux

[TOC]

**DSLR Controller** is a universal interface for clients to remotely control a variety of DSLR camera's over USB.  This library relies on gphoto2 written by Jim Easterbrook (https://github.com/jim-easterbrook/python-gphoto2) and the libghoto2 binding. 



### Goals

- To allow clients written in any language to interface with a DSLR camera without need for any specific library
- Consistent messaging and triggers
- Universal system architecture through the use of docker
- MQTT messaging for continuous system status across various subscribers

### Dependencies

- Docker
- Raspbian Stretch (ARM) or Debian Linux (x64)

### Installation

```bash
sudo apt-get install docker
```

#### ENV Vars (optional)

You'll need access to the .env files. These can be built with the included encrypted files.  Run the make_env_vars script and enter the vault password. This step is optional if you don't have the vault password.  The env files merely contain mqtt creds and logging / sentry creds, but this stack can run without them.

```bash
bash make-env.sh
enter password:
```

### Run the stack

```bash
bash start.sh
```

### Testing

There are currently no automated tests but you can run the test_mqtt.py file to get a status or capture an image.

```bash
python test/test_mqtt.py capture
```



## Still being developed

### If you want a preview of the video stream

```bash
# Install the loopback utils package so we can see the camera feed on a virtual device
sudo apt-get install v4l2loopback-utils

# Install VLC to view the stream
sudo apt-get install vlc

# Setup a vitrual device to send the stream to

```
