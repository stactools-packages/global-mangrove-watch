# stactools-global-mangrove-watch

[![PyPI](https://img.shields.io/pypi/v/stactools-global-mangrove-watch?style=for-the-badge)](https://pypi.org/project/stactools-global-mangrove-watch/)
![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/stactools-packages/global-mangrove-watch/continuous-integration.yml?style=for-the-badge)

- Name: global-mangrove-watch
- Package: `stactools.global_mangrove_watch`
- [stactools-global-mangrove-watch on PyPI](https://pypi.org/project/stactools-global-mangrove-watch/)
- Owner: @githubusername
- [Dataset homepage](http://example.com)
- STAC extensions used:
  - [proj](https://github.com/stac-extensions/projection/)
- Extra fields:
  - `global-mangrove-watch:custom`: A custom attribute
- [Browse the example in human-readable form](https://radiantearth.github.io/stac-browser/#/external/raw.githubusercontent.com/stactools-packages/global-mangrove-watch/main/examples/collection.json)
- [Browse a notebook demonstrating the example item and collection](https://github.com/stactools-packages/global-mangrove-watch/tree/main/docs/example.ipynb)

A short description of the package and its usage.

## STAC examples

- [Collection](examples/collection.json)
- [Item](examples/item/item.json)

## Installation

```shell
pip install stactools-global-mangrove-watch
```

## Command-line usage

Description of the command line functions

```shell
stac global-mangrove-watch create-item source destination
```

Use `stac global-mangrove-watch --help` to see all subcommands and options.

## Contributing

We use [pre-commit](https://pre-commit.com/) to check any changes.
To set up your development environment:

```shell
uv sync
uv run pre-commit install
```

To check all files:

```shell
uv run pre-commit run --all-files
```

To run the tests:

```shell
uv run pytest -vv
```

If you've updated the STAC metadata output, update the examples:

```shell
uv run scripts/update-examples
```
