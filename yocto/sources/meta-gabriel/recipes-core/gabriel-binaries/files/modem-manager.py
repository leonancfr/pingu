import logging
import subprocess
from dataclasses import dataclass
import os
import glob

_logger = logging.getLogger("Modem-Manager")
_handler = logging.StreamHandler()
_handler.setFormatter(
    logging.Formatter("%(name)s %(levelname)s %(lineno)d: %(message)s")
)
_logger.setLevel(logging.INFO)
_logger.addHandler(_handler)

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
        _logger.error(f"Cannot run command: {command}. {e}")
        raise Exception(f"Cannot run command: {command}. {e}")


def get_SIM_operator() -> str:
    try:
        command = (
            'echo -ne "AT+QSPN\r\n" | microcom -s 115200 -X '
            + TTY_PATH
            + " -t 100"
        )
        response = run_command(command=command).stdout.split('\n')
        for qspn in range(len(response)):
            if "+QSPN:" in response[qspn]:
                for ok in range(qspn, len(response)):
                    if "OK" in response[ok]:
                        return response[qspn][7:].split(",")[2]
        raise Exception("Mobile operator info not founded")
    except Exception as e:
        _logger.error(f"Fail while check mobile operator of SIM card. {e}")
        raise (Exception("Mobile operator info not found"))


try:
    apn = None
    sim = get_SIM_operator()
    _logger.info(f"Operator: {sim}")
    if "telecall" in sim.lower():
        apn = "telecall.com.br"
    elif "arqia" in sim.lower():
        apn = "bl.arqia.br"
    else:
        _logger.info(f"Mobile operator {sim} don't have a registered APN.")

    if apn is not None:
        _logger.info(f"Starting Quectel modem-manager with apn: {apn}")
        exit(os.system("/opt/quectel/bin/quectel-CM -s " + apn))

except Exception as ex:
    _logger.error(f"Service will close: {ex}")
    exit(1)
