import sys

import cv2

sys.path.append("/openpose/build/python")
from openpose import pyopenpose as op


def video_frames(path):
    cap = cv2.VideoCapture(path)
    while True:
        ok, frame = cap.read()
        if not ok:
            return
        yield frame


opWrapper = op.WrapperPython()
# Custom Params (refer to include/openpose/flags.hpp for more parameters)
opWrapper.configure({
    "model_folder": "/openpose/models",
    '3d': '1',
    'number_people_max': '1',
    'disable_multi_thread': '1',
    # 'num_gpu': '1',
    'model_pose': 'COCO',
    'net_resolution': '160x80',
})
opWrapper.start()

datum = op.Datum()
for numFrames, f1 in enumerate(video_frames('/data/vid0.mp4')):
    datum.cvInputData = f1
    opWrapper.emplaceAndPop(op.VectorDatum([datum]))

    print(f'frame {numFrames} {datum.poseKeypoints=}')
