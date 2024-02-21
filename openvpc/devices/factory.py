import pprint

from .vyos import DeviceVyos


class DeviceFactory:
    def instance(
        self,
        type,
        host,
        key,
        protocol,
        port,
        verify=False,
        timeout=10,
    ):
        print(f"DeviceFactory: {type} {protocol} {host} {port} {verify} {timeout}")

        if type == "vyos":
            return DeviceVyos.instance(host, key, protocol, port, verify, timeout)
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
