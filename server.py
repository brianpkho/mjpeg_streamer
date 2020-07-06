from flask import Flask, Response
# from kafka import Kafka
import cv2
import io

cam = cv2.VideoCapture(0)
# Settings to smooth camera
cam.set(cv2.CAP_PROP_FPS, 60)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
app = Flask(__name__)


def show_webcam(mirror=False):
    # Kafka for future implementations
    # kafka = Kafka()
    while True:
        ret_val, img = cam.read()
        if mirror: 
            img = cv2.flip(img, 1)
        retval, buffer = cv2.imencode('.jpg', img)
        io_buf = io.BytesIO(buffer)
        # kafka.send_kafka_message(io_buf.getvalue(), 'test')
        yield (b'--jpgboundary\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + io_buf.read() + b'\r\n')


@app.route('/')
def video_feed():
    return Response(
        show_webcam(mirror=True),
        mimetype='multipart/x-mixed-replace; boundary=--jpgboundary'
    )

if __name__ == '__main__':
    app.run(port=5001, debug=True)