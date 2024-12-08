---
title: "Performance Comparison: WSL2 vs Windows Native with MSVC, MinGW, and Python"
date: 2024-12-08
categories: [Programming]
tags: [Win, Wsl, C++, Python]
---

## Introduction

As developers increasingly embrace cross-platform workflows, understanding the performance characteristics of different development environments becomes crucial. In this experiment, we compare the execution times of a set of CPU-intensive and I/O-intensive benchmarks across multiple scenarios:

- **WSL2 with g++ on ext4** (Linux filesystem)
- **WSL2 with g++ on NTFS** (mounted Windows filesystem)
- **Windows native with MinGW (g++)**
- **Windows native with MSVC (cl)**
- **WSL2 with Python**
- **Windows with Python**

The tests include:

1. **CPU-Intensive Tasks**: 
   - Prime sieve up to 10 million.
   - 1000x1000 matrix multiplication (or 500x500 for Python).
2. **I/O Tests**:
   - Reading a 1,000,000-line file.
   - Writing a 200,000-line file.

This setup provides a clear picture of both raw computation and I/O handling in each environment.

## Summary of Results

Below is a representative set of results extracted from multiple runs. Note that the times may vary slightly between individual runs, so the values shown are approximate mid-range observations based on the provided logs.

**C++ Results (Prime and Matrix tests use 10M prime limit and 1000x1000 matrix)**

| Environment         | Prime Sieve (s) | Matrix Mul (s) | Read 1,000,000 Lines (s)         | Write 200,000 Lines (s) |
| ------------------- | --------------- | -------------- | -------------------------------- | ----------------------- |
| WSL2 g++ (ext4)     | ~0.03           | ~0.48          | ~0.01                            | ~0.009-0.01             |
| WSL2 g++ (NTFS)     | ~0.03           | ~0.48          | ~0.19-0.46 (avg ~0.25+)          | ~0.07-0.09              |
| Windows MinGW (g++) | ~0.027-0.028    | ~0.48-0.49     | ~0.02                            | ~0.016                  |
| Windows MSVC (cl)*  | ~0.016-0.017    | ~0.46-0.50     | ~0.00011-0.00019 (avg ~0.00014+) | ~0.044                  |

**Python Results (Prime and Matrix tests use 1,000,000 prime limit and 500x500 matrix)**

| Environment    | Prime Sieve (s) | Matrix Mul (500x500) (s) | Read 1,000,000 Lines (s) | Write 200,000 Lines (s) |
| -------------- | --------------- | ------------------------ | ------------------------ | ----------------------- |
| WSL2 Python    | ~0.03-0.04      | ~5.4-5.6                 | ~0.03                    | ~0.02-0.03              |
| Windows Python | ~0.05           | ~6.1-6.2                 | ~0.06-0.07               | ~0.09                   |

## Analysis and Explanations

1. **CPU-Bound Tasks**:  
   - **MSVC** often shows the fastest prime sieve times (~0.016-0.017s), suggesting very effective compiler optimizations.  
   - **WSL2 (g++) and MinGW** show similar prime and matrix performance, around ~0.03s for prime sieve and ~0.48s for matrix multiplication. This indicates that both environments can produce well-optimized native code.
   - **Python** is significantly slower for CPU-intensive tasks, taking ~5.5s for the 500x500 matrix multiplication compared to ~0.48s in C++ due to its interpreted overhead.

2. **I/O Performance**:
   - **WSL2 ext4**: Very fast I/O with ~0.01s reads and ~0.009-0.01s writes.
   - **WSL2 NTFS**: Noticeably slower. Reads may take up to half a second, and writes ~0.07-0.09s. The overhead of crossing subsystem boundaries into NTFS is significant.
   - **Windows MinGW**: Good I/O performance (~0.02s read and ~0.016s write), not as fast as WSL2 ext4 but still efficient.
   - **Windows MSVC**: Writes are around 0.044s, slower than MinGW’s ~0.016s writes. Reads are impressively fast, averaging ~0.00014s, which is significantly faster than all other environments. This suggests that MSVC benefits from highly optimized file handling for reads, likely due to differences in runtime libraries or caching mechanisms. However, the slower write times indicate that MinGW might handle certain output operations more efficiently in this test scenario.
   - **Python**: Faster on WSL2 (~0.03s read, ~0.02-0.03s write) than on Windows (~0.06-0.07s read, ~0.09s write), likely due to differences in system call overhead and environment optimizations.

3. **Filesystem and Interoperability Layers**:  
   The data underscores that when using WSL2, placing files on the native ext4 filesystem yields much better performance than accessing them through an NTFS mount. For disk-heavy tasks, this can be a deciding factor.

4. **Interpreted vs. Compiled**:
   Python’s slower performance for CPU tasks is expected. However, Python still benefits from WSL2’s efficient file I/O when working on ext4.

## Conclusions

- **CPU-bound tasks**: Both MSVC and g++ (WSL2 or MinGW) deliver strong performance. MSVC can have a slight edge in prime computation, but these differences are small.
- **I/O-bound tasks**: WSL2 ext4 stands out as incredibly fast for I/O. Using WSL2 with NTFS, however, introduces significant overhead.
- **Python**: Interpreted overhead is visible in CPU-bound operations. Still, Python on WSL2 ext4 outperforms Python on Windows in I/O operations.

**Recommendations**:
- For maximum CPU performance in C++, MSVC and MinGW on Windows or g++ on WSL2 ext4 are all good choices.  
- For maximum I/O performance under WSL2, store files on the ext4 filesystem rather than NTFS.  
- For Python, prefer WSL2 if you need slightly better performance, especially for I/O-bound tasks.

This analysis can guide developers in choosing the right environment and filesystem strategy to optimize build and runtime performance.