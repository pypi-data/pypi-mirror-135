# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

## [2022.1.0]

### Changed
- switched to calver

## [0.3.2]

### Changed
- quieter warnings

### Fixed
- enum type now defaults to first allowed if current value not in new allowed list
- float widget avoids updating when set while user has focus
- fixed problem with column width by using integer division

## [0.3.1]

### Changed
- removed suprious dependency toml
- removed suprious dependency yaq_traits

## [0.3.0]

### Changed
- complete overhaul based on tree

### Added
- edited signal

### Fixed
- strings disabled properly at startup

## [0.2.0]

### Added
- filepath support

### Changed
- moved to get/set instead of read/write
- migrate to flit

### Fixed
- spacing issues with scroll area

## [0.1.0]

### Added
- initial release

[Unreleased]: https://gitlab.com/yaq/qtypes/-/compare/v2022.1.0...main
[2022.1.0]: https://gitlab.com/yaq/qtypes/-/compare/v0.3.2...v2022.1.0
[0.3.2]: https://gitlab.com/yaq/qtypes/-/compare/v0.3.1...v0.3.2
[0.3.1]: https://gitlab.com/yaq/qtypes/-/compare/v0.3.0...v0.3.1
[0.3.0]: https://gitlab.com/yaq/qtypes/-/compare/v0.2.0...v0.3.0
[0.2.0]: https://gitlab.com/yaq/qtypes/-/compare/v0.1.0...v0.2.0
[0.1.0]: https://gitlab.com/yaq/qtypes/-/tags/v0.1.0
