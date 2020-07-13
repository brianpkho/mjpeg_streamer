import multiprocessing

bind = "0.0.0.0:5001" #Address and port for computer
timeout = 10000000 # To keep the camera alive since we're in a while loop
workers = multiprocessing.cpu_count() * 2 + 1 #handle multiple clients