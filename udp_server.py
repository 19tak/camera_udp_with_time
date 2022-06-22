import base64
import cv2
import socket
import pickle
import numpy as np

import time
from datetime import datetime

# host = "0.0.0.0"
# host = '10.10.0.79'
host = '192.168.0.210'
# host = '10.30.18.46'
port = 5000
max_length = 65540
# max_length = 65000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((host, port))

frame_info = None
buffer = None
frame = None

print("-> waiting for connection")

while True:
    try:
        data, address = sock.recvfrom(max_length)
        
        if len(data) < 25:
            frame_info = pickle.loads(data)

            if frame_info:
                nums_of_packs = frame_info["packs"]
                # buffer_size = frame_info["buffer_size"]
                # print("Number of packs:",nums_of_packs)
                for i in range(nums_of_packs):
                    data, address = sock.recvfrom(max_length)
                    if i == 0:
                        buffer = data
                    # elif i >= nums_of_packs -3:
                    #     pass
                    else:
                        buffer += data

                # stime, address = sock.recvfrom(max_length)
                stime, address = sock.recvfrom(26)

                # frame = np.frombuffer(buffer, dtype=np.uint8)
                frame = np.frombuffer(base64.b64decode(buffer), np.uint8)
                frame = frame.reshape(frame.shape[0], 1)

                frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
                # frame = cv2.flip(frame, 1)

                try:
                    stime2 = stime.decode('utf-8')
                    stimet = datetime.strptime(stime2,'%Y-%m-%d %H:%M:%S.%f')
                    dtime =  datetime.utcnow() - stimet
                    # print('send time: ' + stime.decode('utf-8'))
                    # print('receive time: ' + datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f'))
                    # print('test :' + str(dtime))
                    text = 'time difference : ' + str(dtime)
                    org = (50,100)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(frame,text,org,font,1,(0,0,0),2)
                except Exception as e:
                    print(e)
                    pass
                
                if frame is not None and type(frame) == np.ndarray:
                    cv2.imshow("Stream", frame)
                    if cv2.waitKey(1) == 27:
                        break


    except Exception as e:
        print(e)
        pass
print("goodbye")
