from loguru import logger

from ..core.device_vyos import DeviceVyos


class DeviceFactory:
    def instance(
        self,
        type,
        host,
        port,
        protocol,
        username=None,
        password=None,
        private_key=None,
        verify=False,
        timeout=10,
    ):
        logger.debug(
            f"DeviceFactory: {type} {host} {port} {protocol} {username} {verify} {timeout}"
        )

        if type == "vyos":
            return DeviceVyos.instance(
                host, port, protocol, username, password, private_key, verify, timeout
            )
        else:
            raise ValueError(f"Unknown device type: {type}")

    def show(self, path):
        if hasattr(self, "device"):
            result = self.device.show(path)
            logger.debug(result)
            return result
        else:
            raise Exception("Device not instanced")

    def is_connected(self):
        if hasattr(self, "device"):
            return self.device.is_connected()
        else:
            raise Exception("Device not instanced")
