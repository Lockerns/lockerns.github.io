---
title: "Jellyfin MacOS Subtitle Playback Error"
date: 2024-11-08
categories: [Mac]
tags: [Mac, Jellyfin]
---

## Introduction
Recently, I encountered a subtitle playback error when using Jellyfin on macOS. The issue didn’t occur on Android or Windows, so I began troubleshooting on macOS. Here’s how I identified and solved the problem.

## Problem Description
When playing media with subtitles on Jellyfin for macOS, I noticed playback errors. Initially, I suspected a font issue, so I installed the same fonts used on my Jellyfin server. Unfortunately, that didn’t resolve the problem. A friend suggested that Jellyfin burns subtitles by default, leading me to suspect hardware acceleration. After testing, I found that turning off both hardware encoding and subtitle burning could resolve the issue.

![Playback Error Screenshot](images/2024-11-8-Jellyfin-Macos-Subtitle-Error/play_back_error.jpg)

## Solution
To fix this issue, I recommend turning off subtitle burning, as software encoding is slow and inefficient. Follow these steps:

1. Open Jellyfin and go to *Settings > Subtitles > Burn Subtitles*.
2. Select *Only Image Formats (VobSub, PGS, SUB)* to improve performance.

![Settings Screenshot](images/2024-11-8-Jellyfin-Macos-Subtitle-Error/turnoff_burning_subtitles.png)

## Conclusion
This method ensures that subtitles work smoothly on macOS without compromising performance. Let me know in the comments if this solution helped or if you have other troubleshooting tips!
