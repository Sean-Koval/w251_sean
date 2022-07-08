# Homework 9 - Distributed training

This is a graded homework

Due: before week 10 begins

In this homework, we are focused on aspects of multi-node and multi-gpu (mnmg) model training.
The high level idea is to practice running multi-node training by adapting the code we develop in homework 5 (imagenet training from random weights) to run on two GPU nodes instead of one.

Notes:
* You will need to provision two g4dn.2xlarge instances. Each has 8 vCPUs, so you'll need to the ability (limit) to provision 16 vCPUs. 
* We recommend adding 400GB of storage space under /root so that you can comfortably work with imagenet2012 (below)
* You'll need to [re-] download imagenet2012 (we'll provide links in class again) and unpack it on each machine -- e.g. under /data/
* You'll need to demonstrate your command of [PyTorch DDP](https://pytorch.org/tutorials/beginner/dist_overview.html)
* Apply [PyTorch native AMP](https://pytorch.org/docs/stable/amp.html)
* Document your run using [Tensorboard](https://www.tensorflow.org/tensorboard) or [Weights and Biases](https://wandb.ai/home) 
* Hopefully, demonstrate that your training is ~2x faster than on a single GPU machine.

Tips:
* You could trt using g4dn.xlarge, but in our experience, they just don't have enough CPUs to keep the GPU fed, so the results will be slow.
* Ideally, you should be able to use EFS.  However, one must ensure that performance is good-- and we've seen issues.
* There is no need to train to the end (e.g. 90 epochs); it would be sufficient to run the training for 1-2 epochs, time it, and compare the results against a run on a sinle GPU instance.
* Please monitor the GPU utilization using nvidia-smi; as long as both GPUs are > 95% utilized, you are doing fine.


https://wandb.ai/quickstart/pytorch

### Steps:

1) Create and spin up the two instances within VPC
2) Clone repos onto Hive and Drone instances (g4)
3) Sign up/create account for tensoboard/wandb.ai
4) Run the notebooks in Hive and Drone instances (Hive first)
5) Try running single node instnace file (compare the two and submit output)




THIS WORKED:
```
docker run --gpus all --shm-size=2048m -it --rm --net=host -v ./data:/data -v ./w251_sean/HW9/:/workspace/w251 nvcr.io/nvidia/pytorch:21.08-py3
```
THIS ^^^^^
```
docker run --gpus all --shm-size=2048m -it --rm -v ~/data:/data nvcr.io/nvidia/pytorch:21.08-py3
```

Run this command from inside the /data folder of the g4dxn.2xlarge instance
```
Run the above docker command. Have to cd .. back to /data or cd /data to find the train and val datasets within the docker image. 

thank you Gerrit and all for sharing this.   I was stuck for a moment because I couldn’t find the /data folder once I am in the docker container.   However, you need to cd .. back to root to see the /data  because the command above is set to root/data, but when you enter your docker container (at least for me) the landing directory is /root/workspace
```

```
docker run --gpus all -it --rm -v /data:./data -p 8888:8888 nvcr.io/nvidia/pytorch:21.08-py3
```

