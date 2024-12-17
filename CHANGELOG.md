# Changelog

All notable changes to hyprpy will be documented here.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [0.1.10] - 2024-12-17

### Fixed

- Fixed a bug where importing the hyprpy module without the `$HYPRLAND_INSTANCE_SIGNATURE` being set causes a `hyprpy.utils.shell.EnvironmentException` at import time.

## [0.1.9] - 2024-12-12

### Fixed

- Fixed a data parsing error caused by an upstream change to Hyprland wherein the `fullscreenMode` and `fakeFullscreen` attributes were removed from window objects

## [0.1.8] - 2024-06-18

### Fixed

- Fixed Instance.watch() crashing when special workspace changes on newer versions of Hyprland

## [0.1.7] - 2024-05-25

### Fixed

- Fixed a hyprpy crash during Socket initialization on newer Hyprland versions caused by upstream changes

## [0.1.6] - 2024-05-11

### Added

- Method `Instance.dispatch()`

## [0.1.5] - 2023-09-13

### Fixed

- Broken link to documentation on PyPi repaired
- Incorrect example code in documentation recitified

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

[0.1.10]: https://github.com/ulinja/hyprpy/compare/v0.1.9...v0.1.10
[0.1.9]: https://github.com/ulinja/hyprpy/compare/v0.1.8...v0.1.9
[0.1.8]: https://github.com/ulinja/hyprpy/compare/v0.1.7...v0.1.8
[0.1.7]: https://github.com/ulinja/hyprpy/compare/v0.1.6...v0.1.7
[0.1.6]: https://github.com/ulinja/hyprpy/compare/v0.1.5...v0.1.6
[0.1.5]: https://github.com/ulinja/hyprpy/compare/v0.1.4...v0.1.5
[0.1.4]: https://github.com/ulinja/hyprpy/compare/v0.1.3...v0.1.4
[0.1.3]: https://github.com/ulinja/hyprpy/compare/v0.1.2...v0.1.3
[0.1.2]: https://github.com/ulinja/hyprpy/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/ulinja/hyprpy/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/ulinja/hyprpy/releases/tag/v0.1.0
