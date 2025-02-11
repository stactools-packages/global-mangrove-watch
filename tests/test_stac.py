from stactools.global_mangrove_watch import stac

from . import test_data


def test_create_collection() -> None:
    # This function should be updated to exercise the attributes of interest on
    # the collection

    collection = stac.create_collection()
    collection.set_self_href(None)  # required for validation to pass
    assert collection.id == stac.COLLECTION_ID
    collection.validate()


def test_create_item() -> None:
    # This function should be updated to exercise the attributes of interest on
    # a typical item

    item = stac.create_item(test_data.get_path("data/GMW_N26W082_2020_v3.tif"))
    assert item.id == "GMW_N26W082_2020_v3"
    item.validate()
