build:
	docker build -t openpose .

RUN=docker run \
	  -it \
	  --rm \
	  --gpus all \
	  --device /dev/video0 \
	  --device /dev/nvidia0 \
	  --device /dev/nvidia-modeset  \
	  --device /dev/nvidia-uvm \
	  --device /dev/nvidia-uvm-tools \
	  --device /dev/nvidiactl \
	  --ipc=host \
	  --net=host \
	  -e DISPLAY=$(DISPLAY) \
	  -e XAUTHORITY=/root/.Xauthority \
	  -v /tmp/.X11-unix:/tmp/.X11-unix \
	  -v $(PWD):/data \
	  -v $(XAUTHORITY):/root/.Xauthority \
	  openpose

shell:
	$(RUN) zsh

run_webcam_demo:
	$(RUN) /openpose/build/examples/openpose/openpose.bin --hand --net_resolution 160x80 -disable_multi_thread 

run_py_tut_01:
	$(RUN) zsh -c 'cd /openpose/build/examples/tutorial_api_python; python3 01_body_from_image.py'

run_analyze:
	$(RUN) python3 /data/analyze.py