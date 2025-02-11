import os
import re
from datetime import datetime, timezone
from typing import Any, Dict, Optional

import rio_stac
import semver
from pystac import (
    Collection,
    Extent,
    Item,
    ItemAssetDefinition,
    Link,
    MediaType,
    Provider,
    ProviderRole,
    RelType,
    SpatialExtent,
    TemporalExtent,
    get_stac_version,
)
from pystac.extensions.classification import (
    Classification,
    ItemAssetsClassificationExtension,
)
from pystac.extensions.render import Render, RenderExtension
from pystac.extensions.scientific import Publication


def format_multiline_string(string: str) -> str:
    """Format a multi-line string for use in metadata fields"""
    return re.sub(r" +", " ", re.sub(r"(?<!\n)\n(?!\n)", " ", string))


def parse_gmw_filename(cog_basename: str) -> Dict[str, Any] | None:
    pattern = r"GMW_([NS]\d+)([EW]\d+)_(\d{4})_v(\d+)\.tif"
    match = re.match(pattern, cog_basename)

    if match:
        lat_str, lon_str, year, version = match.groups()

        lat_direction = lat_str[0]
        lat_value = int(lat_str[1:])
        latitude = lat_value if lat_direction == "N" else -lat_value

        lon_direction = lon_str[0]
        lon_value = int(lon_str[1:])
        longitude = lon_value if lon_direction == "E" else -lon_value

        return {
            "latitude": latitude,
            "longitude": longitude,
            "year": int(year),
            "version": int(version),
        }
    else:
        return None


VERSION = "3.0"
COLLECTION_ID = f"global-mangrove-watch-{VERSION}"
TITLE = "Global Mangrove Watch (1996 - 2020) Version 3.0 Dataset"
KEYWORDS = ["mangrove", "SAR"]

DATASET_DOI = "10.5281/zenodo.6894273"
PUBLICATION_DOI = "10.3390/rs14153657"

PUBLICATION_CITATION = """Bunting, P.; Rosenqvist, A.; Hilarides, L.; Lucas, R.M.; 
Thomas, T.; Tadono, T.; Worthington, T.A.; Spalding, M.; Murray, N.J.; Rebelo, L-M. 
Global Mangrove Extent Change 1996 – 2020: Global Mangrove Watch Version 3.0. Remote 
Sensing. 2022"""

DATASET_CITATION = f"""Bunting, P., Rosenqvist, A., Hilarides, L., Lucas, R., 
Thomas, N., Tadono, T., Worthington, T., Spalding, M., Murray, N., & Rebelo, L.-M. 
(2022). Global Mangrove Watch (1996 - 2020) Version 3.0 Dataset (3.0) [Data set]. 
Zenodo. {DATASET_DOI}"""

DESCRIPTION = f"""This study has used L-band Synthetic Aperture Radar (SAR) global
mosaic datasets from the Japan Aerospace Exploration Agency (JAXA) for 11 epochs from 
1996 to 2020 to develop a long-term time-series of global mangrove extent and change. 
The study used a map-to-image approach to change detection where the baseline map (GMW 
v2.5) was updated using thresholding and a contextual mangrove change mask. This 
approach was applied between all image-date pairs producing 10 maps for each epoch, 
which were summarised to produce the global mangrove time-series. The resulting 
mangrove extent maps had an estimated accuracy of 87.4 % 
(95th conf. int.: 86.2 - 88.6 %), although the accuracies of the individual gain and 
loss change classes were lower at 58.1 % (52.4 - 63.9 %) and 60.6 % (56.1 - 64.8 %), 
respectively. Sources of error included a mis-registration in the SAR mosaic datasets, 
which could only be partially corrected for, but also confusion in fragmented areas of 
mangroves, such as around aquaculture ponds. Overall, 152,604 km2 (133,996 - 176,910) 
of mangroves were identified for 1996, with this decreasing by -5,245 km2 
(-13,587 - 3686) resulting in a total extent of 147,359 km2 (127,925 - 168,895) in 
2020, and representing an estimated loss of 3.4 % over the 24-year time period. The 
Global Mangrove Watch Version 3.0 represents the most comprehensive record of global 
mangrove change achieved to date and is expected to support a wide range of activities, 
including the ongoing monitoring of the global coastal environment, defining and 
assessments of progress towards conservation targets, protected area planning and risk 
assessments of mangrove ecosystems worldwide.

The paper which goes along with this dataset is available at the following reference:

{PUBLICATION_CITATION}"""


COG_ASSET_NAME = "cog"
CHANGE_ASSET_NAME = "change_cog"

ITEM_ASSETS = {
    COG_ASSET_NAME: ItemAssetDefinition.create(
        title="Mangrove cover",
        description="Gridded estimate of mangrove cover",
        media_type=MediaType.COG.value,
        roles=["data"],
    ),
    CHANGE_ASSET_NAME: ItemAssetDefinition.create(
        title="Mangrove cover change since 1996",
        description="Gridded estimate of mangrove cover change since 1996",
        media_type=MediaType.COG.value,
        roles=["data"],
    ),
}


def create_collection() -> Collection:
    """Creates a STAC Collection.

    Returns:
        Collection: STAC Collection object
    """
    extent = Extent(
        SpatialExtent([[-180.0, 90.0, 180.0, -90.0]]),
        TemporalExtent(
            [
                [
                    datetime(1996, 1, 1, tzinfo=timezone.utc),
                    datetime(2020, 12, 31, 23, 59, 59, tzinfo=timezone.utc),
                ]
            ]
        ),
    )

    collection = Collection(
        id=COLLECTION_ID,
        title=TITLE,
        description=format_multiline_string(DESCRIPTION),
        keywords=KEYWORDS,
        extent=extent,
        license="CC-BY-4.0",
        providers=[
            Provider(
                name="Zenodo",
                url="https://zenodo.org/records/6894273",
                roles=[
                    ProviderRole.HOST,
                ],
            ),
            Provider(
                name="Global Mangrove Watch",
                url="https://www.globalmangrovewatch.org/",
                roles=[
                    ProviderRole.PRODUCER,
                    ProviderRole.LICENSOR,
                ],
            ),
        ],
    )

    collection.add_link(
        Link(
            rel=RelType.LICENSE,
            target="https://creativecommons.org/licenses/by/4.0/",
            media_type=MediaType.HTML,
            title="CC-BY-4.0 license",
        ),
    )

    collection.item_assets = ITEM_ASSETS

    # classification values
    cog_classification = ItemAssetsClassificationExtension(
        collection.item_assets[COG_ASSET_NAME]
    )
    cog_classification.classes = [
        Classification.create(
            value=0,
            description="nodata",
            nodata=True,
            name="nodata",
        ),
        Classification.create(
            value=1,
            description="mangrove",
            name="mangrove",
            color_hint="009600",
        ),
    ]

    change_classification = ItemAssetsClassificationExtension(
        collection.item_assets[CHANGE_ASSET_NAME]
    )
    change_classification.classes = [
        Classification.create(
            value=0,
            description="nodata",
            nodata=True,
            name="nodata",
        ),
        Classification.create(
            value=1,
            description="mangrove gained",
            name="mangrove-gained",
            color_hint="ff0000",
        ),
        Classification.create(
            value=2,
            description="mangrove lost",
            name="mangrove-lost",
            color_hint="0000ff",
        ),
    ]

    collection.ext.add("version")
    collection.ext.version.version = VERSION

    collection.ext.add("sci")
    collection.ext.sci.doi = DATASET_DOI
    collection.ext.sci.citation = format_multiline_string(DATASET_CITATION)
    collection.ext.sci.publications = [
        Publication(
            doi=PUBLICATION_DOI,
            citation=format_multiline_string(PUBLICATION_CITATION),
        )
    ]

    # if using STAC v1.0.0, add raster and item-assets extensions
    if semver.Version.parse(get_stac_version()) <= semver.Version.parse("1.0.0"):
        collection.ext.add("raster")
        collection.ext.add("item_assets")

    # add render extension
    collection.ext.add("render")
    renders = {
        "mangroves": Render.create(
            assets=[COG_ASSET_NAME],
            colormap={
                # convert hex to rgb
                str(classification.value): tuple(
                    int(classification.color_hint[i : i + 2], 16) for i in (0, 2, 4)
                )
                for classification in cog_classification.classes
                if classification.color_hint
            },
        ),
        "change": Render.create(
            assets=[CHANGE_ASSET_NAME],
            colormap={
                # convert hex to rgb
                str(classification.value): tuple(
                    int(classification.color_hint[i : i + 2], 16) for i in (0, 2, 4)
                )
                for classification in change_classification.classes
                if classification.color_hint
            },
        ),
    }

    RenderExtension.ext(collection).apply(renders)

    return collection


def create_item(cog_asset_href: str, change_asset_href: Optional[str] = None) -> Item:
    """Creates a STAC item from a asset href.

    Args:
        cog_asset_href (str): The HREF pointing to the COG asset associated with the
        item

    Returns:
        Item: STAC Item object
    """
    cog_basename = os.path.basename(cog_asset_href)
    item_attributes = parse_gmw_filename(cog_basename)

    if not item_attributes:
        raise ValueError(f"could not parse item properties from {cog_asset_href}")

    assets = {
        asset_key: ITEM_ASSETS[asset_key].create_asset(href=asset_href)
        for asset_key, asset_href in zip(
            [COG_ASSET_NAME, CHANGE_ASSET_NAME], [cog_asset_href, change_asset_href]
        )
        if asset_href
    }

    item = rio_stac.create_stac_item(
        source=cog_asset_href,
        id=cog_basename.replace(".tif", ""),
        assets=assets,
        with_proj=True,
        with_raster=False,
        input_datetime=datetime(year=item_attributes["year"], month=12, day=31),
        raster_max_size=4500,
        geom_precision=4,
    )

    assert isinstance(item, Item)

    return item
