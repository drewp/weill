from pathlib import Path

import numpy

# datum.hpp says: 3x4 camera matrix of the camera (equivalent to cameraIntrinsics * cameraExtrinsics).
cameraMatrices = [
    numpy.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]],
                dtype=numpy.double),
    numpy.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]],
                dtype=numpy.double),
    numpy.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]],
                dtype=numpy.double),
]
params = {
    "model_folder": "/openpose/models",
    '3d': '1',
    'number_people_max': '1',
    'disable_multi_thread': '1',
    'model_pose': 'COCO',
    'net_resolution': '160x80',
    # 'net_resolution':'320x160',
    # 'num_gpu': '1',
}

videoPaths = [
    '/data/150821_dance1/vid0.mp4',
    '/data/150821_dance1/vid1.mp4',
    '/data/150821_dance1/vid3.mp4',
]

outDir = Path('/data/out')
