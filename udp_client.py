import cv2
import socket
import math
import pickle
import sys

import time
from datetime import datetime
import base64
import numpy as np

max_length = 65000
host = '192.168.0.210'
# host = '10.30.18.46'
# host = '10.10.0.79'
port = 5000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture(2)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
ret, frame = cap.read()
while ret:
    # resize_frame = cv2.resize(frame, dsize=(1920, 1080), interpolation=cv2.INTER_AREA)
    retval, buffer = cv2.imencode(".jpg", frame)
    # retval, buffer = cv2.imencode(".jpg", resize_frame)
    if retval:
        buffer = buffer.tobytes()
        buffer_size = len(buffer)
        # print(buffer_size)

        num_of_packs = 1
        if buffer_size > max_length:
            # num_of_packs = math.ceil(buffer_size/max_length)+4
            num_of_packs = math.ceil(buffer_size/max_length)+2
            # num_of_packs = 6

        frame_info = {"packs":num_of_packs}
        # frame_info = {"packs":num_of_packs, "buffer_size":buffer_size}
        # print("Number of packs:", num_of_packs)
        # print(len(pickle.dumps(frame_info)))
        sock.sendto(pickle.dumps(frame_info), (host, port))
        
        print("Number of Packs: ",num_of_packs,", additional bytes: ",max_length*(num_of_packs) - buffer_size)

        left = 0
        right = max_length
        for i in range(num_of_packs):
            # print("left:", left)
            # print("right:", right)

            # truncate data to send
            # data = buffer[left:right]
            d = np.array(buffer)
            stringData = base64.b64encode(d)
            data = stringData[left:right]
            left = right
            right += max_length
            # send the frames accordingly
            sock.sendto(data, (host, port))

        stime = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
        sock.sendto(stime.encode('utf-8'), (host, port))
        # print(stime)
        # print(len(stime.encode('utf-8')))
    
    ret, frame = cap.read()

print("done")
