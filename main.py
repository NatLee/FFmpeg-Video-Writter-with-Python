"""Example for FFmepegVideoWritter"""

from random import randint
import cv2
from FFmpegVideoWritter import FFmpegVideoWritter

if __name__ == "__main__":

    ffvw = FFmpegVideoWritter('./data/test.mp4', './result/result.mp4')

    while True:
        frame = ffvw.get_frame()
        if frame is not None:
            out_frame = cv2.resize(frame, None, fx=0.5, fy=0.5)
            h, w, _ = out_frame.shape
            out_frame = cv2.rectangle(out_frame, \
                                      (randint(0, w), randint(0, h)), \
                                      (randint(0, w), randint(0, h)), \
                                      (randint(0, 255), randint(0, 255), randint(0, 255)), \
                                      randint(1, 5)) 
            cv2.imshow('frame', cv2.cvtColor(out_frame, cv2.COLOR_BGR2RGB))
            cv2.waitKey(1)
            ffvw.write(out_frame)
        else:
            break

    ffvw.close()
    
    # You can get gif output!
    ffvw.output_to_gif('result/result.gif')