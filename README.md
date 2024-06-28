# Development platform for ARM BLE devices supported by [Apache NimBLE](https://github.com/apache/mynewt-nimble) for [PlatformIO](https://platformio.org)

[![Examples](https://github.com/h2zero/platform-n-able/actions/workflows/examples.yml/badge.svg?branch=n-able)](https://github.com/h2zero/platform-n-able/actions/workflows/examples.yml)

Apache NimBLE is an open-source Bluetooth 5.1 stack (both Host & Controller) that completely replaces the proprietary SoftDevice on Nordic chipsets and is part of Apache Mynewt project. This platform aims to provide the use of the [NimBLE-Arduino library](https://github.com/h2zero/NimBLE-Arduino) for Nordic and other ARM based devices that are supported by the underlying NimBLE stack, using the [n-able Arduino core](https://github.com/h2zero/n-able-Arduino).


# Usage

1. [Install PlatformIO](https://platformio.org)
2. Create PlatformIO project and configure a platform option in [platformio.ini](http://docs.platformio.org/page/projectconf.html) file:

```ini
[env]
platform = https://github.com/h2zero/platform-n-able.git@^1.0.0
framework = arduino
lib_deps = h2zero/NimBLE-Arduino@^1.4.0
board = ...
...
```

## Supported boards

### nRF52840
 * [Generic nRF52840 MCU](https://www.nordicsemi.com/Products/nRF52840)
 * [Nordic nRF52840 DK](https://www.nordicsemi.com/Products/Development-hardware/nRF52840-DK)
 * [Nordic nRF52840 Dongle](https://www.nordicsemi.com/Products/Development-hardware/nrf52840-dongle)
 * [Adafruit CLUE nRF52840](https://www.adafruit.com/product/4500)
 * [Adafruit Circuit Playground Bluefruit](https://www.adafruit.com/product/4333)
 * [Adafruit Feather nRF52840 Express](https://www.adafruit.com/product/4062)
 * [Adafruit Feather nRF52840 Sense](https://www.adafruit.com/product/4516)
 * [Adafruit ItsyBitsy nRF52840 Express](https://www.adafruit.com/product/4481)
 * [Ebyte E104-BT5040U](https://www.ebyte.com/en/product-view-news.html?id=1185)

### nRF52833
 * [Generic nRF52833 MCU](https://www.nordicsemi.com/Products/nRF52833)
 * [Nordic nRF52833 DK](https://www.nordicsemi.com/Products/Development-hardware/nRF52833-DK)
 * [BBC micro:bit v2](https://microbit.org/new-microbit/)

### nRF52832
 * [Generic nRF52832 MCU](https://www.nordicsemi.com/Products/nRF52832)
 * [Nordic nRF52832 DK](https://www.nordicsemi.com/eng/Products/Bluetooth-Smart-Bluetooth-low-energy/nRF52-DK)
 * [RedBear Blend 2](https://github.com/redbear/nRF5x#blend-2)
 * [RedBear Nano 2](https://github.com/redbear/nRF5x#ble-nano-2)
 * [Bluey](https://github.com/electronut/ElectronutLabs-bluey)
 * [hackaBLE](https://github.com/electronut/ElectronutLabs-hackaBLE)
 * [hackaBLE_v2](https://github.com/electronut/ElectronutLabs-hackaBLE)
 * [Adafruit Feather nRF52832](https://www.adafruit.com/product/3406)
 * [Ebyte E104-BT5032A-TB](https://www.ebyte.com/en/product-view-news.html?id=956)

### nRF52810
 * [Generic nRF52810 MCU](https://www.nordicsemi.com/Products/nRF52810)

### nRF51
 * [Generic nRF51 MCU](https://www.nordicsemi.com/eng/Products/Bluetooth-low-energy/nRF51822)
 * [BBC micro:bit](https://microbit.org)
 * [Calliope mini](https://calliope.cc/en)
 * [Bluz DK](http://bluz.io)
 * [Nordic Semiconductor nRF51822 Development Kit](https://www.nordicsemi.com/eng/Products/Bluetooth-low-energy/nRF51822-Development-Kit)
 * [Nordic Semiconductor NRF51 Smart Beacon Kit](https://www.nordicsemi.com/eng/Products/Bluetooth-low-energy/nRF51822-Bluetooth-Smart-Beacon-Kit)
 * [Nordic Semiconductor NRF51 Dongle](http://www.nordicsemi.com/eng/Products/nRF51-Dongle)
 * [OSHChip](http://www.oshchip.org/)
 * [RedBearLab BLE Nano](http://redbearlab.com/blenano/)
 * [RedBearLab nRF51822](http://redbearlab.com/redbearlab-nrf51822/)
 * [Waveshare BLE400](http://www.waveshare.com/wiki/BLE400)
 * [ng-beacon](https://github.com/urish/ng-beacon)
 * [TinyBLE](https://www.seeedstudio.com/Seeed-Tiny-BLE-BLE-%2B-6DOF-Mbed-Platform-p-2268.html)
 * [Sino:bit](http://sinobit.org)

## Tools
Available options for uploading firmware are: JLink, Black Magic Probe, ST-Link, cmsis-dap, nrfjprog, adafruit-nrfutil , and nrfutil (nordic).

## Debugging
Supported debugging tools are: JLink, Black Magic Probe, ST-Link, and cmsis-dap. Both on-board and external debug tools are supported with 1-click debugging.
