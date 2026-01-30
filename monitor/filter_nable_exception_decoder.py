#!/usr/bin/env python3
# Copyright (c) 2014-present PlatformIO <contact@platformio.org>
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
Nable backtrace decoder monitor filter.

This filter automatically decodes hard fault backtraces using addr2line,
similar to the ESP32 exception decoder.

Usage in platformio.ini:
  [env:seeed_xiao_nrf52840_sense]
  monitor_filters = nable_exception_decoder
"""

import os
import re
import subprocess
import sys

from platformio.exception import PlatformioException
from platformio.public import (
    DeviceMonitorFilterBase,
    load_build_metadata,
)

# By design, __call__ is called inside miniterm and we can't pass context to it.
# pylint: disable=attribute-defined-outside-init

IS_WINDOWS = sys.platform.startswith("win")

class NableExceptionDecoder(DeviceMonitorFilterBase):
    """Nable backtrace decoder filter."""

    NAME = "nable_exception_decoder"

    # Pattern to match hex addresses in backtrace format like "  #0: 0x12345678"
    ADDR_PATTERN = re.compile(r"(\s+#\d+:\s+)(0x[0-9a-fA-F]{8})")

    def __call__(self):
        """Initialize the filter."""
        self.buffer = ""
        self.backtrace_buffer = ""
        self.in_backtrace = False
        self.firmware_path = None
        self.addr2line_path = None
        self.enabled = self.setup_paths()

        if not self.enabled:
            sys.stderr.write(
                "%s: failed to find addr2line or firmware. Backtrace decoding disabled.\n"
                % self.__class__.__name__
            )

        if self.config.get("env:" + self.environment, "build_type") != "debug":
            sys.stderr.write(
                """
Please build project in debug configuration to get more details about an exception.
See https://docs.platformio.org/page/projectconf/build_configurations.html
"""
            )

        return self

    def setup_paths(self):
        """Setup paths to firmware and addr2line tool."""
        self.project_dir = os.path.abspath(self.project_dir)
        try:
            data = load_build_metadata(self.project_dir, self.environment, cache=True)

            self.firmware_path = data["prog_path"]
            if not os.path.isfile(self.firmware_path):
                sys.stderr.write(
                    "%s: firmware at %s does not exist, rebuild the project?\n"
                    % (self.__class__.__name__, self.firmware_path)
                )
                return False

            cc_path = data.get("cc_path", "")
            if "eabi-gcc" in cc_path:
                path = cc_path.replace("eabi-gcc", "eabi-addr2line")
                if os.path.isfile(path):
                    self.addr2line_path = path
                    return True

        except PlatformioException as e:
            sys.stderr.write(
                "%s: disabling, exception while looking for addr2line: %s\n"
                % (self.__class__.__name__, e)
            )
            return False

        sys.stderr.write(
            "%s: disabling, failed to find addr2line.\n" % self.__class__.__name__
        )
        return False

    def rx(self, text):
        """Process received text and decode backtraces."""
        if not self.enabled:
            return text

        output = ""
        lines = text.splitlines(True)

        for line in lines:
            ended = line.endswith("\n") or line.endswith("\r")
            raw = line.rstrip("\r\n") if ended else line
            ending = line[len(raw):] if ended else ""

            # Detect start of backtrace
            if "Call Stack Backtrace:" in raw:
                self.in_backtrace = True
                self.backtrace_buffer = ""
                output += raw + (ending or "\n")
                continue

            # Detect end of backtrace
            if self.in_backtrace and "======" in raw:
                self.in_backtrace = False
                # Process complete backtrace
                decoded = self.process_backtrace(self.backtrace_buffer)
                if decoded:
                    output += decoded
                output += raw + (ending or "\n")
                self.backtrace_buffer = ""
                continue

            # Buffer backtrace lines
            if self.in_backtrace:
                if ended:
                    self.backtrace_buffer += raw + "\n"
                else:
                    self.backtrace_buffer += raw
            else:
                output += raw + ending

        return output

    def process_backtrace(self, backtrace_text):
        """Process complete backtrace and decode all addresses."""
        result = ""
        lines = backtrace_text.split("\n")

        for line in lines:
            m = self.ADDR_PATTERN.search(line)
            if m is not None:
                decoded = self.build_backtrace(m.group(1), m.group(2))
                if decoded:
                    result += decoded
            elif line.strip():
                # Preserve non-address informational lines inside the backtrace
                result += line + "\n"

        return result

    def tx(self, text):
        """Process transmitted text (pass-through)."""
        return text

    def build_backtrace(self, prefix, addr):
        """Build a formatted backtrace from a single address."""
        enc = "mbcs" if IS_WINDOWS else "utf-8"
        args = [self.addr2line_path, "-fipC", "-e", self.firmware_path]

        try:
            output = (
                subprocess.check_output(args + [addr])
                .decode(enc)
                .strip()
            )

            # newlines happen with inlined methods
            output = output.replace("\n", "\n     ")

            output = self.strip_project_dir(output)
            trace = "%s%s in %s\n" % (prefix, addr, output)
            return trace

        except subprocess.CalledProcessError as e:
            sys.stderr.write(
                "%s: failed to call %s: %s\n"
                % (self.__class__.__name__, self.addr2line_path, e)
            )
            return "%s%s in ??:?\n" % (prefix, addr)

    def strip_project_dir(self, trace):
        """Remove project directory path from trace for cleaner output."""
        while True:
            idx = trace.find(self.project_dir)
            if idx == -1:
                break
            trace = trace[:idx] + trace[idx + len(self.project_dir) + 1:]

        return trace
