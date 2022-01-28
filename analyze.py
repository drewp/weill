import os
import json
import sys
import time

import cv2

sys.path.append("/openpose/build/python")
from openpose import pyopenpose as op

import config


def streamVideoFrames(path):
    cap = cv2.VideoCapture(path)
    while True:
        ok, frame = cap.read()
        if not ok:
            return
        yield frame


def saveArray(path, array):
    if array is None:
        print(f'  no array to write to {path}')
        return
    with open(path, 'wt') as out:
        fmt = json.dumps(array.tolist(), indent=2)
        fmt = fmt.replace('\n      ', ' ').replace('\n    ],', ' ],\n')
        out.write(fmt)


class Openpose:
    def __init__(self, params, cameraMatrices):
        self.opWrapper = op.WrapperPython()
        # Custom Params (refer to include/openpose/flags.hpp for more parameters)
        self.opWrapper.configure(params)

        self.datums = []
        for i, cm in enumerate(cameraMatrices):
            d = op.Datum()
            d.cameraMatrix = cm
            d.subId = i
            d.subIdMax = len(cameraMatrices) - 1
            self.datums.append(d)

        self.opWrapper.start()

    def analyze(self, frameNum, images):
        for datum, image in zip(self.datums, images):
            datum.cvInputData = image
            datum.id = frameNum

        self.opWrapper.emplaceAndPop(op.VectorDatum(self.datums))
        return self.datums


def frameGroups(videoPaths):
    return enumerate(zip(*[streamVideoFrames(p) for p in videoPaths]))


def main():
    config.outDir.mkdir(exist_ok=True)
    openpose = Openpose(config.params, config.cameraMatrices)

    for frameNum, images in frameGroups(config.videoPaths):
        print(f'frame {frameNum} analyze...')
        t1 = time.time()
        datums = openpose.analyze(frameNum, images)
        print(f'  finished in {time.time()-t1:.3g} sec')
        for cam, d in enumerate(datums):
            base = f'{config.outDir}/frame-{frameNum}-cam-{cam}'
            cv2.imwrite(f'{base}-out.jpg', d.cvOutputData)
            saveArray(f'{base}-poseKeypoints.json', d.poseKeypoints)
            saveArray(f'{base}-poseKeypoints3D.json', d.poseKeypoints3D)

        if frameNum > 2:
            break


main()
