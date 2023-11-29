import cv2
import requests
import numpy as np
import matplotlib.pyplot as plt

# Replace 'your_video_url' with the actual URL of the MJPEG stream
video_url = 'http://10.0.0.26:8080/video_feed'

while True:
    response = requests.get(video_url, stream=True)
    print(response.status_code)

    if response.status_code == 200:
        bytes = bytes()
        for chunk in response.iter_content(chunk_size=1024):
            bytes += chunk
            a = bytes.find(b'\xff\xd8')
            b = bytes.find(b'\xff\xd9')
            if a != -1 and b != -1:
                jpg = bytes[a:b+2]
                bytes = bytes[b+2:]
                frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                print("Received a frame")
                plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                plt.show()

    # Press 'q' to exit the loop
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

