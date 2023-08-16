# Changelog

All notable changes to this hyprpy will be documented here.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [0.1.4] - 2023-08-14

### Changed

- Signal data now returns parsed event data (component IDs) in favour of instaniated Components, as that sometimes lead to returning `None` type objects.

## [0.1.3] - 2023-08-15

### Added

- Methods `Instance.get_active_workspace()` and `Instance.get_active_window()`

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

[0.1.4]: https://github.com/ulinja/hyprpy/compare/v0.1.3...v0.1.4
[0.1.3]: https://github.com/ulinja/hyprpy/compare/v0.1.2...v0.1.3
[0.1.2]: https://github.com/ulinja/hyprpy/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/ulinja/hyprpy/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/ulinja/hyprpy/releases/tag/v0.1.0
