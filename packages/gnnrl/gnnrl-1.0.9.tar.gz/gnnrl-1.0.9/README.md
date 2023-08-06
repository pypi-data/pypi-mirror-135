# GNN-RL-Model-Compression
GNN-RL Compression: Topology-Aware Network Pruning using Multi-stage Graph Embedding and Reinforcement Learning

## Dependencies

Current code base is tested under following environment:

1. Python   3.8
2. PyTorch  1.8.0 (cuda 11.1)
3. torchvision 0.7.0
4. [torch-geometric](https://pytorch-geometric.readthedocs.io/en/latest/notes/installation.html#) 1.6.1

## Results on ImageNet
| Models                   | FLOPs ratio| Top1 Acc. (%) |![\delta](http://latex.codecogs.com/svg.latex?{\Delta}) Acc.| Dataset |
| ------------------------ | ------------     | ------------ |------------|------------|
| MobileNet-v1                | 40% FLOPs       | **69.50**  |**-1.40**  |ImageNet|
| MobileNet-v1                | 70% FLOPs       | **70.70**  |**-0.20**  |ImageNet|
| MobileNet-v2                | 58% FLOPs       | **70.04**  |**-1.83**  |ImageNet|
| VGG-16                | 20% FLOPs       | **70.992**   |**+0.49** |ImageNet|
| ResNet-50                | 47% FLOPs       | **74.28**   |**-1.82** |ImageNet|
| ResNet-18                | 50% FLOPs       | **68.66**   |**-1.10** |ImageNet|

