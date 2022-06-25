# Development platform for ARM BLE devices supported by [Apache NimBLE](https://github.com/apache/mynewt-nimble) for [PlatformIO](https://platformio.org)

[![Build Status](https://github.com/platformio/platform-nordicnrf51/workflows/Examples/badge.svg)](https://github.com/platformio/platform-nordicnrf51/actions)

Apache NimBLE is an open-source Bluetooth 5.1 stack (both Host & Controller) that completely replaces the proprietary SoftDevice on Nordic chipsets. It is part of Apache Mynewt project. This platform aims to provide the use of the [NimBLE-Arduino library](https://github.com/h2zero/NimBLE-Arduino) for Nordic and other ARM based devices that are supported by the underlying NimBLE stack, using the [n-able Arduino core](https://github.com/h2zero/n-able).


# Usage

1. [Install PlatformIO](https://platformio.org)
2. Create PlatformIO project and configure a platform option in [platformio.ini](http://docs.platformio.org/page/projectconf.html) file:

## Stable version

```ini
[env]
platform = n-able
framework = arduino
platform_packages = framework-n-able@https://github.com/h2zero/n-able
board = ...
...
```
