import os
import sys

import pytest
import tempenv
import xarray as xr
from cloudpathlib import AnyPath, S3Client

from eoreader import utils
from eoreader.bands import *
from eoreader.env_vars import DEM_PATH, S3_DB_URL_ROOT
from eoreader.exceptions import InvalidTypeError
from eoreader.reader import Platform

from .scripts_utils import (
    AWS_ACCESS_KEY_ID,
    AWS_S3_ENDPOINT,
    AWS_SECRET_ACCESS_KEY,
    READER,
    dask_env,
    get_db_dir,
    opt_path,
    s3_env,
)


@pytest.mark.xfail
def test_utils():
    root_dir = AnyPath(__file__).parent.parent.parent
    # Root directory
    src_dir = root_dir.joinpath("eoreader")
    data_dir = src_dir.joinpath("data")
    assert utils.get_root_dir() == root_dir
    assert utils.get_src_dir() == src_dir
    assert utils.get_data_dir() == data_dir


def test_alias():
    # DEM
    assert not is_dem(NDVI)
    assert not is_dem(HH)
    assert not is_dem(GREEN)
    assert is_dem(SLOPE)
    assert not is_dem(CLOUDS)

    # Index
    assert is_index(NDVI)
    assert not is_index(HH)
    assert not is_index(GREEN)
    assert not is_index(SLOPE)
    assert not is_index(CLOUDS)

    # Bands
    assert not is_sat_band(NDVI)
    assert is_sat_band(HH)
    assert is_sat_band(GREEN)
    assert not is_sat_band(SLOPE)
    assert not is_sat_band(CLOUDS)

    # Clouds
    assert not is_clouds(NDVI)
    assert not is_clouds(HH)
    assert not is_clouds(GREEN)
    assert not is_clouds(SLOPE)
    assert is_clouds(CLOUDS)

    # Other functions
    lst = to_band(["NDVI", "GREEN", RED, "VH_DSPK", "SLOPE", DEM, "CLOUDS", CLOUDS])
    assert lst == [NDVI, GREEN, RED, VH_DSPK, SLOPE, DEM, CLOUDS, CLOUDS]
    with pytest.raises(InvalidTypeError):
        to_band(["WRONG_BAND"])


@s3_env
@dask_env
def test_products():
    # Get paths
    prod1_path = opt_path().joinpath(
        "LC08_L1GT_023030_20200518_20200527_01_T2"
    )  # Newer
    prod2_path = opt_path().joinpath(
        "LM03_L1GS_033028_19820906_20180414_01_T2"
    )  # Older

    # Open prods
    prod1 = READER.open(prod1_path)
    prod2 = READER.open(prod2_path)

    assert prod1 == prod1
    assert prod1 >= prod1
    assert prod1 <= prod1
    assert prod1 > prod2
    assert prod2 < prod1
    assert prod1 != prod2

    # Test bands
    assert prod1.has_band(BLUE)
    assert prod1.has_bands(BLUE)
    assert prod1.has_bands([BLUE, RED, GREEN])
    with pytest.raises(AssertionError):
        assert prod1.has_band(VV)
    with pytest.raises(AssertionError):
        assert prod1.has_bands(VV)
    with pytest.raises(AssertionError):
        assert prod1.has_bands([VV, RED, GREEN])

    # Test without a DEM set:
    old_dem = None
    if DEM_PATH in os.environ:
        old_dem = os.environ.pop(DEM_PATH)
    with pytest.raises(ValueError):
        prod1.load([DEM])
    with pytest.raises(FileNotFoundError):
        os.environ[DEM_PATH] = "fczergg"
        prod1.load([DEM])

    # Reset DEM
    if old_dem != os.environ[DEM_PATH]:
        if not old_dem:
            del os.environ[DEM_PATH]
        else:
            os.environ[DEM_PATH] = old_dem

    # Test invalid band
    with pytest.raises(AssertionError):
        prod1.load("TEST")


@pytest.mark.skipif(
    S3_DB_URL_ROOT not in os.environ or sys.platform == "win32",
    reason="S3 DB not set or Rasterio bugs with http urls",
)
@s3_env
@dask_env
def test_dems_https():
    # Get paths
    prod_path = opt_path().joinpath("LC08_L1GT_023030_20200518_20200527_01_T2")

    # Open prods
    prod = READER.open(prod_path)

    # Test two different DEM source
    dem_sub_dir_path = [
        "GLOBAL",
        "MERIT_Hydrologically_Adjusted_Elevations",
        "MERIT_DEM.vrt",
    ]
    local_path = str(get_db_dir().joinpath(*dem_sub_dir_path))
    remote_path = "/".join([os.environ.get(S3_DB_URL_ROOT, ""), *dem_sub_dir_path])

    # Loading same DEM from two different sources (one hosted locally and the other hosted on S3 compatible storage)
    with tempenv.TemporaryEnvironment({DEM_PATH: local_path}):  # Local DEM
        dem_local = prod.load(
            [DEM], resolution=30
        )  # Loading same DEM from two different sources (one hosted locally and the other hosted on S3 compatible storage)
    with tempenv.TemporaryEnvironment({DEM_PATH: remote_path}):  # Remote DEM
        dem_remote = prod.load([DEM], resolution=30)

    xr.testing.assert_equal(dem_local[DEM], dem_remote[DEM])


@s3_env
@pytest.mark.skipif(
    AWS_ACCESS_KEY_ID not in os.environ,
    reason="AWS S3 Compatible Storage IDs not set",
)
def test_dems_S3():
    # Get paths
    prod_path = opt_path().joinpath("LC08_L1GT_023030_20200518_20200527_01_T2")

    # Open prods
    prod = READER.open(prod_path)

    # Test two different DEM source
    dem_sub_dir_path = [
        "GLOBAL",
        "MERIT_Hydrologically_Adjusted_Elevations",
        "MERIT_DEM.vrt",
    ]
    local_path = str(get_db_dir().joinpath(*dem_sub_dir_path))

    # ON S3
    client = S3Client(
        endpoint_url=f"https://{AWS_S3_ENDPOINT}",
        aws_access_key_id=os.getenv(AWS_ACCESS_KEY_ID),
        aws_secret_access_key=os.getenv(AWS_SECRET_ACCESS_KEY),
    )
    client.set_as_default_client()
    s3_path = str(AnyPath("s3://sertit-geodatastore").joinpath(*dem_sub_dir_path))

    # Loading same DEM from two different sources (one hosted locally and the other hosted on S3 compatible storage)
    with tempenv.TemporaryEnvironment({DEM_PATH: local_path}):  # Local DEM
        dem_local = prod.load(
            [DEM], resolution=30
        )  # Loading same DEM from two different sources (one hosted locally and the other hosted on S3 compatible storage)
    with tempenv.TemporaryEnvironment({DEM_PATH: s3_path}):  # S3 DEM
        dem_s3 = prod.load([DEM], resolution=30)

    xr.testing.assert_equal(dem_local[DEM], dem_s3[DEM])


def test_bands():
    # SAR
    assert SarBandNames.from_list(["VV", "VH"]) == [VV, VH]
    assert SarBandNames.to_value_list([HV_DSPK, VV]) == ["HV_DSPK", "VV"]
    assert SarBandNames.to_value_list() == SarBandNames.list_values()
    assert SarBandNames.corresponding_speckle(SarBandNames.VV) == VV
    assert SarBandNames.corresponding_speckle(SarBandNames.VV_DSPK) == VV

    # OPTIC
    map_dic = {
        CA: "01",
        BLUE: "02",
        GREEN: "03",
        RED: "04",
        VRE_1: "05",
        VRE_2: "06",
        VRE_3: "07",
        NIR: "08",
        NARROW_NIR: "8A",
        WV: "09",
        SWIR_1: "11",
        SWIR_2: "12",
    }
    ob = OpticalBands()
    ob.map_bands(map_dic)

    for key, val in map_dic.items():
        assert key in ob._band_map
        assert ob._band_map[key] == map_dic[key]

    with pytest.raises(InvalidTypeError):
        ob.map_bands({VV: "wrong_val"})


@s3_env
def test_reader_methods():
    # Get paths
    prod_path = opt_path().joinpath("LC08_L1GT_023030_20200518_20200527_01_T2")

    # NAME
    READER.valid_name(prod_path, Platform.L8)
    READER.valid_name(prod_path, "L8")
    READER.valid_name(prod_path, "Landsat-8")
    READER.valid_name(prod_path, Platform.L8.name)
    READER.valid_name(prod_path, Platform.L8.value)

    # MTD
    READER.valid_mtd(prod_path, Platform.L8)
    READER.valid_mtd(prod_path, "L8")
    READER.valid_mtd(prod_path, "Landsat-8")
    READER.valid_mtd(prod_path, Platform.L8.name)
    READER.valid_mtd(prod_path, Platform.L8.value)
