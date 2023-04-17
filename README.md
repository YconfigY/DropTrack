# DropTrack
The official fine-tuning implementation of DropTrack for the **CVPR 2023** paper [_DropMAE: Masked Autoencoders with Spatial-Attention Dropout for Tracking Tasks_](https://arxiv.org/pdf/2304.00571.pdf).

[[Models](https://drive.google.com/drive/folders/1ttafo0O5S9DXK2PX0YqPvPrQ-HWJjhSy?usp=sharing)][[Raw Results](https://drive.google.com/drive/folders/1TYU5flzZA1ap2SLdzlGRQDbObwMxCiaR?usp=sharing)][[Training logs](https://drive.google.com/drive/folders/1LUsGf9JRV0k-R3TA7UFBRlcic22M4uBp?usp=sharing)]


## :sunny: Highlights

#### * Thanks for the great [_OSTrack_](https://github.com/botaoye/OSTrack) library, which helps us to quickly implement the [_DropMAE_](https://github.com/jimmy-dq/DropMAE) VOT fine-tuning. The repository mainly follows the OSTrack repository.

#### * The OSTrack w/ our [_DropMAE_](https://github.com/jimmy-dq/DropMAE) pre-trained models can achieve state-of-the-art perforamnce on existing popular tracking benchmarks.

| Tracker     | GOT-10K (AO) | LaSOT (AUC) | LaSOT (AUC) | TrackingNet (AUC) | TNL2K(AUC) |
|:-----------:|:------------:|:-----------:|:-----------:|:-----------------:|:-----------:|
| DropTrack-K700-ViTBase | 75.9         | 71.8        | 52.7        | 84.1              | 56.9        |


### :star2: Training Speed
Our DropTrack has the same training procedure and nearly the same model parameters (i.e., except for using two frame identity embeddings) w/ OSTrack, so the training speed is consistent w/ OSTrack. We use 4 A100 GPUs w/ a total batch size of 128, which costs about ~6 hours (100 Epochs) for training on GOT-10k.

## Install the environment
**Option1**: Use the Anaconda (CUDA 10.2)
```
conda create -n ostrack python=3.8
conda activate ostrack
bash install.sh
```

**Option2**: Use the Anaconda (CUDA 11.3)
```
conda env create -f ostrack_cuda113_env.yaml
```

**Option3**: Use the docker file

We provide the full docker file here.


## Set project paths
Run the following command to set paths for this project
```
python tracking/create_default_local_file.py --workspace_dir . --data_dir ./data --save_dir ./output
```
After running this command, you can also modify paths by editing these two files
```
lib/train/admin/local.py  # paths about training
lib/test/evaluation/local.py  # paths about testing
```

## Data Preparation
Put the tracking datasets in ./data. It should look like:
   ```
   ${PROJECT_ROOT}
    -- data
        -- lasot
            |-- airplane
            |-- basketball
            |-- bear
            ...
        -- got10k
            |-- test
            |-- train
            |-- val
        -- coco
            |-- annotations
            |-- images
        -- trackingnet
            |-- TRAIN_0
            |-- TRAIN_1
            ...
            |-- TRAIN_11
            |-- TEST
   ```


## Training
Download pre-trained [MAE ViT-Base weights](https://dl.fbaipublicfiles.com/mae/pretrain/mae_pretrain_vit_base.pth) and put it under `$PROJECT_ROOT$/pretrained_models` (different pretrained models can also be used, see [MAE](https://github.com/facebookresearch/mae) for more details).

```
python tracking/train.py --script ostrack --config vitb_256_mae_ce_32x4_ep300 --save_dir ./output --mode multiple --nproc_per_node 4 --use_wandb 1
```

Replace `--config` with the desired model config under `experiments/ostrack`. We use [wandb](https://github.com/wandb/client) to record detailed training logs, in case you don't want to use wandb, set `--use_wandb 0`.


## Evaluation
Download the model weights from [Google Drive](https://drive.google.com/drive/folders/1PS4inLS8bWNCecpYZ0W2fE5-A04DvTcd?usp=sharing) 

Put the downloaded weights on `$PROJECT_ROOT$/output/checkpoints/train/ostrack`

Change the corresponding values of `lib/test/evaluation/local.py` to the actual benchmark saving paths

Some testing examples:
- LaSOT or other off-line evaluated benchmarks (modify `--dataset` correspondingly)
```
python tracking/test.py ostrack vitb_384_mae_ce_32x4_ep300 --dataset lasot --threads 16 --num_gpus 4
python tracking/analysis_results.py # need to modify tracker configs and names
```
- GOT10K-test
```
python tracking/test.py ostrack vitb_384_mae_ce_32x4_got10k_ep100 --dataset got10k_test --threads 16 --num_gpus 4
python lib/test/utils/transform_got10k.py --tracker_name ostrack --cfg_name vitb_384_mae_ce_32x4_got10k_ep100
```
- TrackingNet
```
python tracking/test.py ostrack vitb_384_mae_ce_32x4_ep300 --dataset trackingnet --threads 16 --num_gpus 4
python lib/test/utils/transform_trackingnet.py --tracker_name ostrack --cfg_name vitb_384_mae_ce_32x4_ep300
```

## Visualization or Debug 
[Visdom](https://github.com/fossasia/visdom) is used for visualization. 
1. Alive visdom in the sever by running `visdom`:

2. Simply set `--debug 1` during inference for visualization, e.g.:
```
python tracking/test.py ostrack ostrack384_elimination_ep300 --dataset vot22 --threads 1 --num_gpus 1 --debug 1
```
3. Open `http://localhost:8097` in your browser (remember to change the ip address and port according to the actual situation).

4. Then you can visualize the candidate elimination process.

![ECE_vis](https://github.com/botaoye/OSTrack/blob/main/assets/vis.png)


## Test FLOPs, and Speed
*Note:* The speeds reported in our paper were tested on a single RTX2080Ti GPU.

```
# Profiling vitb_256_mae_ce_32x4_ep300
python tracking/profile_model.py --script ostrack --config vitb_256_mae_ce_32x4_ep300
# Profiling vitb_384_mae_ce_32x4_ep300
python tracking/profile_model.py --script ostrack --config vitb_384_mae_ce_32x4_ep300
```


## Acknowledgments
* Thanks for the [STARK](https://github.com/researchmm/Stark) and [PyTracking](https://github.com/visionml/pytracking) library, which helps us to quickly implement our ideas.
* We use the implementation of the ViT from the [Timm](https://github.com/rwightman/pytorch-image-models) repo.  


## Citation
If our work is useful for your research, please consider cite:

```
@article{ye2022ostrack,
  title={Joint Feature Learning and Relation Modeling for Tracking: A One-Stream Framework},
  author={Ye, Botao and Chang, Hong and Ma, Bingpeng and Shan, Shiguang and Chen, Xilin},
  journal={arXiv preprint arXiv:2203.11991},
  year={2022}
}
```
