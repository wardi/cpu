#!/usr/bin/env python3
import cv2
import gzip

OUT_W = 5 * 8 + 7  # pixels * columns + pixel spaces in between
OUT_H = 8 * 4 + 3  # pixels * rows + pixel spaces in between

video = cv2.VideoCapture(sys.argv[1])

with gzip.open(sys.argv[2], 'wb') as f:
    while True:
        ret, frame = video.read()
        if not ret:
            break

        frame = cv2.resize(frame, (OUT_W, OUT_H), interpolation=cv2.INTER_AREA)
        ret, frame = cv2.threshold(frame, 127, 255, cv2.THRESH_BINARY_INV)

        # convert [0, 0, 0] / [255, 255, 255] pixels into 0s / 1s
        bits = frame.reshape(OUT_H * OUT_W * 3)[::3].reshape(OUT_H, OUT_W) // 255

        for top in range(0, OUT_H, 9):
            for left in range(0, OUT_W, 6):
                for y in range(8):
                    b = bits[top+y][left:left+5]
                    f.write(bytes([b[0]*16+b[1]*8+b[2]*4+b[3]*2+b[4]]))
