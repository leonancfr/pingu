#!/usr/bin/env python3

import glob
import json
import socket
import subprocess
import time
import logging

_logger = logging.getLogger("HardwareBridge-Handler")
_handler = logging.StreamHandler()
_handler.setFormatter(
    logging.Formatter("%(name)s %(levelname)s %(lineno)d: %(message)s")
)
_logger.setLevel(logging.INFO)
_logger.addHandler(_handler)

__version__ = "0.1.10"

SOCKET_PATH = "/var/run/gabriel/monitoring_bridge.sock"
MODEM_SERIAL_PATH_PATTERN = '/dev/serial/by-id/usb-*-if02-port0'


def get_modem_serial_path() -> str:
    matching_paths = glob.glob(MODEM_SERIAL_PATH_PATTERN)
    if matching_paths:
        return matching_paths[0]
    else:
        raise Exception("modem serial interface not found")


def banner() -> None:
    print(f"{'='*30}", flush=True)
    print("HARDWARE-BRIDGE SERVICE", flush=True)
    print(f"VERSION: {__version__}", flush=True)
    print(f"{'='*30}", flush=True)


def run_command(command) -> (int, str):
    try:
        stdout = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        output = stdout.communicate()[0]
        output = output.decode("utf-8")
        return_code = stdout.returncode
        return (return_code, output)
    except Exception as e:
        _logger.error(f"Cannot run commnad: {command}. {e}")
        raise Exception(f"Cannot run commnad: {command}. {e}")


def remove_device_monitor():
    try:
        command = "docker container rm -f device-monitor"
        (status_code, response) = run_command(command=command)
        response = response.replace("\n", "")
        return status_code
    except Exception as e:
        _logger.error(f"Cannot remove device-monitor container. {e}")
        raise Exception(f"Cannot remove device-monitor container. {e}")


def restart_edge_crane():
    try:
        command = "docker restart edge-crane"
        (status_code, response) = run_command(command=command)
        response = response.replace("\n", "")
        return status_code
    except Exception as e:
        _logger.error(f"Cannot start device-monitor container. {e}")
        raise Exception(f"Cannot start device-monitor container. {e}")


def restart_device_monitor():
    try:
        if remove_device_monitor() != 0:
            raise Exception("Error removing device-monitor")

        if restart_edge_crane() != 0:
            raise Exception("Error starting device-monitor")

    except Exception as e:
        _logger.error(f"Cannot restart container. {e}")
        raise Exception(f"Cannot restart container. {e}")


def restart_history():
    try:
        command = "docker restart history"
        (_, response) = run_command(command=command)
        response = response.replace("\n", "")
        if response != "":
            return {"res": response}
        raise
    except Exception as e:
        _logger.error(f"Cannot restart container. {e}")
        raise Exception(f"Cannot restart container. {e}")


def get_internal_device_path():
    if check_system_is_32_bits():
        return get_device_path(label="rootfs")
    else:
        return get_device_path(label="root")


def get_device_path(label):
    try:
        command = "blkid -L " + label
        (_, response) = run_command(command=command)
        response = response.replace("\n", "")
        if response != "":
            return response
        raise
    except Exception as e:
        _logger.error(f"Cannot retrieve device_path from {label} label. {e}")
        raise Exception(f"Disco {label} não encontrado.")


def get_uuid(device_path):
    try:
        command = "blkid " + device_path
        (_, response) = run_command(command=command)
        response = response.replace("\n", "")
        uuid = next((x for x in response.split() if "UUID" in x), None)
        if uuid is not None:
            return uuid.split('"')[1]
        raise
    except Exception as e:
        _logger.error(f"Cannot retrieve uuid from {device_path}. {e}")
        raise Exception(f"Cannot retrieve uuid from {device_path}. {e}")


def get_hd_model():
    try:
        command = "lsblk -o NAME,MOUNTPOINT,MODEL -J -b /dev/sd?"
        (_, response) = run_command(command=command)
        response = response.replace("\n", "")
        output = json.loads(response)
        model = output["blockdevices"][0]["model"]
        mountpoint = output["blockdevices"][0]["children"][0]["mountpoint"]
        if mountpoint != "/media/usb0":
            raise
        return {"model": model}
    except Exception as e:
        _logger.error(f"Cannot retrieve hd_model. {e}")
        raise Exception(f"Error: Cannot retrieve hd_model. {e}")


def get_storage_usage(mountpoint):
    try:
        command = (
            "df -m | grep "
            + mountpoint
            + ' | awk {\'printf ""$2","$3","$4""\'}'
        )
        (_, response) = run_command(command=command)
        response = response.split(",")
        return {
            "total_mbytes": int(response[0]),
            "used_mbytes": int(response[1]),
            "available_mbytes": int(response[2]),
        }
    except Exception as e:
        _logger.error(f"Cannot retrieve disk usage. {e}")
        raise Exception(f"Error: Cannot retrieve disk usage. {e}")


def get_external_storage_info():
    try:
        check_external_storage_driver()
        device_path = get_device_path(label="gabriel")
        uuid = get_uuid(device_path=device_path)
        return {
            "external_storage_request_status": True,
            "external_storage": {
                "device_path": device_path,
                "uuid": uuid,
                **get_storage_usage("/media/usb0"),
                **get_hd_model(),
            },
        }
    except Exception as e:
        _logger.error(f"Error retrieving external_storage_info: {e}")
        return {
            "external_storage_request_status": False,
            "external_storage": {"reason": str(e.args[0])},
        }


def check_external_storage_driver():
    if not check_system_is_32_bits():
        command = "lsusb"
        (_, response) = run_command(command=command)
        response = response.split("\n")
        for line in response:
            if "ID 0451:" in line:
                # Correct values to HD drivers configuration
                if "ID 0451:9260" not in line and "ID 0451:9261" not in line:
                    raise Exception(
                        "Erro. Provavelmente temos um problema com o driver do HD"
                    )
                return True
        raise Exception(
            "Erro: não conseguimos encontrar o HD nos dispositivos USB"
        )
    _logger.info("System is 32 bits. Cannot check SATA driver")
    return True


def check_system_is_32_bits():
    try:
        command = "uname -m"
        (_, response) = run_command(command=command)
        if "v7" in response:
            return True
        return False
    except Exception as e:
        _logger.error(f"Cannot retrieve Arch from system {e}")
        raise Exception(f"Error: cannot retrieve Arch from system {e}")


def modem_in_usb_list():
    try:
        command = "lsusb"
        (_, response) = run_command(command=command)
        response = response.replace("\n", "")
        if "2c7c:0125" in response:
            return {"err": False, "data": True}
        else:
            return {"err": False, "data": False}
    except Exception as e:
        _logger.error(f"Cannot find modem. {e}")
        return {"err": True, "reason": str(e.args[0])}


def get_modem_AT_response():
    try:
        command = (
            'echo -ne "AT\r\n" | microcom -s 115200 -X ' + get_modem_serial_path() + " -t 100"
        )
        (_, response) = run_command(command=command)
        response = response.split("\n")
        for at in range(len(response)):
            if "AT" in response[at]:
                for ok in range(at, len(response)):
                    if "OK" in response[ok]:
                        return {"err": False, "data": True}
        return {"err": False, "data": False}
    except Exception as e:
        _logger.error(f"Error sending AT command. {e}")
        return {"err": True, "reason": str(e.args[0])}


def get_modem_signal_strength():
    try:
        command = (
            'echo -ne "AT+CSQ\r\n" | microcom -s 115200 -X '
            + get_modem_serial_path()
            + " -t 100"
        )
        (_, response) = run_command(command=command)
        response = response.split("\n")
        for csq in range(len(response)):
            if "+CSQ:" in response[csq]:
                signal_strength = int(response[csq][6:].split(",")[0])
                signal_strength_dbm = -113 + (2 * signal_strength)
                return {"err": False, "data": signal_strength_dbm}
        raise Exception("Falha ao determinar o nível de sinal")
    except Exception as e:
        _logger.error(f"Error sending AT command. {e}")
        return {"err": True, "reason": str(e.args[0])}


def modem_sim_is_inserted():
    try:
        command = (
            'echo -ne "AT+CPIN?\r\n" | microcom -s 115200 -X '
            + get_modem_serial_path()
            + " -t 100"
        )
        (_, response) = run_command(command=command)
        response = response.split("\n")
        for csq in range(len(response)):
            if "+CPIN:" in response[csq]:
                if "READY" in response[csq]:
                    return {"err": False, "data": True}
                else:
                    return {"err": False, "data": False}
            elif "+CME ERROR:" in response[csq]:
                raise Exception(f"CME error number {response[csq][12:]}")
        raise Exception("Response not recognized")
    except Exception as e:
        _logger.error(f"Fail while check if SIM card is present. {e}")
        return {"err": True, "reason": str(e.args[0])}


def get_modem_sim_operator() -> str:
    try:
        command = (
            'echo -ne "AT+QSPN\r\n" | microcom -s 115200 -X '
            + get_modem_serial_path()
            + " -t 100"
        )
        (_, response) = run_command(command=command)
        response = response.split("\n")
        for qspn in range(len(response)):
            if "+QSPN:" in response[qspn]:
                for ok in range(qspn, len(response)):
                    if "OK" in response[ok]:
                        return {"err": False, "data": response[qspn][7:].split(",")[2].replace('"', '')}
        raise Exception("Operator not founded")
    except Exception as e:
        _logger.error(f"Fail while check operator of SIM card. {e}")
        return {"err": True, "reason": str(e.args[0])}


def get_sim_ICCID():
    try:
        command = (
            'echo -ne "AT+ICCID\r\n" | microcom -s 115200 -X '
            + get_modem_serial_path()
            + " -t 100"
        )
        (_, response) = run_command(command=command)
        response = response.split("\n")
        for iccid in range(len(response)):
            if "+ICCID:" in response[iccid]:
                for ok in range(iccid, len(response)):
                    if "OK" in response[ok]:
                        return {"err": False, "data": response[iccid][8:].split()[0]}
        raise Exception("ICCID command error")
    except Exception as e:
        _logger.error(f"Fail while check ICCID from SIM card. {e}")
        return {"err": True, "reason": str(e.args[0])}


def get_modem_info():
    signal_strength_raw = get_modem_signal_strength()
    return {
        "modem_is_present": modem_in_usb_list(),
        "modem_sim_iccid": get_sim_ICCID(),
        "modem_is_operational": get_modem_AT_response(),
        "modem_sim_inserted": modem_sim_is_inserted(),
        "modem_sim_operator": get_modem_sim_operator(),
        "signal_strength_raw": signal_strength_raw
    }


def get_internal_storage_info():
    try:
        device_path = get_internal_device_path()
        uuid = get_uuid(device_path=device_path)
        return {
            "internal_storage_request_status": True,
            "internal_storage": {
                "device_path": device_path,
                "uuid": uuid,
                **get_storage_usage("/$"),
            },
        }
    except Exception as e:
        _logger.error(f"Error retrieving internal_storage_info: {e}")
        return {
            "internal_storage_request_status": False,
            "internal_storage": {},
        }


def get_storage_info():
    try:
        return {**get_internal_storage_info(), **get_external_storage_info()}
    except Exception as e:
        _logger.error(f"Error retrieving storage_info. {e}")


def get_internal_disk_info():
    internal_disk = get_internal_storage_info()
    if internal_disk["internal_storage_request_status"] is False:
        return {
                "device_path": {"reason":  internal_disk["internal_storage"]["reason"], "err": True},
                "uuid": {"reason":  internal_disk["internal_storage"]["reason"], "err": True},
                "total_mbytes": {"reason":  internal_disk["internal_storage"]["reason"], "err": True},
                "used_mbytes": {"reason":  internal_disk["internal_storage"]["reason"], "err": True},
                "available_mbytes": {"reason":  internal_disk["internal_storage"]["reason"], "err": True}
        }
    else:
        return {
                "device_path": {"data": internal_disk["internal_storage"]["device_path"], "err": False},
                "uuid": {"data": internal_disk["internal_storage"]["uuid"],"err": False},
                "total_mbytes": {"data": internal_disk["internal_storage"]["total_mbytes"],"err": False},
                "used_mbytes": {"data": internal_disk["internal_storage"]["used_mbytes"],"err": False},
                "available_mbytes": {"data": internal_disk["internal_storage"]["available_mbytes"], "err": False}
        }


def get_external_disk_info():
    external_disk = get_external_storage_info()
    if external_disk["external_storage_request_status"] is False:
        return {
                "device_path": {"reason":  external_disk["external_storage"]["reason"], "err": True},
                "uuid": {"reason":  external_disk["external_storage"]["reason"], "err": True},
                "total_mbytes": {"reason":  external_disk["external_storage"]["reason"], "err": True},
                "used_mbytes": {"reason":  external_disk["external_storage"]["reason"], "err": True},
                "available_mbytes": {"reason":  external_disk["external_storage"]["reason"], "err": True},
                "model": {"reason":  external_disk["external_storage"]["reason"], "err": True}

        }
    else:
        return {
                "device_path": {"data": external_disk["external_storage"]["device_path"], "err": False},
                "uuid": {"data": external_disk["external_storage"]["uuid"],"err": False},
                "total_mbytes": {"data": external_disk["external_storage"]["total_mbytes"],"err": False},
                "used_mbytes": {"data": external_disk["external_storage"]["used_mbytes"],"err": False},
                "available_mbytes": {"data": external_disk["external_storage"]["available_mbytes"], "err": False},
                "model": {"data": external_disk["external_storage"]["model"], "err": False}
        }



def get_os_release(tag, field):
    try:
        command = "cat /etc/os-release"
        (_, response) = run_command(command=command)
        response = response.split("\n")
        for line in response:
            if line.startswith(tag):
                return {field: {'err': False, 'data': line.split("=")[1].replace('"', "")}}
                return {field: line.split("=")[1].replace('"', "")}
        raise Exception(f"Cannot find {field}")
    except Exception as e:
        _logger.error(f"Cannot retrieve {field}_info. {e}")
        return {field: {'err': True, 'reason': f"Cannot find {field}"}}


def get_board_rev():
    try:
        command = "source /opt/gabriel/bin/board-rev-info.sh && get_board_rev"
        (status_code, response) = run_command(command=command)
        response = response.replace("\n", "")
        if status_code == 0:
            return {"board_rev": {"err": False, "data": response}}
        raise
    except Exception as e:
        _logger.error(f"Cannot to get board rev. {e}")
        return {"board_rev": {"err": True, "reason": "Cannot to get board rev"}}


def get_system_info():
    return {
        **get_os_release("VERSION_ID=", "version"),
        **get_os_release("NAME=", "distro"),
        **get_board_rev()
    }


def get_containers_info():
    try:
        image_register = {}
        images = [
            "provisioning",
            "history",
            "camera-monitor",
            "modem-manager",
            "iot-api",
            "device-monitoring",
            "livestream-on-demand",
            "occlusion-detector",
            "portainer",
            "edge-crane"
        ]
        command = "docker images"
        (_, response) = run_command(command=command)
        for image in images:
            if image in response:
                image_register[image] = True
            else:
                image_register[image] = False
        return image_register
    except Exception as e:
        raise Exception(f"Error: Cannot retrieve hd_model. {e}")


def get_services_info():
    return {
        "install-gabriel-containers": get_install_edge_crane_service_info()
    }


def get_install_edge_crane_service_info():
    try:
        active_state = ""
        sub_state = ""
        command = "systemctl show install-edge-crane --no-page | grep -E 'ActiveState|SubState'"
        (_, response) = run_command(command=command)
        response = response.split("\n")
        for line in response:
            if "ActiveState" in line:
                active_state = line.split("=")[1]
            if "SubState" in line:
                sub_state = line.split("=")[1]
        if active_state == "active":
            if sub_state == "exited":
                return "Download concluído"
            elif sub_state == "running":
                return "Download em andamento"
        else:
            return "Não iniciado"
        return "Desconhecido"
    except Exception as e:
        raise Exception(
            f"Error: Cannot retrieve edge_crane service info. {e}"
        )


def socket_handler(server_address: str):
    _logger.info("Trying to connect with monitoring_bridge.sock")
    while True:
        try:
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.connect(server_address)
            handler_connection(connection=sock)
        except Exception as msg:
            _logger.error(
                f"A error occurred in connection with monitoring_bridge.sock: \
                {msg}"
            )
        time.sleep(5)
        _logger.info("Trying to reconnect with monitoring_bridge.sock")


def publisher_start_msg():
    return json.dumps({"cmd": "pub_hw_brdg"})


def handler_connection(connection):
    _logger.info("Connected with monitoring_bridge.sock")
    publisher_msg = publisher_start_msg()
    connection.sendall(publisher_msg.encode("utf-8"))
    try:
        while True:
            _logger.debug("Waiting message")
            data = connection.recv(1024)
            _logger.debug(f"Message received: {data}")
            if data:
                data = json.loads(data.decode("utf8"))
                decoded_msg = message_decoder(data)
                response = {"cmd": data["cmd"], "mid": data["mid"]}

                if decoded_msg != {}:
                    response["data"] = decoded_msg
                    response["suc"] = True
                else:
                    response["suc"] = False

                _logger.debug(f"Sending message {response}")
                response = json.dumps(response).encode("utf-8")
                connection.sendall(response)
            else:
                break
    except Exception as ex:
        _logger.error(f"Communication error: {ex}")
    finally:
        connection.close()


def message_decoder(message):
    try:
        if "cmd" in message:
            if message["cmd"] == "get_storage_info":
                return get_storage_info()
            if message["cmd"] == "get_internal_storage_info":
                return get_internal_disk_info()
            if message["cmd"] == "get_external_storage_info":
                return get_external_disk_info()
            elif message["cmd"] == "get_containers_info":
                return get_containers_info()
            elif message["cmd"] == "get_system_info":
                return get_system_info()
            elif message["cmd"] == "get_services_info":
                return get_services_info()
            elif message["cmd"] == "get_modem_info":
                return get_modem_info()
            elif message["cmd"] == "restart_containers":
                restart_device_monitor()
                restart_history()
                return {}
            else:
                return {}
    except Exception as ex:
        _logger.error("Failed to decode message:", ex)
        return {}


banner()
socket_handler(SOCKET_PATH)
