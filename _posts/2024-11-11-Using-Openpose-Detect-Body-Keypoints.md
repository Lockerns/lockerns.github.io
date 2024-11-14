---
title: "Using Openpose Detect Body Keypoints"
date: 2024-11-11
categories: [For 311]
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

In this command:
- `--image_dir` specifies the directory containing the input images (input_images).
- `--write_json` saves the keypoint data in JSON format to the output_jsons directory.
- `--write_images` stores the rendered images with pose annotations in the output_images directory.

Once the command finishes executing, you’ll find the rendered images and keypoint data in the `output_images` and `output_jsons` directories, respectively.

![alt text](images/2024-11-11-openpose/image-1.png)

![alt text](images/2024-11-11-openpose/image-2.png)

## 4. Processing Video with OpenPose

To process a video using OpenPose, you can use the following command:

```powershell
.\bin\OpenPoseDemo.exe `
--video input_videos\1.avi `
--write_video output_videos\1_rendered.avi `
--write_video_fps 30 `
--write_json output_jsons
```

In this command:
- `--video` specifies the input video file.
- `--write_video` defines the output file for the processed video.
- `--write_video_fps` sets the frame rate for the output video.
- `--write_json` enables saving pose data in JSON format for each frame, which will be stored in the `output_jsons` directory.

### Handling MP4 Files

Note that MP4 files are not supported natively on Windows with OpenPose. To convert an MP4 video to the required AVI format, you can use `ffmpeg` with the following command:

```bash
ffmpeg -i 1.mp4 -c:v copy -c:a copy 1.avi
```

This command copies the video and audio streams from the MP4 file to an AVI container without re-encoding, preserving the quality of the original video.

Source code and models: [CMU Perceptual Computing Lab OpenPose GitHub](https://github.com/CMU-Perceptual-Computing-Lab/openpose)