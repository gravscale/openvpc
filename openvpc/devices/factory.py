import pprint

from .vyos import Device_Vyos


class Device_Factory:
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
        print(
            f"Device_Factory: {type} {host} {port} {protocol} {username} {password} {private_key} {verify} {timeout}"
        )

        if type == "vyos":
            return Device_Vyos.instance(
                host, port, protocol, username, password, private_key, verify, timeout
            )
        else:
            raise ValueError(f"Unknown device type: {type}")

    def show(self, path):
        if hasattr(self, "device"):
            result = self.device.show(path)
            pprint.pprint(result)
            return result
        else:
            raise Exception("Device not instanced")

    def is_connected(self):
        if hasattr(self, "device"):
            return self.device.is_connected()
        else:
            raise Exception("Device not instanced")
