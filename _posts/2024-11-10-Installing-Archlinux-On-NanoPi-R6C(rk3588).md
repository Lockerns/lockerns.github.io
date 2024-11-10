---
title: "Installing Arch Linux on NanoPi R6C (rk3588)"
date: 2024-11-10
categories: [Arch Linux, NanoPi]
tags: [Linux, Arch Linux, NanoPi, rk3588]
---

My rk3588-based NanoPi R6C board does not have an official Arch Linux image, so I decided to attempt modifying the official Debian image to run Arch Linux. The main approach involves retaining the kernel and boot configuration from the Debian image while replacing the root filesystem with Arch Linux.

## Step One: Install Debian to eMMC

Since I need the bootloader and kernel from the official image, I started by installing the official Debian image on the eMMC.

## Step Two: Obtain the Arch Linux Root Filesystem

Download the official Arch Linux ARM image from [here](https://archlinuxarm.org/about/downloads) and extract it as follows:

```bash
wget http://os.archlinuxarm.org/os/ArchLinuxARM-aarch64-latest.tar.gz
mkdir -p arch-rootfs
tar -xpf ArchLinuxARM-aarch64-latest.tar.gz -C arch-rootfs
```

## Step Three: Modify the Root Filesystem

To modify the root filesystem on the eMMC, boot from a TF (microSD) card and mount the rootfs partition from the eMMC.

```bash
lsblk
mount /dev/mmcblk2p8 /mnt
```

![alt text](images/2024-11-10-Installing-Archlinux-On-NanoPi-R6C(rk3588)/image.png)

Next, copy the `lib/modules` directory from the eMMC rootfs to `arch-rootfs` which contains various kernel modules, then delete all directories under `/mnt` except boot.

Afterward, copy everything from `arch-rootfs` to `/mnt`:

```bash
cp -a arch-rootfs/* /mnt
```

![alt text](images/2024-11-10-Installing-Archlinux-On-NanoPi-R6C(rk3588)/image-2.png)

To check if the setup is correct, run:

```bash
chroot /mnt /bin/bash
cat /etc/os-release
```

If the output shows Arch Linux information, the modification was successful. Remember to reset the root password and enable SSH root login before exiting the TF card environment.

## Conclusion

After testing, Arch Linux works well on my NanoPi R6C. However, there is one limitation: the Media Process Platform (MPP) module is not available. I will need to compile it manually from the [source code](https://github.com/rockchip-linux/mpp.git).
