<p align="center">
    <strong>Block development toolkit for UP42.</strong>
</p>

<p align="center">
    <a href="https://pypi.org/project/up42-blockutils/" title="up42-blockutils on pypi"><img src="https://img.shields.io/pypi/v/up42-blockutils"></a>
    <a href="https://twitter.com/UP42_" title="UP42 on Twitter"><img src="https://img.shields.io/twitter/follow/UP42_.svg?style=social"></a>
</p>

<p align="center">
    <b>
      <a href="https://blockutils.up42.com/"> Documentation</a> &nbsp; • &nbsp;
      <a href="http://www.up42.com">UP42.com</a> &nbsp; • &nbsp;
      <a href="#support">Support</a>
    </b>
</p>

## Highlights

- Python package with utilities to build blocks in UP42.
- For UP42 partners and customers interested in creating blocks!
- Base classes for data and processing blocks.
- Facilities to easily create tests, ensuring production ready blocks.

## Overview

The UP42 `blockutils` package provides several modules with specific concerns:

- **Blocks**: Base classes for data and processing blocks.
- **Common**: Directory and query/parameter input handling.
- **Logging**: Standard logging facility.
- **Data Path**: Input and output file handling.
- **E2E**: Utility class to create end-to-end tests.
- **Exceptions**: Shared exceptions between blocks.
- **Format**: Exotic file handling (DIMAP and NETCDF).
- **Raster**: Raster handling methods.
- **Geometry**: Generic recurrent geometry operations.
- **Windows**: Raster windowed read and write helper, useful for large file handling.
- **STAC**: Handling STAC type queries.
- **WMTS**: Helper for downloading, processing and merging tiles.

See the full code reference [here](https://blockutils.up42.com/blocks/).

## Docker image

In order to make development of blocks easier, we have made available a public `blockutils`
base image that you can use in your `Dockerfile`. Check out the
[DockerHub page](https://hub.docker.com/r/up42/up42-blockutils-py37)
for the `up42/up42-blockutils-py37` image.


## Template repositories

For your convenience, we have created two template repositories hosted on GitHub
 that include this package and generic `make` utilities for building and pushing blocks:

- [Data block template](https://github.com/up42/data-block-template)
- [Processing block template](https://github.com/up42/processing-block-template)

## Install

The package requires Python > 3.6.

```bash
pip install up42-blockutils
```

## Quickstart

The example below shows a minimal processing block that takes a raster file and returns
the raster values to the power of 2. In this example we make use of the `logging`,
`blocks`, `exceptions`, `datapath` and `windows` modules.

```python3
from pathlib import Path
import rasterio as rio
from geojson import FeatureCollection, Feature
import blockutils

logger = blockutils.logging.get_logger(__name__)


class AProcessingBlock(blockutils.blocks.ProcessingBlock):
    def process(self, input_fc: FeatureCollection) -> FeatureCollection:
        output_fc = FeatureCollection([])

        if not input_fc.features:
            raise blockutils.exceptions.UP42Error(
                blockutils.exceptions.SupportedErrors.NO_INPUT_ERROR
            )

        for feat in input_fc["features"]:
            logger.info(f"Processing {feat}...")
            input_path = Path("/tmp/input/") / Path(blockutils.datapath.get_data_path(feat))
            with rio.open(input_path) as src:
                src_win = blockutils.windows.WindowsUtil(src)
                (
                    output_name,
                    output_path,
                ) = blockutils.datapath.get_output_filename_and_path(
                    input_path.name, postfix="processed"
                )
                dst_meta = src.meta.copy()
                with rio.open(output_path, "w", **dst_meta) as dst:
                    for win in src_win.windows_regular():
                        exp = src.read(window=win) ** 2
                        dst.write(exp, window=win)

                out_feat = Feature(bbox=feat.bbox, geometry=feat.geometry)
                out_feat["properties"] = self.get_metadata(feat)
                out_feat = blockutils.datapath.set_data_path(out_feat, output_name)
                logger.info(f"Processed {out_feat}...")
                output_fc.features.append(out_feat)
            return output_fc


AProcessingBlock().run()
```

## Support

For any issues or help please contact us via Email **[support@up42.com](mailto:support@up42.com)**.
