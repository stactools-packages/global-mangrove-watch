import logging
from typing import Optional

import click
from click import Command, Group

from stactools.global_mangrove_watch import stac

logger = logging.getLogger(__name__)


def create_globalmangrovewatch_command(cli: Group) -> Command:
    """Creates the stactools-global-mangrove-watch command line utility."""

    @cli.group(
        "globalmangrovewatch",
        short_help=("Commands for working with stactools-global-mangrove-watch"),
    )
    def globalmangrovewatch() -> None:
        pass

    @globalmangrovewatch.command(
        "create-collection",
        short_help="Creates a STAC collection",
    )
    @click.argument("destination")
    def create_collection_command(destination: str) -> None:
        """Creates a STAC Collection

        Args:
            destination: An HREF for the Collection JSON
        """
        collection = stac.create_collection()
        collection.set_self_href(destination)
        collection.save_object()

    @globalmangrovewatch.command("create-item", short_help="Create a STAC item")
    @click.argument("cog_asset_href")
    @click.argument("destination")
    @click.option("--change-asset-href", type=str)
    def create_item_command(
        cog_asset_href: str, destination: str, change_asset_href: Optional[str] = None
    ) -> None:
        """Creates a STAC Item

        Args:
            cog_asset_href: HREF of the COG asset associated with the Item
            destination: An HREF for the STAC Item
            change_asset_href: Optional HREF to the change asset associated with the
              Item
        """
        item = stac.create_item(
            cog_asset_href=cog_asset_href,
            change_asset_href=change_asset_href,
        )
        item.save_object(dest_href=destination)

    return globalmangrovewatch
