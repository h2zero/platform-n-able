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

import os
import sys
import subprocess

from platformio.public import PlatformBase


IS_WINDOWS = sys.platform.startswith("win")


class NablePlatform(PlatformBase):

    def is_embedded(self):
        return True

    def configure_default_packages(self, variables, targets):
        upload_protocol = ""
        board = variables.get("board")

        if "erase" in targets:
            self.packages["tool-nrfjprog"]["optional"] = False

        if board:
            upload_protocol = variables.get(
                "upload_protocol",
                self.board_config(board).get("upload.protocol", ""))

            if upload_protocol == "adafruit-nrfutil":
                self.packages["tool-adafruit-nrfutil"]["optional"] = False

            if upload_protocol == "nrfutil":
                try:
                    import nordicsemi
                except ImportError:
                    nrfutil_whl = os.path.join(self.get_dir(), "tools",
                                               "n_able_nrfutil-1.0.0-py3-none-any.whl")
                    try:
                        subprocess.check_call([sys.executable, "-m", "pip", "install", "-U", nrfutil_whl])
                    except subprocess.CalledProcessError as e:
                        sys.stderr.write("Error: Could not install nrfutil : %s" %  e)

        # configure J-LINK tool
        jlink_conds = [
            "jlink" in variables.get(option, "")
            for option in ("upload_protocol", "debug_tool")
        ]
        if variables.get("board"):
            board_config = self.board_config(variables.get("board"))
            jlink_conds.extend([
                "jlink" in board_config.get(key, "")
                for key in ("debug.default_tools", "upload.protocol")
            ])
        jlink_pkgname = "tool-jlink"
        if not any(jlink_conds) and jlink_pkgname in self.packages:
            del self.packages[jlink_pkgname]

        return super().configure_default_packages(variables, targets)

    def get_boards(self, id_=None):
        result = super().get_boards(id_)
        if not result:
            return result
        if id_:
            return self._add_default_debug_tools(result)
        else:
            for key in result:
                result[key] = self._add_default_debug_tools(result[key])
        return result

    def _add_default_debug_tools(self, board):
        debug = board.manifest.get("debug", {})
        upload_protocols = board.manifest.get("upload", {}).get(
            "protocols", [])
        if "tools" not in debug:
            debug["tools"] = {}

        # J-Link / ST-Link / BlackMagic Probe / CMSIS-DAP
        for link in ("blackmagic", "jlink", "stlink", "cmsis-dap"):
            if link not in upload_protocols or link in debug["tools"]:
                continue

            if link == "blackmagic":
                debug["tools"]["blackmagic"] = {
                    "hwids": [["0x1d50", "0x6018"]],
                    "require_debug_port": True
                }

            elif link == "jlink":
                assert debug.get("jlink_device"), (
                    "Missed J-Link Device ID for %s" % board.id)
                debug["tools"][link] = {
                    "server": {
                        "package": "tool-jlink",
                        "arguments": [
                            "-singlerun",
                            "-if", "SWD",
                            "-select", "USB",
                            "-device", debug.get("jlink_device"),
                            "-port", "2331"
                        ],
                        "executable": ("JLinkGDBServerCL.exe"
                                       if IS_WINDOWS else
                                       "JLinkGDBServer")
                    }
                }

            else:
                server_args = [
                    "-s", "$PACKAGE_DIR/scripts",
                    "-f", "interface/%s.cfg" % link
                ]
                if link == "stlink":
                    server_args.extend([
                        "-c",
                        "transport select hla_swd; set WORKAREASIZE 0x4000"
                    ])
                server_args.extend(["-f", "target/%s.cfg" % board.manifest.get("build", "")["mcu"][0:5].lower()])
                debug["tools"][link] = {
                    "server": {
                        "package": "tool-openocd",
                        "executable": "bin/openocd",
                        "arguments": server_args
                    }
                }

            debug["tools"][link]["onboard"] = link in debug.get("onboard_tools", [])
            debug["tools"][link]["default"] = link in debug.get("default_tools", [])

        board.manifest['debug'] = debug
        return board

    def configure_debug_session(self, debug_config):
        if debug_config.speed:
            server_executable = (debug_config.server or {}).get("executable", "").lower()
            if "openocd" in server_executable:
                debug_config.server["arguments"].extend(
                    ["-c", "adapter speed %s" % debug_config.speed]
                )
            elif "jlink" in server_executable:
                debug_config.server["arguments"].extend(
                    ["-speed", debug_config.speed]
                )
