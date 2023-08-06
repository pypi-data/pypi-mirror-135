import os
from typing import Union, List
import math
import numpy as np

from code_loader.contract.enums import DatasetInputType, DatasetOutputType, DatasetMetadataType
from code_loader.contract.datasetclasses import SubsetResponse
from code_loader import dataset_binder
from google.cloud import storage
from google.cloud.storage import Bucket
from google.oauth2 import service_account

crop_size = 128


def _connect_to_gcs() -> Bucket:
    auth_secret = os.environ['AUTH_SECRET']
    if type(auth_secret) is dict:
        # getting credentials from dictionary account info
        credentials = service_account.Credentials.from_service_account_info(auth_secret)
    else:
        # getting credentials from path
        credentials = service_account.Credentials.from_service_account_file(auth_secret)
    project = credentials.project_id

    gcs_client = storage.Client(project=project, credentials=credentials)

    bucket_name = 'YOUR_BUCKET_NAME'

    return gcs_client.bucket(bucket_name)


def subset_func() -> List[SubsetResponse]:
    bucket = _connect_to_gcs()

    base_path = 'ISBICellSegmentation/'
    train_path = f'{base_path}train-volume2.npy'

    blob = bucket.blob(train_path)
    blob.download_to_filename(train_path)
    scans = np.load(train_path) / 255

    train_path = f'{base_path}train-labels2.npy'
    blob.download_to_filename(train_path)
    masks = np.load(train_path) / 255
    image_size = scans.shape[-1]

    val_split = int(len(scans) * 0.8)
    train_scans = scans[:val_split]
    val_scans = scans[val_split:]
    train_masks = masks[:val_split]
    val_masks = masks[val_split:]

    crop_per_image = int(image_size / crop_size) ** 2
    train_length = crop_per_image * len(train_scans)
    val_length = crop_per_image * len(val_scans)
    crop_per_image = int(image_size / crop_size) ** 2

    train = SubsetResponse(length=train_length, data={'images': train_scans, 'masks': train_masks,
                                                      'shape': image_size, 'crop_per_image': crop_per_image})
    val = SubsetResponse(length=val_length, data={'images': val_scans, 'masks': val_masks, 'shape': image_size,
                                                  'crop_per_image': crop_per_image})
    response = [train, val]
    return response


def input_encoder_1(idx: int, subset: SubsetResponse) -> np.ndarray:
    crop_per_image = subset.data['crop_per_image']
    image_idx = int(idx / crop_per_image)
    image = subset.data['images'][image_idx]
    img_slice = idx - (image_idx * crop_per_image)
    crop = np.split(image, crop_per_image)[img_slice]

    axis_slice = int(math.sqrt(crop_per_image))

    hi = int(img_slice / axis_slice)
    vi = int(img_slice % axis_slice)
    crop = np.hsplit(np.vsplit(image, axis_slice)[hi], axis_slice)[vi]

    return crop[..., np.newaxis]


def output_encoder_1(idx: int, subset: Union[SubsetResponse, list]) -> np.ndarray:
    crop_per_image = subset.data['crop_per_image']
    image_idx = int(idx / crop_per_image)
    image = subset.data['masks'][image_idx]
    img_slice = idx - (image_idx * crop_per_image)
    crop = np.split(image, crop_per_image)[img_slice]

    axis_slice = int(math.sqrt(crop_per_image))

    hi = int(img_slice / axis_slice)
    vi = int(img_slice % axis_slice)
    crop = np.hsplit(np.vsplit(image, axis_slice)[hi], axis_slice)[vi]

    return crop[..., np.newaxis]


def metadata_encoder_1(idx: int, subset: Union[SubsetResponse, list]) -> np.ndarray:
    crop_per_image = subset.data['crop_per_image']
    image_idx = int(idx / crop_per_image)
    image = subset.data['masks'][image_idx]
    img_slice = idx - (image_idx * crop_per_image)
    crop = np.split(image, crop_per_image)[img_slice]

    axis_slice = int(math.sqrt(crop_per_image))

    hi = int(img_slice / axis_slice)
    vi = int(img_slice % axis_slice)
    crop = np.hsplit(np.vsplit(image, axis_slice)[hi], axis_slice)[vi]
    return float(np.mean(crop))


def metadata_encoder_2(idx: int, subset: Union[SubsetResponse, list]) -> np.ndarray:
    crop_per_image = subset.data['crop_per_image']
    image_idx = int(idx / crop_per_image)
    image = subset.data['masks'][image_idx]
    img_slice = idx - (image_idx * crop_per_image)
    crop = np.split(image, crop_per_image)[img_slice]

    axis_slice = int(math.sqrt(crop_per_image))

    hi = int(img_slice / axis_slice)
    vi = int(img_slice % axis_slice)
    crop = np.hsplit(np.vsplit(image, axis_slice)[hi], axis_slice)[vi]
    return float(np.std(crop))


dataset_binder.set_subset(ration=1, function=subset_func, name='MicroscopeCellImages')

dataset_binder.set_input(function=input_encoder_1, subset='MicroscopeCellImages', input_type=DatasetInputType.Image,
                         name='Crops')

dataset_binder.set_ground_truth(function=output_encoder_1, subset='MicroscopeCellImages',
                                ground_truth_type=DatasetOutputType.Mask,
                                name='segments', labels=['Background', 'Cell'], masked_input='Crops')

dataset_binder.set_metadata(function=metadata_encoder_1, subset='MicroscopeCellImages',
                            metadata_type=DatasetMetadataType.float,
                            name='label_mean')
dataset_binder.set_metadata(function=metadata_encoder_2, subset='MicroscopeCellImages',
                            metadata_type=DatasetMetadataType.float,
                            name='laebl_std')
