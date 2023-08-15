# Changelog

All notable changes to this hyprpy will be documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.2] - 2023-08-15

### Added

- Sockets now provide methods for better interaction with the underlying unix sockets

### Changed

- Components no longer proxy access to data attributes using `__getattr__`, keep them as direct instance attributes
- Removed class variable `connection_timeout_seconds` from `EventSocket` and `CommandSocket`

### Fixed

- A JSONParseError occurring when many windows are open
- Polling of the EventSocket in `Instance.watch()` replaced in favour of a `select` syscall.

## [0.1.1] - 2023-08-14

### Changed

- rename `EventSocket` and `CommandSocket` class variable from `conncection_timeout_seconds` to `connection_timeout_seconds`

## [0.1.0] - 2023-08-14

### Added

- Component classes:
    - Instance
    - Monitor
    - Workspace
    - Window
- Data model classes:
    - InstanceData
    - MonitorData
    - WorkspaceData
    - WindowData
- Signals
- Sockets
- README
- sphinx documentation

## [Unreleased]

[0.1.2]: https://github.com/ulinja/hyprpy/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/ulinja/hyprpy/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/ulinja/hyprpy/releases/tag/v0.1.0
