# Copyright 2014-present PlatformIO <contact@platformio.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Arduino

Arduino Wiring-based Framework allows writing cross-platform software to
control devices attached to a wide range of Arduino boards to create all
kinds of creative coding, interactive objects, spaces or physical experiences.
"""

from os import listdir
from os.path import isdir, join

from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()
platform = env.PioPlatform()
board = env.BoardConfig()

FRAMEWORK_DIR = platform.get_package_dir("framework-n-able")
assert isdir(FRAMEWORK_DIR)

env.Append(
    ASFLAGS=["-x", "assembler-with-cpp"],

    CFLAGS=["-std=gnu11"],

    CCFLAGS=[
        "-Os",  # optimize for size
        "-ffunction-sections",  # place each function in its own section
        "-fdata-sections",
        "-Wall",
        "-mthumb",
        "-nostdlib",
        "--param",
        "max-inline-insns-single=500"
    ],

    CXXFLAGS=[
        "-fno-rtti",
        "-fno-exceptions",
        "-std=gnu++11",
        "-fno-threadsafe-statics"
    ],

    CPPDEFINES=[
        ("F_CPU", board.get("build.f_cpu")),
        ("ARDUINO", 10805),
        # For compatibility with sketches designed for AVR@16 MHz (see SPI lib)
        "ARDUINO_ARCH_NRF5",
        "NRF5",
        ("RIOT_VERSION", 1),
        "%s" % "NRF52_SERIES" if "NRF52" in board.get("build.mcu", "").upper() else "NRF51",
        "%s" % board.get("build.mcu", "").upper()
    ],

    LIBPATH=[
        join(FRAMEWORK_DIR, "cores", board.get("build.core"),
             "nordic", "linker")
    ],

    CPPPATH=[
        join(FRAMEWORK_DIR, "cores", board.get("build.core")),
        join(FRAMEWORK_DIR, "cores", board.get("build.core"),
             "nordic", "nrfx"),
        join(FRAMEWORK_DIR, "cores", board.get("build.core"),
             "nordic", "nrfx", "drivers", "include"),
        join(FRAMEWORK_DIR, "cores", board.get("build.core"),
             "nordic", "nrfx", "drivers", "src"),
        join(FRAMEWORK_DIR, "cores", board.get("build.core"),
             "nordic", "nrfx", "hal"),
        join(FRAMEWORK_DIR, "cores", board.get("build.core"),
             "nordic", "nrfx", "mdk"),
        join(FRAMEWORK_DIR, "cores", board.get("build.core"),
             "nordic", "nrfx", "soc"),
        join(FRAMEWORK_DIR, "cores", board.get("build.core"),
             "CMSIS", "Include"),
        join(FRAMEWORK_DIR, "cores", board.get("build.core"),
            "nimble_config"),
        join(FRAMEWORK_DIR, "cores", board.get("build.core"),
            "BLEBond_nvs"),
        join(FRAMEWORK_DIR, "cores", board.get("build.core"),
             "FC_Store"),
        join(FRAMEWORK_DIR, "cores", board.get("build.core"),
             "TinyUSB"),
        join(FRAMEWORK_DIR, "cores", board.get("build.core"),
             "TinyUSB", "Adafruit_TinyUSB_ArduinoCore"),
        join(FRAMEWORK_DIR, "cores", board.get("build.core"),
             "TinyUSB", "Adafruit_TinyUSB_ArduinoCore", "tinyusb", "src")
    ],

    LINKFLAGS=[
        "-Os",
        "-Wl,--gc-sections",
        "-mthumb",
        "--specs=nano.specs",
        "--specs=nosys.specs",
        "-Wl,--check-sections",
        "-Wl,--unresolved-symbols=report-all",
        "-Wl,--warn-common",
        "-Wl,--warn-section-align"
    ],

    LIBSOURCE_DIRS=[join(FRAMEWORK_DIR, "libraries")],

    LIBS=["m"]
)

if "BOARD" in env:
    env.Append(
        CCFLAGS=[
            "-mcpu=%s" % env.BoardConfig().get("build.cpu")
        ],
        LINKFLAGS=[
            "-mcpu=%s" % env.BoardConfig().get("build.cpu")
        ]
    )

if board.get("build.cpu") == "cortex-m4":
    env.Append(
        ASFLAGS=[
            "-mfloat-abi=hard",
            "-mfpu=fpv4-sp-d16",
        ],
        CCFLAGS=[
            "-mfloat-abi=hard",
            "-mfpu=fpv4-sp-d16"
        ],
        LINKFLAGS=[
            "-mfloat-abi=hard",
            "-mfpu=fpv4-sp-d16"
        ]
    )

if "build.usb_product" in env.BoardConfig():
    env.Append(
        CPPDEFINES=[
            "USBCON",
            "USE_TINYUSB",
            ("USB_VID", board.get("build.hwids")[0][0]),
            ("USB_PID", board.get("build.hwids")[0][1]),
            ("USB_PRODUCT", '\\"%s\\"' % board.get("build.usb_product", "").replace('"', "")),
            ("USB_MANUFACTURER", '\\"%s\\"' % board.get("vendor", "").replace('"', ""))
        ]
    )

env.Append(
    ASFLAGS=env.get("CCFLAGS", [])[:]
)

cpp_defines = env.Flatten(env.get("CPPDEFINES", []))

if not board.get("build.ldscript", ""):
    # if SoftDevice is not specified use default ld script from the framework
    env.Replace(LDSCRIPT_PATH=board.get("build.arduino.ldscript", ""))

#
# Target: Build Core Library
#

libs = []

if "build.variant" in board:
    env.Append(CPPPATH=[
        join(FRAMEWORK_DIR, "variants", board.get("build.variant"))
    ])

    env.BuildSources(
        join("$BUILD_DIR", "FrameworkArduinoVariant"),
        join(FRAMEWORK_DIR, "variants",
                board.get("build.variant")))

libs.append(
    env.BuildLibrary(
        join("$BUILD_DIR", "FrameworkArduino"),
        join(FRAMEWORK_DIR, "cores", board.get("build.core"))))

env.Prepend(LIBS=libs)
