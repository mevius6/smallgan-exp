import torch
import torchvision
import torch.nn as nn

from . import BigGAN as biggan
from .AdaBIGGAN import AdaBIGGAN

# taken from https://github.com/ajbrock/BigGAN-PyTorch/issues/8
bigagn128config = {'dataset': 'I128_hdf5',
 'augment': False,
 'num_workers': 8,
 'pin_memory': True,
 'shuffle': False,
 'load_in_mem': False,
 'use_multiepoch_sampler': False,
 'model': 'BigGAN',
 'G_param': 'SN',
 'D_param': 'SN',
 'G_ch': 96,
 'D_ch': 96,
 'G_depth': 1,
 'D_depth': 1,
 'D_wide': True,
 'G_shared': True,
 'shared_dim': 128,
 'dim_z': 120,
 'z_var': 1.0,
 'hier': True,
 'cross_replica': False,
 'mybn': False,
 'G_nl': 'relu',
 'D_nl': 'relu',
 'G_attn': '64',
 'D_attn': '64',
 'norm_style': 'bn',
 'seed': 0,
 'G_init': 'ortho',
 'D_init': 'ortho',
 'skip_init': True,
 'G_lr': 5e-05,
 'D_lr': 0.0002,
 'G_B1': 0.0,
 'D_B1': 0.0,
 'G_B2': 0.999,
 'D_B2': 0.999,
 'batch_size': 64,
 'G_batch_size': 0,
 'num_G_accumulations': 1,
 'num_D_steps': 2,
 'num_D_accumulations': 1,
 'split_D': False,
 'num_epochs': 100,
 'parallel': False,
 'G_fp16': False,
 'D_fp16': False,
 'D_mixed_precision': False,
 'G_mixed_precision': False,
 'accumulate_stats': False,
 'num_standing_accumulations': 16,
 'G_eval_mode': False,
 'save_every': 2000,
 'num_save_copies': 2,
 'num_best_copies': 2,
 'which_best': 'IS',
 'no_fid': False,
 'test_every': 5000,
 'num_inception_images': 50000,
 'hashname': False,
 'base_root': '',
 'data_root': 'data',
 'weights_root': 'weights',
 'logs_root': 'logs',
 'samples_root': 'samples',
 'pbar': 'mine',
 'name_suffix': '',
 'experiment_name': '',
 'config_from_name': False,
 'ema': False,
 'ema_decay': 0.9999,
 'use_ema': False,
 'ema_start': 0,
 'adam_eps': 1e-08,
 'BN_eps': 1e-05,
 'SN_eps': 1e-08,
 'num_G_SVs': 1,
 'num_D_SVs': 1,
 'num_G_SV_itrs': 1,
 'num_D_SV_itrs': 1,
 'G_ortho': 0.0,
 'D_ortho': 0.0,
 'toggle_grads': True,
 'which_train_fn': 'GAN',
 'load_weights': '',
 'resume': False,
 'logstyle': '%3.3e',
 'log_G_spectra': False,
 'log_D_spectra': False,
 'sv_log_interval': 10,
 'sample_npz': False,
 'sample_num_npz': 50000,
 'sample_sheets': False,
 'sample_interps': False,
 'sample_sheet_folder_num': -1,
 'sample_random': False,
 'sample_trunc_curves': '',
 'sample_inception_metrics': False,
 'resolution': 128,
 'n_classes': 1000,
 'G_activation': torch.nn.modules.activation.ReLU(inplace=True),
 'D_activation': torch.nn.modules.activation.ReLU(inplace=True),
 'no_optim': True,
 'device': 'cpu'}

def setup_model(name,dataset_size,resume=None,biggan_imagenet_pretrained_model_path="./data/G_ema.pth"):
    print("model name:",name)
    if name=="biggan128-ada":
        G = biggan.Generator(**bigagn128config)
        G.load_state_dict(torch.load(biggan_imagenet_pretrained_model_path,map_location=lambda storage, loc: storage))
        model = AdaBIGGAN(G,dataset_size=dataset_size)
    else:
        print("%s (model name) is not defined"%name)
        raise NotImplementedError()

    if resume is not None:
        print("resuming trained weights from %s"%resume)
        checkpoint_dict = torch.load(resume)
        model.load_state_dict(checkpoint_dict["model"])

    return model
