from flask import Flask, Response, make_response
# from kafka import Kafka
import cv2
import io
import base64
import time

cam = cv2.VideoCapture(0)
# Settings to smooth camera
cam.set(cv2.CAP_PROP_FPS, 60)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
app = Flask(__name__)


def show_webcam():
    while True:
        ret_val, img = cam.read()
        retval, buffer = cv2.imencode('.jpg', img)
        io_buf = io.BytesIO(buffer)
        yield (b'--jpgboundary\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + io_buf.read() + b'\r\n')


@app.route('/stream')
def video_feed():
    return Response(
        show_webcam(),
        status=200,
        mimetype='multipart/x-mixed-replace; boundary=--jpgboundary'
    )

@app.route('/snap')
def snap_feed():
    ret_val, img = cam.read()
    retval, buffer = cv2.imencode('.jpg', img)
    jpg_as_text = base64.b64encode(buffer)
    response = make_response(buffer.tobytes())
    response.headers['Content-Type'] = 'image/jpeg'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True, threaded=True)