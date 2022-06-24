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


## v1.0.0

First release of sila_cetoni

This is the core plugin which contains core SiLA 2 features that are used by multiple devices

### Added
- SystemStatusProvider feature and feature implementation
- ShutdownController feature
- BatteryService feature and feature implementation
- Device driver interface for battery-powered devices
- Battery device driver implementation for the CETONI MobDos (mobile dosing unit)