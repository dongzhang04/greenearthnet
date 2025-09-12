#!/usr/bin/env python3
"""Test Script
"""
from argparse import ArgumentParser
import os
os.environ["CUDA_VISIBLE_DEVICES"] = ""

import pytorch_lightning as pl
from earthnet_models_pytorch.data import DATASETS
from earthnet_models_pytorch.model import MODELS
from earthnet_models_pytorch.task import SpatioTemporalTask
from earthnet_models_pytorch.utils import parse_setting
from pytorch_lightning.callbacks import TQDMProgressBar


def test_model(setting_dict: dict, checkpoint: str):
    print("inside test")

    # Data
    data_args = [
        "--{}={}".format(key, value) for key, value in setting_dict["Data"].items()
    ]
    data_parser = ArgumentParser()
    data_parser = DATASETS[setting_dict["Setting"]].add_data_specific_args(data_parser)
    data_params = data_parser.parse_args(data_args)
    dm = DATASETS[setting_dict["Setting"]](data_params)

    print("loaded dataset")

    # Model
    model_args = [
        "--{}={}".format(key, value) for key, value in setting_dict["Model"].items()
    ]
    model_parser = ArgumentParser()
    model_parser = MODELS[setting_dict["Architecture"]].add_model_specific_args(
        model_parser
    )
    model_params = model_parser.parse_args(model_args)
    model = MODELS[setting_dict["Architecture"]](model_params)

    print("loaded model")

    # Task
    task_args = [
        "--{}={}".format(key, value) for key, value in setting_dict["Task"].items()
    ]
    task_parser = ArgumentParser()
    task_parser = SpatioTemporalTask.add_task_specific_args(task_parser)
    task_params = task_parser.parse_args(task_args)
    task = SpatioTemporalTask(model=model, hparams=task_params)

    if checkpoint != "None":
        task.load_from_checkpoint(
            checkpoint_path=checkpoint,
            context_length=setting_dict["Task"]["context_length"],
            target_length=setting_dict["Task"]["target_length"],
            model=model,
            hparams=task_params,
        )

    print("loaded task")
    # Trainer

    trainer_dict = setting_dict["Trainer"]
    trainer_dict["logger"] = False

    print(trainer_dict)

    trainer = pl.Trainer(callbacks=TQDMProgressBar(refresh_rate=10), **trainer_dict)

    print("loaded trainer")

    dm.setup("test")

    print("Checking dataloaders...")
    test_dl = dm.test_dataloader()
    print("Test loader batches:", len(test_dl))

    print("starting task")

    trainer.test(model=task, datamodule=dm, ckpt_path=None)

    print("finished task")



if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "setting",
        type=str,
        metavar="path/to/setting.yaml",
        help="yaml with all settings",
    )
    parser.add_argument(
        "checkpoint", type=str, metavar="path/to/checkpoint", help="checkpoint file"
    )
    parser.add_argument(
        "--track",
        type=str,
        metavar="iid|ood|ex|sea",
        default="ood-t_chopped",
        help="which track to test: either iid, ood, ex or sea",
    )
    parser.add_argument(
        "--pred_dir",
        type=str,
        default="preds/",
        metavar="path/to/prediction/dir",
        help="Path where to save predictions",
    )
    parser.add_argument(
        "--data_dir",
        type=str,
        default="data/greenearthnet/",
        metavar="path/to/dataset",
        help="Path where dataset is located",
    )
    parser.add_argument(
        "--gpus",
        type=int,
        metavar="n gpus",
        default=1,
        help="how many gpus to use",
    )
    args = parser.parse_args()

    # import os

    for k, v in os.environ.items():
        if k.startswith("SLURM"):
            del os.environ[k]

    setting_dict = parse_setting(args.setting, track=args.track)

    if args.pred_dir is not None:
        setting_dict["Task"]["pred_dir"] = args.pred_dir

    if args.data_dir is not None:
        setting_dict["Data"]["base_dir"] = args.data_dir

    if "gpus" in setting_dict["Trainer"]:
        del setting_dict["Trainer"]["gpus"]
        setting_dict["Trainer"]["accelerator"] = "cpu"
        # setting_dict["Trainer"]["devices"] = 1
        setting_dict["Trainer"]["strategy"] = "auto"


    print("entering test")
    print(setting_dict)
    test_model(setting_dict, args.checkpoint)
