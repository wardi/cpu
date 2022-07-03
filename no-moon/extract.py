#!/usr/bin/env python3
import cv2
import gzip
import sys

OUT_W = 5 * 14 + 13  # pixels * columns + pixel spaces in between
OUT_H = 8 * 4 + 3  # pixels * rows + pixel spaces in between

# based on window.png video overlay
INPUT_X = 256
INPUT_Y = 256
TRIM_TOP = 110
TRIM_LEFT = 85

video = cv2.VideoCapture(sys.argv[1])

with gzip.open(sys.argv[2], 'wb') as f:
    while True:
        ret, frame = video.read()
        if not ret:
            break

        ret, frame = cv2.threshold(frame, 127, 255, cv2.THRESH_BINARY_INV)

        # convert [0, 0, 0] / [255, 255, 255] pixels into 0s / 1s
        #import ipdb; ipdb.set_trace()
        bits = frame.reshape(INPUT_X * INPUT_Y * 3)[::3].reshape(INPUT_X, INPUT_Y) // 255

        for top in range(TRIM_TOP, TRIM_TOP + OUT_H, 9):
            for left in range(TRIM_LEFT, TRIM_LEFT + OUT_W, 6):
                for y in range(8):
                    b = bits[top+y][left:left+5]
                    f.write(bytes([b[0]*16+b[1]*8+b[2]*4+b[3]*2+b[4]]))
