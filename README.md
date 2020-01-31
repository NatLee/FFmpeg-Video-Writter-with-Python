# FFmpeg Video Writter with Python

[![License: MIT v3](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE) [![Python 3](https://img.shields.io/badge/python-3-blue.svg)](https://www.python.org/)

## Introduction

As title, this is a video writter used to write video with **friendly** ffmpeg.

I'm angry with the fucking OpenCV because the video writter always saves only **44 bytes** video header instead of saving videos.

## Requirements

- ffmpeg-python
- opencv-python
- numpy

> OpenCV is optional and it's only used in the demo.

## Usage

### Quick Start

```python
import cv2
from FFmpegVideoWritter import FFmpegVideoWritter

ffvw = FFmpegVideoWritter('./data/test.mp4', './result/result.mp4')

while True:
    frame = ffvw.get_frame()
    if frame is not None:
        out_frame = cv2.resize(frame, None, fx=0.5, fy=0.5)
        cv2.imshow('frame', cv2.cvtColor(out_frame, cv2.COLOR_BGR2RGB))
        cv2.waitKey(1)
        ffvw.write(out_frame)
    else:
        break

ffvw.close()
# You can get gif output!
ffvw.output_to_gif('result/result.gif')
```

### Demo

You can run the DEMO with the following command.

```
python main.py
```

## Results

![Result](./result/result.mp4.gif)