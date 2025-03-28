from pathlib import Path

from click import Group
from click.testing import CliRunner
from pystac import Collection, Item

from stactools.global_mangrove_watch.commands import create_globalmangrovewatch_command
from stactools.global_mangrove_watch.constants import CHANGE_ASSET_NAME

from . import test_data

command = create_globalmangrovewatch_command(Group())


def test_create_collection(tmp_path: Path) -> None:
    path = str(tmp_path / "collection.json")
    runner = CliRunner()
    result = runner.invoke(command, ["create-collection", path])
    assert result.exit_code == 0, "\n{}".format(result.output)
    collection = Collection.from_file(path)
    collection.validate()


def test_create_item(tmp_path: Path) -> None:
    asset_href = test_data.get_path("data/GMW_N26W082_2020_v3.tif")
    path = str(tmp_path / "item.json")
    runner = CliRunner()
    result = runner.invoke(command, ["create-item", asset_href, path])
    assert result.exit_code == 0, "\n{}".format(result.output)
    item = Item.from_file(path)
    assert not item.assets.get(CHANGE_ASSET_NAME)
    item.validate()


def test_create_item_with_change(tmp_path: Path) -> None:
    asset_href = test_data.get_path("data/GMW_N26W082_2020_v3.tif")
    change_asset_href = test_data.get_path("data/GMW_N26W082_chng_f1996_t2020_v3.tif")
    path = str(tmp_path / "item.json")
    runner = CliRunner()
    result = runner.invoke(
        command,
        ["create-item", asset_href, path, "--change-asset-href", change_asset_href],
    )
    assert result.exit_code == 0, "\n{}".format(result.output)
    item = Item.from_file(path)

    assert item.assets.get(CHANGE_ASSET_NAME)
    item.validate()
