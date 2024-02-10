#!/usr/bin/env python3
""" This script will make sure the socketxp service is running,
 and check if there are new socketxp configuration files on
 the common folder."""

import json
import logging
import subprocess
import time
import random
import filecmp
from os import stat_result
from pathlib import Path
from typing import Callable, Optional


_logger = logging.getLogger("SocketXP Handler")
_handler = logging.StreamHandler()
_handler.setFormatter(
    logging.Formatter("%(asctime)s:%(name)s:%(levelname)s:%(message)s")
)
_logger.setLevel(logging.INFO)
_logger.addHandler(_handler)

_restart_counter = 0
_fail_counter = 0
_subdomain = ""


SOCKET_XP_BIN_DIR: Path = Path("/usr/local/bin")
DEVICE_KEY_DIR: Path = Path("/var/lib/socketxp")
CONFIG_JSON_DIR: Path = Path("/etc/socketxp")
DEVICE_KEY_FILENAME: Path = DEVICE_KEY_DIR / "device.key"
CONFIG_JSON_FILENAME: Path = CONFIG_JSON_DIR / "config.json"

COMMON_PATH = Path("/home/gabriel/.apps/common")

DEVICE_KEY_FILENAME_SELFPROV: Path = COMMON_PATH / "device.key"
CONFIG_JSON_FILENAME_SELFPROV: Path = COMMON_PATH / "config.json"

METRIC_NAME = "socketxp"

files_timestamps = {
    "device.key": {
        "path_selfprov": DEVICE_KEY_FILENAME_SELFPROV,
        "path": DEVICE_KEY_FILENAME,
        "last_timestamp": None,
    },
    "config.json": {
        "path_selfprov": CONFIG_JSON_FILENAME_SELFPROV,
        "path": CONFIG_JSON_FILENAME,
        "last_timestamp": None,
    },
}


def get_socketxp_subdomain() -> str:
    global _subdomain

    if not _subdomain and CONFIG_JSON_FILENAME.exists():

        with open(CONFIG_JSON_FILENAME, "r") as f:
            config_json = json.load(f)

            if "tunnels" not in config_json:
                raise RuntimeError("SocketXP tunnels not configured.")

            for tunnel in config_json["tunnels"]:
                if "subdomain" in tunnel:
                    _subdomain = tunnel["subdomain"]

        if not _subdomain:
            _logger.error("Invalid SocketXP configuration")

    return _subdomain


def sudo_mkdir(dirname: Path) -> None:
    shell_cmd(
        f"sudo mkdir -p {dirname}",
        error_msg=f"Error: cannot create socketxp folder: {dirname}.",
        success_msg=f"Folder {dirname} created.",
        on_error=shell_exit_error,
    )


def ensure_socket_xp_directories_exist() -> None:
    if not DEVICE_KEY_DIR.exists():
        sudo_mkdir(DEVICE_KEY_DIR)
    if not CONFIG_JSON_DIR.exists():
        sudo_mkdir(CONFIG_JSON_DIR)


def exist_socket_xp_cfg_files() -> bool:
    exist = True
    if (
        not DEVICE_KEY_FILENAME.exists()
        and not DEVICE_KEY_FILENAME_SELFPROV.exists()
    ):
        _logger.info("File device.key doesn't exist")
        exist = False
    if (
        not CONFIG_JSON_FILENAME.exists()
        and not CONFIG_JSON_FILENAME_SELFPROV.exists()
    ):
        _logger.info("File config.json doesn't exist")
        exist = False
    return exist


def sleep_interval() -> None:
    time.sleep(5 * 60)


def small_sleep_interval() -> None:
    time.sleep(60)


def get_file_timestamp(file_path: Path) -> stat_result:
    return file_path.stat()


def shell_cmd(
    cmd: str,
    success_msg: Optional[str] = None,
    error_msg: Optional[str] = None,
    on_success: Optional[Callable[[], None]] = None,
    on_error: Optional[Callable[[], None]] = None,
) -> bool:
    """wraper using subprocess.run() to handle shell commands"""
    try:
        subprocess.run(cmd, shell=True, check=True, timeout=60)
        if success_msg:
            _logger.info(success_msg)
        if on_success:
            on_success()
        return True
    except subprocess.CalledProcessError:
        if error_msg:
            _logger.error(error_msg)
        if on_error:
            on_error()
        return False


def shell_exit_error() -> None:
    """Wrapper for exit on error when running shell commands"""
    raise RuntimeError


def stop_socketxp():
    shell_cmd(
        "sudo systemctl stop socketxp",
        error_msg="Error: SocketXP Service stop failed!",
        success_msg="SocketXP Service Stopped",
    )


def stop_socketxp_if_started():
    shell_cmd(
        "systemctl is-active socketxp",
        error_msg="SocketXP already stopped",
        success_msg="Stopping SocketXP",
        on_success=stop_socketxp,
    )


def start_and_enable_socketxp():
    shell_cmd(
        "sudo systemctl start socketxp",
        error_msg="Error: SocketXP Service start failed!",
        success_msg="SocketXP Service Started",
        on_error=shell_exit_error,
    )

    shell_cmd(
        "sudo systemctl enable socketxp",
        error_msg="Error: SocketXP Service enable failed!",
        success_msg="Enabled SocketXP Service to start always on reboot",
        on_error=shell_exit_error,
    )


def restart_socketxp():
    global _restart_counter
    _restart_counter += 1
    shell_cmd(
        "sudo systemctl restart socketxp",
        error_msg="Error: SocketXP Service restart failed!",
        success_msg=f"SocketXP Service Restarted ({_restart_counter})",
        on_error=shell_exit_error,
    )


def reload_daemon():
    shell_cmd(
        "sudo systemctl daemon-reload",
        success_msg="SocketXP Service Daemon-Reload Completed",
        error_msg="Error: SocketXP Service daemon-reload failed!",
        on_error=shell_exit_error,
    )


def install_socket_xp():
    shell_cmd(
        f"sudo {SOCKET_XP_BIN_DIR}/socketxp service install --config {CONFIG_JSON_FILENAME}",
        error_msg="Error: SocketXP Service Install failed!",
        success_msg="SocketXP Service Install Completed",
        on_error=shell_exit_error,
    )

    reload_daemon()


def ensure_socket_xp_running():
    global _fail_counter
    is_active = shell_cmd(
        "systemctl is-active socketxp",
        error_msg="Service socketxp was not active",
    )

    if not is_active:
        start_and_enable_socketxp()


def ensure_socket_xp_installed():
    shell_cmd(
        "systemctl | grep socketxp.service",
        error_msg="Service socketxp doesn't exist",
        on_error=install_socket_xp,
    )


def copy_new_cfg_files() -> bool:
    has_new_file = False

    for filename, cfg in files_timestamps.items():
        cfg_path = cfg["path"]
        cfg_path_selfprov = cfg["path_selfprov"]
        last_timestamp = cfg["last_timestamp"]

        if not cfg_path_selfprov.exists():
            continue

        new_timestamp = get_file_timestamp(cfg_path_selfprov)

        if not last_timestamp:
            _logger.info("Loading timestamp to %s", filename)
            cfg["last_timestamp"] = new_timestamp
            if not cfg_path.exists() or not filecmp.cmp(
                cfg_path, cfg_path_selfprov
            ):
                has_new_file = True

        elif last_timestamp != new_timestamp:
            _logger.info("Found newer %s", filename)
            cfg["last_timestamp"] = new_timestamp
            has_new_file = True

        if has_new_file:
            _logger.info("Copy %s -> %s", cfg_path_selfprov, cfg_path)
            shell_cmd(
                f"sudo cp -p {cfg_path_selfprov} {cfg_path}",
                error_msg="Copy failed.",
                on_error=shell_exit_error,
            )

    return has_new_file


def handle_socket_xp() -> bool:
    ensure_socket_xp_directories_exist()

    if not exist_socket_xp_cfg_files():
        # socketxp is probably not enabled on backend,
        # no need to install and run socketxp
        return False

    ensure_socket_xp_installed()

    if copy_new_cfg_files():
        stop_socketxp_if_started()

    ensure_socket_xp_running()

    return True


if __name__ == "__main__":
    _logger.info("Starting socketxp handler")

    while True:
        try:
            if handle_socket_xp():
                sleep_interval()
                continue
        except Exception as ex:
            _logger.error(ex)
        small_sleep_interval()
