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
# host = UDP_IP = '10.30.18.51'
host = UDP_IP = '10.30.18.25'
# host = '192.168.0.139'
port = 5000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
ret, frame = cap.read()

while ret:
    # compress frame
    # resize_frame = cv2.resize(frame, dsize=(480, 315), interpolation=cv2.INTER_AREA)
    # encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
    # retval, buffer = cv2.imencode('.jpg', resize_frame, encode_param)
    retval, buffer = cv2.imencode(".jpg", frame)

    if retval:
        # convert to byte array
        buffer = buffer.tobytes()
        # get size of the frame
        buffer_size = len(buffer)

        num_of_packs = 1
        if buffer_size > max_length:
            num_of_packs = math.ceil(buffer_size/max_length)

        frame_info = {"packs":num_of_packs}

        # send the number of packs to be expected
        print("Number of packs:", num_of_packs)
        sock.sendto(pickle.dumps(frame_info), (host, port))

        left = 0
        right = max_length

        for i in range(num_of_packs):
            print("left:", left)
            print("right:", right)

            # truncate data to send
            data = buffer[left:right]
            # d = np.array(buffer)
            # stringData = base64.b64encode(d)
            # data = stringData[left:right]
            left = right
            right += max_length

            # send the frames accordingly
            sock.sendto(data, (host, port))

        stime = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
        sock.sendto(stime.encode('utf-8'), (host, port))
        # print(stime)
    
    ret, frame = cap.read()

print("done")
