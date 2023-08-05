#%%
import os

# importing shutil module
import shutil
import sys
from datetime import datetime
from pathlib import Path

import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
import rasterio as rio
import rioxarray
import xarray as xr
from rasterio.enums import Resampling


#%%
def npy_load_rot_flip_img(file_name, n_rot90=1, flip_axis=0):
    data = np.load(file_name)
    data = np.flip(np.rot90(data, n_rot90), flip_axis)
    return data


def create_netcdf_dataset(insar_processed_folder, outname, overwrite=False):
    from pathlib import Path

    if overwrite or not Path(outname).is_file():
        # Read lat lon for geocoding
        lat = np.load(
            insar_processed_folder.joinpath("./col_axis_lat_coord.npy")
        )
        lon = np.load(
            insar_processed_folder.joinpath("./row_axis_lon_coord.npy")
        )

        paramters2save = [
            file.name[:-15]
            for file in sorted(
                list(insar_processed_folder.glob("*_geo_lonlat.npy"))
            )
        ]
        # Init xarray empty dataset
        dst = xr.Dataset(
            {},
            coords={
                "y": lat,
                "x": lon,
            },
        )

        for var in paramters2save:
            # print(var)
            var_load = npy_load_rot_flip_img(
                insar_processed_folder.joinpath(f"./{var}_geo_lonlat.npy")
            )

            if "mask" in var:
                print(f"Mask var: {var}")
                dst[var] = (["y", "x"], np.int8(var_load))
            elif "forest_height" in var:
                dst[f"pm_{var}"] = (["y", "x"], np.float32(var_load))
            elif (
                np.all(np.iscomplex(var_load))
                or "slave_image" in var
                or "master_image" in var
            ):
                print(f"Complex var: {var}")
                dst[f"{var}_real"] = (
                    ["y", "x"],
                    np.float32(np.real(var_load)),
                )
                dst[f"{var}_imag"] = (
                    ["y", "x"],
                    np.float32(np.imag(var_load)),
                )

            else:
                print(f"float32 var: {var}")
                dst[var] = (["y", "x"], np.float32(var_load))
        mask_forest = np.int8(dst["pm_forest_height"] > 0)
        dst["mask_forest"] = (("y", "x"), mask_forest)
        """
        # define and read the dataset varaible
        kz = npy_load_rot_flip_img(insar_processed_folder.joinpath('./kz_cor_geo_lonlat.npy'))
        coh = npy_load_rot_flip_img(insar_processed_folder.joinpath('./coh_cor_geo_lonlat.npy'))
        forest_height = npy_load_rot_flip_img(insar_processed_folder.joinpath('./forest_height_geo_lonlat.npy'))
        #phase = npy_load_rot_flip_img(insar_processed_folder.joinpath('./phase_geo_lonlat.npy'))
        #interferogram = npy_load_rot_flip_img(insar_processed_folder.joinpath('./interferogram_geo_lonlat.npy'))
        master_image = npy_load_rot_flip_img(insar_processed_folder.joinpath('./master_image_geo_lonlat.npy'))
        slave_image = npy_load_rot_flip_img(insar_processed_folder.joinpath('./slave_image_geo_lonlat.npy'))

        max_valid_height = npy_load_rot_flip_img(insar_processed_folder.joinpath('./max_valid_height_geo_lonlat.npy'))
        min_valid_height = npy_load_rot_flip_img(insar_processed_folder.joinpath('./min_valid_height_geo_lonlat.npy'))
        bias = npy_load_rot_flip_img(insar_processed_folder.joinpath('./bias_geo_lonlat.npy'))
        dem = npy_load_rot_flip_img(insar_processed_folder.joinpath('./dem_geo_lonlat.npy'))

        # define and read the masks
        mask_coh = npy_load_rot_flip_img(insar_processed_folder.joinpath('./mask_coh_geo_lonlat.npy'))
        mask_kz = npy_load_rot_flip_img(insar_processed_folder.joinpath('./mask_kz_geo_lonlat.npy'))
        # Generate mask above the forest only
        mask_forest = np.int8((forest_height > 0))

        # Create Xarray Dataset
        dst = xr.Dataset(
            {
                'coherence': (('y', 'x'), coh),
                'kz': (('y', 'x'), kz),
                'pm_forest_height': (('y', 'x'), forest_height),
                #'phase': (('y', 'x'), phase),
                #'interferogram': (('y', 'x'), interferogram),
                'master_image': (('y', 'x'), master_image),
                'slave_image': (('y', 'x'), slave_image),
                'max_valid_height': (('y', 'x'), max_valid_height),
                'min_valid_height': (('y', 'x'), min_valid_height),
                'bias': (('y', 'x'), bias),
                'mask_coh': (('y', 'x'), mask_coh),
                'mask_kz': (('y', 'x'), mask_kz),
                'mask_forest': (('y', 'x'), mask_forest),
                'dem': (('y', 'x'), dem),
            },
            coords={
                'y': lat,
                'x': lon,            
            },
        )
        """
        # dst.coords['mask_coh'] = (('y', 'x'), mask_coh )
        # dst.coords['mask_kz'] = (('y', 'x'), mask_kz )
        # dst.coords['mask_forest'] = (('y', 'x'), mask_forest )

        # Set metadata
        # dst.rio.write_crs(4326)
        # dst.rio.write_crs(4326)

        # First Write CRS and WGS data
        dst = dst.rio.write_crs(input_crs=4326, inplace=True)
        # Update the nodata to nan for easier data handling (Needs to be after crs)
        dst = dst.rio.update_attrs(dict(_nodata=np.nan), inplace=True)
        nodata = dst.rio._nodata
        dst_nan = dst.where(dst != nodata)
        dst_nan.rio.set_nodata = np.nan
        dst_nan = dst_nan.rio.update_attrs(
            dict(nodatavals=(np.nan,)), inplace=True
        )
        # print(nodata, dst_nan.nodata)

        dst_nan_reproject = dst_nan.rio.reproject(
            dst_crs=32732, resolution=25.0, resampling=Resampling.bilinear
        )

        dst_nan_reproject.attrs["history"] = (
            "File created: {}".format(
                datetime.now().strftime("%Y.%m.%d %H:%M:%S")
            )
            + f"\nProcessed from: {insar_processed_folder}"
            + "\nProcessed by: {}".format(os.environ.get("USER"))
        )

        # dst.rio.set_attrs(dict(nodatavals=(np.nan,)))

        dst_nan_reproject.attrs["Conventions"] = "CF-1.6"
        # dst.attrs['crs'] = '+init=epsg:4326'

        # The parameters to make sure to write the file with complex data
        # save the variable
        try:
            dst_nan_reproject.to_netcdf(
                outname, engine="h5netcdf", invalid_netcdf=True
            )
            print("Wrote file:", outname)
        except:
            print(f"Error writing file: {str(outname)}")
        else:
            print(f"Done writing file: {str(outname)}")

    else:
        dst_nan_reproject = xr.open_dataset(outname, engine="h5netcdf")
        print("Reading file:", outname)
        try:
            dst_nan_reproject = xr.open_dataset(outname, engine="h5netcdf")
        except:
            print(f"Error reading file: {str(outname)}")
        else:
            print(f"Done reading file: {str(outname)}")
    return dst_nan_reproject


def netcdf_training_dataset(tdxprocessedpath, netcdf_path, gt_path):

    Path(netcdf_path).mkdir(parents=True, exist_ok=True)

    ds = create_netcdf_dataset(
        tdxprocessedpath,
        outname=netcdf_path.joinpath("dataset_geo.nc"),
        overwrite=True,
    )

    groundtruth_dataset = xr.open_rasterio(Path(gt_path))
    nodata = groundtruth_dataset.rio.nodata
    groundtruth_dataset_nan = groundtruth_dataset.where(
        groundtruth_dataset != nodata
    )
    # groundtruth_dataset_nan = groundtruth_dataset.rio.update_attrs(dict(nodatavals=(np.nan,)))
    groundtruth_dataset_nan = groundtruth_dataset_nan.rio.write_nodata(
        np.nan, encoded=True, inplace=True
    )
    groundtruth_dataset_nan.rio.set_nodata = np.nan
    groundtruth_dataset_nan = groundtruth_dataset_nan.rio.update_attrs(
        dict(nodatavals=(np.nan,))
    )
    # print(nodata, groundtruth_dataset_nan.data)
    groundtruth_dataset_nan

    groundtruth_dataset_nan_reproject = (
        groundtruth_dataset_nan.rio.reproject_match(
            ds, resampling=Resampling.bilinear
        )
    )

    ds_reproject_clip = ds  # ds.where((ds.mask_forest == 1))

    groundtruth_dataset_nan_clip = groundtruth_dataset_nan_reproject.sel(
        dict(band=1)
    )

    ds_reproject_clip["lvis_rh100"] = groundtruth_dataset_nan_clip.where(
        ds_reproject_clip.coh_cor >= 0
    )

    # Check if there is an overlap between the ground truth and TDX datasetS
    if (
        np.count_nonzero(
            ~np.isnan(
                ds_reproject_clip["lvis_rh100"].where(
                    ds_reproject_clip.coh_cor >= 0
                )
            )
        )
        > 0
    ):
        print(f"Writing dataset with ground truth for {str(netcdf_path)}")
        ds_reproject_clip.to_netcdf(
            netcdf_path.joinpath("dataset_25m_25m.nc"),
            engine="h5netcdf",
            invalid_netcdf=True,
        )
        # Save as GeoTiff as needed
        ds_reproject_clip["coh_cor"].rio.to_raster(
            netcdf_path.joinpath("./coh_cor.tif")
        )
        ds_reproject_clip["kz_cor"].rio.to_raster(
            netcdf_path.joinpath("./kz_cor.tif")
        )
        ds_reproject_clip["pm_forest_height"].rio.to_raster(
            netcdf_path.joinpath("./pm_forest_height.tif")
        )
        ds_reproject_clip["dem"].rio.to_raster(
            netcdf_path.joinpath("./dem.tif")
        )
        # ds_reproject_clip["phase"].rio.to_raster(netcdf_path.joinpath("./phase.tif"))
        # ds_reproject_clip["slave_image"].rio.to_raster(netcdf_path.joinpath("./slave_image.tif"))
        # ds_reproject_clip["master_image"].rio.to_raster(netcdf_path.joinpath("./master_image.tif"))

        # groundtruth_dataset_nan_clip.rio.to_raster(netcdf_path.joinpath("./lvis_rh100.tif"))
        ds_reproject_clip["lvis_rh100"].rio.to_raster(
            netcdf_path.joinpath("./lvis_rh100.tif")
        )

        f, (ax1, ax2, ax3, ax4) = plt.subplots(
            1, 4, sharey=True, figsize=(20, 6)
        )
        """
        f = plt.figure(constrained_layout=True, figsize=(20,6))
        spec1 = gridspec.GridSpec(ncols=4, nrows=2, figure=f)
        ax1 = f.add_subplot(spec1[0, 0])
        ax2 = f.add_subplot(spec1[0, 1])
        ax3 = f.add_subplot(spec1[0, 2])
        ax4 = f.add_subplot(spec1[0, 3])
        """
        ax1_im = ds_reproject_clip["coh_cor"].plot.imshow(
            ax=ax1,
            vmin=0,
            vmax=1,
            cmap="gray",
            origin="upper",
            x="x",
            y="y",
            add_colorbar=False,
        )
        ax2_im = ds_reproject_clip["kz_cor"].plot.imshow(
            ax=ax2, cmap="jet", origin="upper", x="x", y="y", add_colorbar=False
        )
        ax3_im = ds_reproject_clip["lvis_rh100"].plot.imshow(
            ax=ax3,
            vmin=0,
            vmax=np.ceil(np.nanmax(ds_reproject_clip["pm_forest_height"]) / 10)
            * 10,
            cmap="YlGn",
            x="x",
            y="y",
            origin="upper",
            add_colorbar=False,
        )
        ax4_im = ds_reproject_clip["pm_forest_height"].plot.imshow(
            ax=ax4,
            vmin=0,
            vmax=np.ceil(np.nanmax(ds_reproject_clip["pm_forest_height"]) / 10)
            * 10,
            cmap="YlGn",
            x="x",
            y="y",
            origin="upper",
            add_colorbar=False,
        )

        ax1.set_title("Coherence")

        # ax2.axis('equal')
        ax2.set_title("$K_z$")

        # ax3.axis('equal')
        ax3.set_title("LVIS $RH_{100}$")

        # ax4.axis('equal')
        ax4.set_title("PM Forest Height")

        ax1.set_aspect("equal", "box")
        ax2.set_aspect("equal", "box")
        ax3.set_aspect("equal", "box")
        ax4.set_aspect("equal", "box")

        f.colorbar(ax1_im, ax=ax1, shrink=0.7)
        f.colorbar(ax2_im, ax=ax2, shrink=0.7)
        f.colorbar(ax3_im, ax=ax3, shrink=0.7)
        f.colorbar(ax4_im, ax=ax4, shrink=0.7)

        f.tight_layout()
        f.suptitle(netcdf_path.name + "\n\n", fontsize=16)
        f.savefig(netcdf_path.joinpath("./dataset_plot.png"))

        return True

    else:
        # Path(str(netcdf_path) + '_ERROR/').mkdir(parents=True, exist_ok=True)
        shutil.move(str(netcdf_path) + "/", str(netcdf_path) + "_ERROR")
        # netcdf_path.rename(str(netcdf_path) + '_ERROR/')

        return False


# %%
