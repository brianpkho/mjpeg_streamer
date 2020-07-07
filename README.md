# MJEP Streamer

A simple MJPEG streamer created by Flask. The goal of this is to create a MJPEG Streamer for Octoprint to allow a laptop to monitor 3d-printing.

# Installation

```
pip install -r requirements.txt
```

# Run

To test it locally:
```
python server.py
```

To run it locally:
```
./start.sh
```

To access the stream server: `localhost:5001/stream`

To access the snap stream: `localhost:5001/snap`
