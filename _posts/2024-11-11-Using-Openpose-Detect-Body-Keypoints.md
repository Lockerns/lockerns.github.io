---
title: "Using Openpose Detect Body Keypoints"
date: 2024-11-11
categories: [Deep learning]
tags: [Deep learning, Openpose]
---

In this post, I’ll explain how to use OpenPose to batch-detect body keypoints from images and save the results as JSON files.

## 1. Download the OpenPose-with-Models-Windows Package

First, download the OpenPose-with-Models-Windows package from [Baidu Netdisk](https://pan.baidu.com/s/1SmtO4P27pndMEs4vvb5dfw) with the extraction code `5gb9`. Once downloaded, extract the package to any folder with a simple English path.

## 2. Import Your Dataset

Next, copy your dataset into the `openpose\input_images` folder.

![Dataset Location](images/2024-11-11-openpose/image.png)

## 3. Run the Program Using PowerShell

Open the folder you just extracted in a PowerShell terminal and run the following command:

```powershell
cd D:\temp\openpose

.\bin\04_keypoints_from_images.exe `
--image_dir input_images `
--write_json output_jsons `
--write_images output_images
```

Once the command finishes executing, you’ll find the rendered images and keypoint data in the `output_images` and `output_jsons` directories, respectively.

![alt text](images/2024-11-11-openpose/image-1.png)

![alt text](images/2024-11-11-openpose/image-2.png)

Source code and models: [CMU Perceptual Computing Lab OpenPose GitHub](https://github.com/CMU-Perceptual-Computing-Lab/openpose)