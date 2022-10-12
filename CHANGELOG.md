# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres
to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!--
Types of changes

    `Added` for new features.
    `Changed` for changes in existing functionality.
    `Deprecated` for soon-to-be removed features.
    `Removed` for now removed features.
    `Fixed` for any bug fixes.
    `Security` in case of vulnerabilities.
-->

## Unreleased

## v1.7.1

Sync with sila_cetoni v1.7.1 release

### Fixed

- Typo in pyproject.toml

## v1.7.0

Sync with sila_cetoni v1.7.0

### Changed

- Bump required sila2 version to v0.10.0

## v1.6.0

Sync with sila_cetoni v1.6.0

## v1.5.0

Sync with sila_cetoni v1.5.0

## v1.4.0

Sync with sila_cetoni v1.4.0

## v1.3.0

Sync with sila_cetoni v1.3.0

### Fixed

- Properly call `super().stop()` in the feature implementation classes

## v1.2.0

Sync with sila_cetoni v1.2.0


## v1.1.0

### Changed

- Bump sila2 to v0.8.2

## v1.0.0

First release of sila_cetoni

This is the core plugin which contains core SiLA 2 features that are used by multiple devices

### Added

- SystemStatusProvider feature and feature implementation
- ShutdownController feature
- BatteryService feature and feature implementation
- Device driver interface for battery-powered devices
- Battery device driver implementation for the CETONI MobDos (mobile dosing unit)
