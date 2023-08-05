FROM pytorch/pytorch
RUN apt update -y && \
    apt install -y libglib2.0-0 libsm6 libxrender1 libxext6 libgl1-mesa-glx build-essential wget git
RUN mkdir -p /model_serving/module
RUN mkdir -p /model_serving/interface_class
RUN mkdir -p /mnt/model
WORKDIR /model_serving
ENV HOME=/model_serving
RUN python -m pip install --upgrade pip
RUN pip install torch==1.8.1
COPY requirements.txt /model_serving/requirements.txt
RUN pip install detectron2 -f https://dl.fbaipublicfiles.com/detectron2/wheels/cpu/torch1.8/index.html
COPY sap_computer_vision /model_serving/module/sap_computer_vision
COPY serve_models.py /model_serving/interface_class/serve_models.py
ENV MODEL_CONFIG_LIST_FILEPATH_YAML=/model_serving/model_serving.yaml
ENV PYTHONPATH="/model_serving/module:${PYTHONPATH}"
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH$:/usr/local/nvidia/lib:/usr/local/nvidia/lib64:/usr/local/cuda/lib64:/usr/local/cuda-10.0/targets/x86_64-linux/lib:/usr/local/cuda-10.2/targets/x86_64-linux/lib:/usr/local/cuda-11/targets/x86_64-linux/lib:/usr/local/cuda-11.1/targets/x86_64-linux/lib
RUN python -m pip install -r /model_serving/requirements.txt
RUN chgrp -R nogroup /model_serving && \
    chmod -R 777 /model_serving
RUN chgrp -R nogroup /tmp && \
    chmod -R 777 /tmp && \
    chmod +t /tmp
CMD python /model_serving/interface_class/serve_models.py $MODELS && cat $MODEL_CONFIG_LIST_FILEPATH_YAML && centaur
