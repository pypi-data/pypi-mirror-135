from typing import List, Tuple, Union

import os
import pathlib

import numpy as np
import tensorflow as tf
import xarray as xr
from tensorflow.python.keras.utils import conv_utils


class PatchDatasets:
    def __init__(
        self,
        dataset: Union[str, pathlib.Path, xr.Dataset],
        input_channels: Union[str, List[str]],
        output_channel: Union[str, List[str]],
        kernel_size: Union[int, Tuple[int, int]] = (64, 64),
        strides: Union[int, Tuple[int, int]] = (32, 32),
    ):
        super().__init__()
        if ~isinstance(dataset, (xr.Dataset)):
            # Read dataset if path is given
            self.fdataset = pathlib.Path(dataset)
            dataset = xr.open_dataset(dataset, engine="h5netcdf")

        self.dataset = dataset
        self.input_channels = input_channels
        self.output_channel = output_channel
        self.kernel_size = conv_utils.normalize_tuple(
            kernel_size, 2, "kernel_size"
        )
        self.strides = conv_utils.normalize_tuple(strides, 2, "strides")

    def extract_patches(self, x, filter_nan=False, axis_slice=slice(0, 10)):
        """
        [summary]

        [extended_summary]

        Parameters
        ----------
        x : [type]
            [description]

        filter_nan : bool, optional
            [description], by default False
        Returns
        -------
        patches : tf.Tensor
            patcehs from input array with shape=(patches, patch_height, patch_width, channels).
        """
        if len(x.shape) == 2:
            x = x[..., np.newaxis]

        x = tf.expand_dims(x, 0)
        batch, height, width, channels = x.shape

        try:
            assert len(x.shape) == 3
            assert batch == 1
            assert height == x.shape[0]
            assert width == x.shape[1]
            assert channels == x.shape[2]
        # the errror_message provided by the user gets printed
        except AssertionError as msg:
            print(msg)
        # key,query and value will have the shape of (batch,height,width,depth)
        patches = tf.image.extract_patches(
            images=x,
            sizes=[1, self.kernel_size[0], self.kernel_size[1], 1],
            strides=[1, self.strides[0], self.strides[1], 1],
            rates=[1, 1, 1, 1],
            padding="VALID",
        )

        patches = tf.reshape(
            patches, [-1, self.kernel_size[0], self.kernel_size[1], channels]
        )
        if filter_nan == True:
            patches, _ = filter_nan_patches_axis(
                patches.numpy(), axis_slice=axis_slice
            )
            patches = tf.convert_to_tensor(patches)
        return patches

    def extract_patches_inverse(self, x, y):
        """Standard method to tile images. Inverse patches to one tile.

        [extended_summary]

        Parameters
        ----------
        x : ndarray
            original images are only passed to infer the right shape.
        y : ndarray
            array for the patcehs to be tiled.

        Returns
        -------
        tile: ndarray
            tile image from patcehs
        """
        _x = tf.zeros_like(x)
        _y = self.extract_patches(_x)
        grad = tf.gradients(_y, _x)[0]
        # Divide by grad, to "average" together the overlapping patches
        # otherwise they would simply sum up
        tile = tf.gradients(_y, _x, grad_ys=y)[0] / grad
        return tile

    def xarray_patches(self):
        arr_img = np.array(np.transpose(self.dataset.to_array(), [2, 1, 0]))
        patches = self.extract_patches(
            arr_img, filter_nan=True, axis_slice=slice(0, arr_img.shape[2] - 1)
        )
        ds = patches.numpy()
        dst = xr.Dataset(
            {},
            coords={
                "patch": np.arange(0, ds.shape[0]),
                "y": np.arange(0, self.kernel_size[0]),
                "x": np.arange(0, self.kernel_size[1]),
            },
        )
        for index, var in enumerate(self.dataset.keys()):
            dst[var] = (["patch", "y", "x"], ds[:, :, :, index])

        self.dst_patches = dst
        return self.dst_patches

    def get_commonprofiles(self, cp_path=None):
        if isinstance(self.fdataset, (str, pathlib.Path)):
            self.cp = np.load(self.fdataset.parent / "common_profile.npy")
        else:
            self.cp = np.load(cp_path)

        return self.cp

    def get_dataframe(self):
        self.df = self.dataset.to_dataframe().dropna()
        self.df["filename"] = self.fdataset.parent.name

        return self.df


"""
class My_Custom_Generator(tf.keras.utils.Sequence) :

	def __init__(self, image_filenames, labels, batch_size) :
        self.image_filenames = image_filenames
        self.labels = labels
        self.batch_size = batch_size


	def __len__(self) :
	    return (np.ceil(len(self.image_filenames) / float(self.batch_size))).astype(np.int)

    def __getitem__(self, idx) :
        batch_x = self.image_filenames[idx * self.batch_size : (idx+1) * self.batch_size]
        batch_y = self.labels[idx * self.batch_size : (idx+1) * self.batch_size]

        return batch_x, batch_y
"""


def filter_nan_patches_axis(patches, axis_slice=slice(0, 2)):
    """Remove empty patches.

    [extended_summary]

    Parameters
    ----------
    patches : ndarray
        patches of ndarray with shape=(patches, patch_height, patch_width, channels).
    axis_slice : [type], optional
        [description], by default slice(0, 2)

    Returns
    -------
    ndarray
        ndarray of nan empty patches with shape=(patches-nan_patches, patch_height, patch_width, channels).
    """
    filter_indices = ~np.isnan(patches[:, :, :, axis_slice]).any(axis=(1, 2, 3))
    filter_nan_patches = patches[
        filter_indices,
        :,
    ].reshape(-1, patches.shape[1], patches.shape[2], patches.shape[3])

    return filter_nan_patches, filter_indices


class PixelWiseGenerator(tf.keras.utils.Sequence):
    def __init__(self, paths, batch_size):
        # data = pickle.load(open(filename,'rb'))
        self.paths = paths
        self.batch_size = batch_size
        """
        dst_patches = patches.PatchDatasets(
            dataset=Path(foldername).joinpath("dataset_25m_25m.nc"),
            input_channels="test",
            output_channel="test",
            kernel_size=64,
            strides=16,
            )
        self.commonprofiles = dst_patches.get_commonprofiles()
        data = dst_patches.get_dataframe()
        self.data = data[data['pm_forest_height'] > 0.0 ]
        self.X1 = np.array(self.data['coh_cor'].values)
        self.X2 = np.array(self.data['kz_cor'].values)
        self.X3 = np.array(np.tile(self.commonprofiles,(self.X1.shape[0],1,1)))
        self.y = self.data['pm_forest_height'].values
        """

    """
    @property
    def shape(self):
        return self.X1.shape


    def __len__(self):
        return (len(self.y) - 1) // self.bs + 1


    def __len__(self):
        # steps_per_epoch, if unspecified, will use the len(generator) as a number of steps.
        # hence this
        # ipdb.set_trace()
        return int(np.floor(self.X1.shape[0]/self.batch_size))
    """

    def __len__(self):

        # return int(np.ceil(len(self.paths) / float(self.batch_size)))
        return int(np.ceil(len(self.paths)))

    def __getitem__(self, idx):
        try:
            # start, end = idx * self.bs, (idx+1) * self.bs
            path = self.paths[idx]
            print(path.name)
            data, commonprofiles = self.__load_dataset(path)
            X1 = np.array(data["coh_cor"].values)
            X2 = np.array(data["kz_cor"].values)
            X3 = np.array(np.tile(commonprofiles, (X1.shape[0], 1, 1)))
            y = data["pm_forest_height"].values

            if X1.shape[0] < 100:
                print(f"No sufficient Number of Samples: {path.name}")
                print(f"{X1.shape} {X2.shape} {X3.shape} {y.shape}")
                pass

            else:
                return (X1, X2, X3), y
        except Exception:
            print(f"Error Reading data from: {path.name}")
            pass

        # return [self.X1, self.X2, self.X3], self.y
        # return {'coh_corr': self.X1, 'kz_corr': self.X2, 'common_profiles': self.X3}, np.zeros(())

    def __iter__(self):
        """Create a generator that iterate over the Sequence."""
        yield from (self[i] for i in range(len(self)))

    def __load_dataset(self, path):
        """
        R = Image.open(path + '_red.png')
        G = Image.open(path + '_green.png')
        B = Image.open(path + '_blue.png')
        Y = Image.open(path + '_yellow.png')

        im = np.stack((
            np.array(R),
            np.array(G),
            np.array(B),
            np.array(Y)), -1)

        im = np.divide(im, 255)
        """
        dst_patches = PatchDatasets(
            dataset=pathlib.Path(path).joinpath("dataset_25m_25m.nc"),
            input_channels="test",
            output_channel="test",
            kernel_size=64,
            strides=16,
        )
        commonprofiles = dst_patches.get_commonprofiles()
        data = dst_patches.get_dataframe()
        data = data[data["pm_forest_height"] > 0.0]
        return data, commonprofiles
