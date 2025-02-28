# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
This project attempts to match the major and minor versions of
[stactools](https://github.com/stac-utils/stactools) and increments the patch
number as needed.

## [Unreleased]

## [0.2.2]

### Fixed

- Pin projection extension to v1.2.0 for backwards compatabality with GDAL's STACIT driver

## [0.2.1]

### Fixed

- Fixed order of coordinates in collection extent

## [0.2.0]

### Changed

- Dropped rio-stac in favor of generating STAC item metadata by hand ([#2](https://github.com/stactools-packages/global-mangrove-watch/pull/2))

## [0.1.0]

### Added

- STAC metadata capabilities for the raster assets ([#1](https://github.com/stactools-packages/global-mangrove-watch/pull/1))

[Unreleased]: <https://github.com/stactools-packages/global-mangrove-watch/compare/0.2.0...main>
[0.2.1]: <https://github.com/stactools-packages/global-mangrove-watch/compare/0.2.0...0.2.1>
[0.2.0]: <https://github.com/stactools-packages/global-mangrove-watch/compare/0.1.0...0.2.0>
[0.1.0]: <https://github.com/stactools-packages/global-mangrove-watch/tree/0.1.0>
