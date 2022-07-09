#!/bin/bash
# usage:
# set_vars.sh <num of GPUs per node>
# defaults to 1 GPU if not specified

# functionality
# renames the GPUS on nodes so NCCL recognizes them, and
#sets environment variables to have NCCL work properly and output debugging logs


echo "Im on $(hostname)"

# set NCCL to use ip-over-infiniband rather than default RoCE, since our infiniband does not have RoCE
export NCCL_IB_DISABLE=1

#used for debugging, helps print which nodes are used in code
export NCCL_DEBUG=INFO

#set CUDA_VISIBLE_DEVICES to ints to let the other nodes use the GPUS when they are activated by mpi

#GPU_LIST=0

#for ((i=1; i<=($1-1); i++));
#do
#  GPU_LIST=$GPU_LIST,$i
#done

#echo "numbers of GPUs used: $GPU_LIST"
#export CUDA_VISIBLE_DEVICES=$GPU_LIST

#set CUDA_VISIBLE_DEVICES on other nodes
#NODES=($( cat $PBS_NODEFILE | sort | uniq ))
#NUM_OF_NODES=${#NODES[@]}

#for node in ${NODES[@]}
#do
#  if [[ $node != $(eval hostname) ]]  
#  then
#    ssh $node echo "Im on $node"; export CUDA_VISIBLE_DEVICES=$GPU_LIST
#  fi
#done