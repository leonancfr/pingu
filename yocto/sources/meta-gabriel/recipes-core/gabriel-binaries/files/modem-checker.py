#!/usr/bin/env python3

import glob
from time import sleep
import logging
import subprocess
from dataclasses import dataclass

_logger = logging.getLogger("Modem-Checker")
_handler = logging.StreamHandler()
_handler.setFormatter(
    logging.Formatter("%(name)s %(levelname)s %(lineno)d: %(message)s")
)
_logger.setLevel(logging.INFO)
_logger.addHandler(_handler)

__version__ = "0.2.1"

MAX_RETRY = 5

TTY_PATH = ""
pattern = '/dev/serial/by-id/usb-*-if02-port0'
matching_paths = glob.glob(pattern)
if matching_paths:
    TTY_PATH = matching_paths[0]


@dataclass
class command_response:
    stdout: str
    stderr: str
    return_code: int


def banner():
    _logger.info("-------------------")
    _logger.info("  Modem Manager")
    _logger.info(f"  version {__version__}")
    _logger.info("-------------------")
    _logger.info("")


def restart_portainer() -> int:
    return run_command(
        command="sudo docker restart portainer_edge_agent"
    ).return_code


def restart_socket_xp() -> int:
    return run_command(command="sudo systemctl restart socketxp").return_code


def internet_ok() -> bool:
    return (
        True
        if run_command(
            command="ping -q -c 1 -W 1 -I modem0 google.com"
        ).return_code
        == 0
        else False
    )


def run_command(command) -> command_response:
    try:
        output = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = output.communicate()
        response: command_response = command_response(
            stdout=stdout.decode("utf-8") if stdout else "",
            stderr=stderr.decode("utf-8") if stderr else "",
            return_code=int(output.returncode),
        )
        return response
    except Exception as e:
        _logger.error(f"Cannot run commnad: {command}. {e}")
        raise Exception(f"Cannot run commnad: {command}. {e}")


def check_usbnet_is_0():
    try:
        command = (
            'echo -ne "AT+QCFG=\\"usbnet\\"\r\n" | microcom -s 115200 -X '
            + TTY_PATH
            + " -t 100"
        )
        response = run_command(command=command).stdout.split("\n")
        for qcfg in range(len(response)):
            if "+QCFG:" in response[qcfg]:
                mode = response[qcfg].split(",")[1]
                if int(mode) == 0:
                    return True
        return False
    except Exception as e:
        _logger.error(f"Fail while reset modem. {e}")
        raise Exception("Reset modem fail")


def get_modem_signal_strength() -> str:
    try:
        command = (
            'echo -ne "AT+CSQ\r\n" | microcom -s 115200 -X '
            + TTY_PATH
            + " -t 100"
        )
        response = run_command(command=command).stdout.split("\n")
        for csq in range(len(response)):
            if "+CSQ:" in response[csq]:
                return int(response[csq][6:].split(",")[0])
        return -1
    except Exception as e:
        _logger.error(f"Error sending AT command. {e}")
        return -2


def configure_usbnet():
    try:
        command = (
            'echo -ne "AT+QCFG=\\"usbnet\\",0\r\n" | microcom -s 115200 -X '
            + TTY_PATH
            + " -t 100"
        )
        response = run_command(command=command).stdout.split("\n")
        for ok in range(len(response)):
            if "OK" in response[ok]:
                return True
        return False
    except Exception as e:
        _logger.error(f"Fail while reset modem. {e}")
        raise Exception("Reset modem fail")


def soft_reset_modem() -> bool:
    try:
        command = (
            'echo -ne "AT+CFUN=1,1\r\n" | microcom -s 115200 -X '
            + TTY_PATH
            + " -t 100"
        )
        response = run_command(command=command).stdout.split("\n")
        for cfun in range(len(response)):
            if "AT+CFUN=1,1" in response[cfun]:
                for ok in range(cfun, len(response)):
                    if "OK" in response[ok]:
                        return True
        return False
    except Exception as e:
        _logger.error(f"Fail while reset modem. {e}")
        raise Exception("Reset modem fail")


def check_modem_config():
    if not check_usbnet_is_0():
        _logger.info("Wrong usbnet. Change usbnet to 0.")
        configure_usbnet()
        soft_reset_modem()
        return False
    return True


def restart_services():
    restart_portainer()
    restart_socket_xp()


def parser_signal_strength(signal):
    if signal < 3:
        return "No signal"
    elif signal < 15:
        return "Marginal"
    elif signal < 20:
        return "Good"
    else:
        return "Excellent"


def handler() -> None:
    device_offline_at_last_check = True
    time = 60
    error_counter = 0

    while True:
        try:
            # Our modem manager just works with usbnet = 0
            if not check_modem_config():
                error_counter = 0
                time = 60  # wait modem restart

            elif internet_ok():
                if device_offline_at_last_check:
                    _logger.info("Modem online.")
                    restart_services()
                    device_offline_at_last_check = False

                sig = get_modem_signal_strength()
                sig_verbose = parser_signal_strength(signal=sig)
                _logger.info(f"Signal strength: {sig_verbose} [{'#'*(sig)}{' '*(31-sig)}] {sig}/31")
                error_counter = 0
                time = 120

            else:  # modem offline
                device_offline_at_last_check = True
                if error_counter == MAX_RETRY:
                    _logger.error("Modem offline, restarting modem")
                    soft_reset_modem()
                    error_counter = 0
                    time = 60
                else:
                    _logger.info(
                        f"Modem offline. Try {error_counter+1}/{MAX_RETRY}"
                        + " before restart modem..."
                    )
                    error_counter += 1
                    time = 15

        except Exception as ex:
            _logger.error(f"Fail. {ex}")
            time = 60
        finally:
            sleep(time)


banner()
handler()
