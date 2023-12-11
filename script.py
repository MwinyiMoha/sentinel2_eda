import os

import geopandas as gpd
import numpy
import rasterio
from rasterstats import zonal_stats
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base
from rasterio.mask import mask


class ImageProcessor:

    IMAGES_PATH = "S2B_MSIL2A_20221127T075159_N0400_R135_T36NXF_20221127T100500.SAFE/GRANULE/L2A_T36NXF_A029905_20221127T080452/IMG_DATA/R10m"
    NDVI_OUT_IMAGE = "NDVI.tiff"
    IMAGE_DATE = "20221127T075159"

    def __init__(self, data_path, database_url) -> None:
        self.data_path = data_path
        self.database_url = database_url
        self.image_dir = os.path.join(self.data_path, self.IMAGES_PATH)

    def inspect_image(self):
        BLUE = "T36NXF_20221127T075159_B02_10m.jp2"

        with rasterio.open(os.path.join(self.image_dir, BLUE)) as band_blue:
            meta = band_blue.meta.copy()
            print(meta)

    def mask_image(self):
        BLUE = "T36NXF_20221127T075159_B02_10m.jp2"
        GREEN = "T36NXF_20221127T075159_B03_10m.jp2"
        RED = "T36NXF_20221127T075159_B04_10m.jp2"
        NIR = "T36NXF_20221127T075159_B08_10m.jp2"

        band_blue = None
        with rasterio.open(os.path.join(self.image_dir, BLUE)) as blue:
            band_blue = blue.read(1)

        band_green = None
        with rasterio.open(os.path.join(self.image_dir, GREEN)) as green:
            band_green = green.read(1)

        band_red = None
        with rasterio.open(os.path.join(self.image_dir, RED)) as red:
            band_red = red.read(1)

        band_nir = None
        with rasterio.open(os.path.join(self.image_dir, NIR)) as nir:
            band_nir = nir.read(1)

        composite = os.path.join(self.image_dir, "COMPOSITE.tiff")
        with rasterio.open(
            composite, 
            "w",
            driver="GTiff", 
            width=blue.width, 
            height=blue.height, 
            count=4, 
            crs=blue.crs,
            transform=blue.transform,
            dtype=blue.dtypes[0]
        ) as out:
            out.write(band_blue, 1)
            out.write(band_green, 2)
            out.write(band_red, 3)
            out.write(band_nir, 4)
        
        with rasterio.open(composite) as src:
            boundary = self.prepare_roi(red.crs)
            out_image, out_transform = mask(src, boundary.geometry, crop=True)
            out_meta = src.meta.copy()
            out_meta.update({
                "driver": "GTiff",
                "transform": out_transform,
                "height": out_image.shape[1],
                "width": out_image.shape[2],
                "region": "test roi"
            })

        masked_composite = os.path.join(self.image_dir, "MASKED_COMPOSITE.tiff")
        with rasterio.open(masked_composite, "w", **out_meta) as final:
            final.write(out_image)

    def write_ndvi_image(self):
        RED = "T36NXF_20221127T075159_B04_10m.jp2"
        NIR = "T36NXF_20221127T075159_B08_10m.jp2"

        band_red = None
        with rasterio.open(os.path.join(self.image_dir, RED)) as red:
            band_red = red.read(1)

        band_nir = None
        with rasterio.open(os.path.join(self.image_dir, NIR)) as nir:
            band_nir = nir.read(1)

        numpy.seterr(invalid="ignore", divide="ignore")
        ndvi = (band_nir.astype(float)-band_red.astype(float)) / (band_nir+band_red)
        meta = red.meta.copy()
        meta.update(dtype=rasterio.float32, driver="GTiff")

        ndvi_dst = os.path.join(self.image_dir, self.NDVI_OUT_IMAGE)
        with rasterio.open(ndvi_dst, "w", **meta) as dst:
            dst.write_band(1, ndvi.astype(rasterio.float32))

    def prepare_roi(self, out_crs):
        roi_json = os.path.join(self.data_path, "region_of_interest.geojson")
        roi = gpd.read_file(roi_json)
        roi = roi.to_crs(out_crs)
        return roi
    
    def calculate_ndvi_zonal_statistics(self):
        ndvi_image = os.path.join(self.image_dir, self.NDVI_OUT_IMAGE)

        band_ndvi = None
        with rasterio.open(ndvi_image) as ndvi:
            band_ndvi = ndvi.read(1)

        boundary = self.prepare_roi(ndvi.crs)
        selected_stats = ["min", "max", "mean", "median", "std"]
        stats = zonal_stats(boundary, band_ndvi, affine=ndvi.transform, stats=selected_stats)
        self.save_statistics(stats)

    def save_statistics(self, stats):
        engine = create_engine(self.database_url)
        Base = declarative_base()

        class ZonalStatistics(Base):
            __tablename__ = "test_roi_tbl"
   
            id = Column(Integer, primary_key = True)
            image_date = Column(String)
            min = Column(Float)
            max = Column(Float)
            mean = Column(Float)
            median = Column(Float)
            std_dev = Column(Float)

        Base.metadata.create_all(engine)
        Session = sessionmaker(bind = engine)
        session = Session()

        zs = ZonalStatistics()
        zs.image_date = self.IMAGE_DATE
        zs.min = stats[0]["min"]
        zs.max = stats[0]["max"]
        zs.mean = stats[0]["mean"]
        zs.median = stats[0]["median"]
        zs.std_dev = stats[0]["std"]

        session.add(zs)
        session.commit()


if __name__ == "__main__":
    db_url = "postgresql://postgres:postgres@localhost:5432/zonal_statistics_db"
    data_path = os.path.join(os.path.dirname(__file__), "data")

    script = ImageProcessor(data_path, db_url)
    script.inspect_image()
    script.mask_image()
    script.write_ndvi_image()
    script.calculate_ndvi_zonal_statistics()
