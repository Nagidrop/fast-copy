# fast-copy
Python script for fast parallel copying of files between two locations, originally written by [ikonikon](https://github.com/ikonikon "Ikonikon's GitHub Profile")

Initially developed for use with Google Colab notebooks, where the copying on numerous small files can take a long time. This script achieves >50X speed improvement.

## How to use
```
python fast-copy.py source destination
```
where `source` is the source folder and `destination` is the destination folder.

## Differences from this fork compared to the original

* Optimize imports to avoid using dots
* Use list comprehension for file list creation
* Omit the string 'format' in code line that prints '... copy daemons started'
* Lower number of threads from 16 -> 14

## Little performance benchmark

### Config: 
* 5 runs on Asus Zenbook UX433: i5-8265U 78mV undervolt, frequency locks (1 core 3.4 GHz, 2 core 3.1 GHz, 3-4 cores 2.6 GHz), W&D SN520 256GB SSD
* 1 minute cooldown between each run
* Only Command Prompt (cmd), NotePad, File Explorer are opened
* Copy a folder with 117,491 text files (.txt), total size of 31.3 MB

### Results (each run separated by hyphens): 
* Original script:&emsp;&nbsp;1:05 (65s) - 1:03 (63s) - 1:05 (65s) - 1:05 (65s) - 1:06 (66s) (Average: 64.8s each run)
* My forked script: 1:00 (60s) - 1:01 (61s) - 0:59 (59s) - 1:01 (65s) - 0:59 (59s) (Average: 60s each run - faster than roughly 7.4%)
