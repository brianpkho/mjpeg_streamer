from flask import Flask, Response, make_response
# from kafka import Kafka
import cv2
import io
import base64

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


@app.route('/stream')
def video_feed():
    return Response(
        show_webcam(mirror=True),
        mimetype='multipart/x-mixed-replace; boundary=--jpgboundary'
    )

@app.route('/snap')
def snap_feed(mirror=True):
    
    ret_val, img = cam.read()
    if mirror: 
        img = cv2.flip(img, 1)
    retval, buffer = cv2.imencode('.jpg', img)
    jpg_as_text = base64.b64encode(buffer)
    response = make_response(buffer.tobytes())
    response.headers['Content-Type'] = 'image/jpeg'
    # kafka = Kafka()
    # kafka.send_kafka_message(jpg_as_text, 'test')
    return response

if __name__ == '__main__':
    app.run(port=5001, debug=True)