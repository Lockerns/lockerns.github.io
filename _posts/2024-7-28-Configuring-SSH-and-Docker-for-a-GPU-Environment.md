---
title: "Configuring SSH and Docker for a GPU Environment"
date: 2024-7-28
categories: [Docker]
tags: [Linux, Docker]
---

Setting up Docker and SSH properly can significantly ease your development workflow, especially for GPU-based projects. This guide provides a detailed walkthrough for setting up SSH, running Docker without `sudo`, creating GPU-based Docker images, exporting and importing images, and configuring proxy settings for Docker.

## 1. Configuring SSH

To enable and configure SSH on your system:

```bash
# Install the OpenSSH server
sudo apt-get install openssh-server

# Start the SSH service
sudo /etc/init.d/ssh start

# Verify that the SSH service is running
ps -e | grep ssh
# Example output:
# 6212 ?        00:00:00 sshd
```

### Updating SSH Configuration

Edit the SSH configuration file to allow root login:

```bash
vim /etc/ssh/sshd_config
```

Set `PermitRootLogin` to `yes`. Then, restart the SSH service:

```bash
sudo /etc/init.d/ssh restart
```

---

## 2. Running Docker Without `sudo`

To avoid having to use `sudo` with Docker commands:

```bash
# Create the Docker group
sudo groupadd docker

# Add your user to the Docker group
sudo gpasswd -a ${USER} docker

# Restart the Docker service
sudo systemctl restart docker

# Grant read and write permissions to the Docker socket
sudo chmod a+rw /var/run/docker.sock
```

---

## 3. Creating a GPU-Based Docker Image

To create a Docker container with CUDA and cuDNN support:

```bash
# Run a GPU-enabled container with the following parameters:
nvidia-docker run -d -p <HostPort>:22 \
  --privileged=true \
  --name <ContainerName> \
  -v /data/<Directory>:/data \
  --shm-size="1g" \
  --restart=always \
  <RepositoryName>:<Tag> /usr/sbin/sshd -D
```

### Accessing and Saving the Container

1. Enter the container:
   ```bash
   docker exec -it <ContainerID> /bin/bash
   ```
2. Save the running container as a Docker image:
   ```bash
   sudo docker commit <ContainerID> <RepositoryName>:<Tag>
   ```

---

## 4. Exporting and Importing Docker Images

### Export a Docker Image

First, list your images:

```bash
docker images
```

Then, save the desired image as a `.tar` file:

```bash
docker save <ImageID> > image.tar
```

### Import a Docker Image

Use the `docker load` command to load the image:

```bash
docker load < image.tar
```

### Pushing the Image to Docker Hub

1. Log in to Docker Hub:
   ```bash
   docker login -u <Username>
   ```
2. Push the image:
   ```bash
   docker push <RepositoryName>:<Tag>
   ```

---

## 5. Setting Up a Proxy for Docker

To configure HTTP and HTTPS proxies for Docker:

1. Create the necessary directory:
   ```bash
   sudo mkdir -p /etc/systemd/system/docker.service.d
   ```

2. Create the proxy configuration file:
   ```bash
   sudo vi /etc/systemd/system/docker.service.d/http-proxy.conf
   ```

3. Add the following content to the file:

   ```
   [Service]
   Environment="HTTP_PROXY=http://127.0.0.1:7890"
   Environment="HTTPS_PROXY=http://127.0.0.1:7890"
   ```

### Apply the Changes

```bash
sudo systemctl daemon-reload
sudo systemctl restart docker
sudo systemctl show --property=Environment docker
```

---

This guide should get you up and running with SSH and Docker, optimized for GPU environments, while also making your Docker workflow more efficient. Happy coding!