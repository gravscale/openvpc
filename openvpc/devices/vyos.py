import pprint

from pyvyos.device import VyDevice


class DeviceVyos:
    def __init__(
        self,
        host,
        key,
        protocol,
        port,
        verify=False,
        timeout=10,
    ):
        self.device = VyDevice(
            hostname=host, apikey=key, port=port, protocol=protocol, verify=verify, timeout=timeout
        )

    @classmethod
    def instance(
        cls,
        host,
        key,
        protocol,
        port,
        verify=False,
        timeout=10,
    ):
        return cls(host, key, protocol, port, verify, timeout)

    def show(self, path):
        return self.device.retrieve_show_config(path)

    def is_connected(self):
        response = self.show(["system"])
        pprint.pprint(response)

        if response.error is False:
            return True
        return False

    def create_vpc(self, vpc_name, primary_device_name, secondary_device_name):
        response = self.show(["system"])
        pprint.pprint(response)

        if response.error is False:
            return True
        return False

    def delete_vpc(self, vpc_name):
        response = self.show(["system"])
        pprint.pprint(response)

        if response.error is False:
            return True
        return False

    def get_vpc(self, vpc_name):
        response = self.show(["system"])
        pprint.pprint(response)

        if response.error is False:
            return True
        return False

    def get_vpcs(self):
        response = self.show(["system"])
        pprint.pprint(response)

        if response.error is False:
            return True
        return False

    def get_vpc_status(self, vpc_name):
        response = self.show(["system"])
        pprint.pprint(response)

        if response.error is False:
            return True
        return False

    def set_interface_vpc(self, vpc_name, interface_name, vlans=[]):
        response = self.show(["system"])
        pprint.pprint(response)

        if response.error is False:
            return True
        return False

    def unset_interface_vpc(self, vpc_name, interface_name):
        response = self.show(["system"])
        pprint.pprint(response)

        if response.error is False:
            return True
        return False

    def add_gateway(self, vpc_name, gateway_name, gateway_ip, gateway_interface):
        response = self.show(["system"])
        pprint.pprint(response)

        if response.error is False:
            return True
        return False

    def add_route(self, vpc_name, route_name, route_ip, route_interface, route_gateway):
        response = self.show(["system"])
        pprint.pprint(response)

        if response.error is False:
            return True
        return False

    def delete_gateway(self, vpc_name, gateway_name):
        response = self.show(["system"])
        pprint.pprint(response)

        if response.error is False:
            return True
        return False

    def delete_route(self, vpc_name, route_name):
        response = self.show(["system"])
        pprint.pprint(response)

        if response.error is False:
            return True
        return False

    def create_sg(self, vpc_name, sg_name, sg_rules=[]):
        response = self.show(["system"])
        pprint.pprint(response)

        if response.error is False:
            return True
        return False

    def delete_sg(self, vpc_name, sg_name):
        response = self.show(["system"])
        pprint.pprint(response)

        if response.error is False:
            return True
        return False

    def add_sg_rule(
        self,
        vpc_name,
        sg_name,
        sg_rule_name,
        sg_rule_protocol,
        sg_rule_port,
        sg_rule_source_ip,
        sg_rule_destination_ip,
    ):
        response = self.show(["system"])
        pprint.pprint(response)

        if response.error is False:
            return True
        return False

    def delete_sg_rule(self, vpc_name, sg_name, sg_rule_name):
        response = self.show(["system"])
        pprint.pprint(response)

        if response.error is False:
            return True
        return False

    def add_dhcp(
        self,
        vpc_name,
        dhcp_name,
        dhcp_ip_range,
        dhcp_gateway,
        dhcp_dns_servers=[],
        dhcp_domain_name=None,
        dhcp_lease_time=None,
        dhcp_domain_search=[],
    ):
        response = self.show(["system"])
        pprint.pprint(response)

        if response.error is False:
            return True
        return False

    def delete_dhcp(self, vpc_name, dhcp_name):
        response = self.show(["system"])
        pprint.pprint(response)

        if response.error is False:
            return True
        return False

    def add_dhcp_dns_server(self, vpc_name, dhcp_name, dns_server_ip):
        response = self.show(["system"])
        pprint.pprint(response)

        if response.error is False:
            return True
        return False

    def delete_dhcp_dns_server(self, vpc_name, dhcp_name, dns_server_ip):
        response = self.show(["system"])
        pprint.pprint(response)

        if response.error is False:
            return True
        return False

    def add_dhcp_domain_search(self, vpc_name, dhcp_name, domain_search_name):
        response = self.show(["system"])
        pprint.pprint(response)

        if response.error is False:
            return True
        return False

    def delete_dhcp_domain_search(self, vpc_name, dhcp_name, domain_search_name):
        response = self.show(["system"])
        pprint.pprint(response)

        if response.error is False:
            return True
        return False

    def add_lag(self, vpc_name, lag_name, lag_interfaces=[]):
        response = self.show(["system"])
        pprint.pprint(response)

        if response.error is False:
            return True
        return False

    def delete_lag(self, vpc_name, lag_name):
        response = self.show(["system"])
        pprint.pprint(response)

        if response.error is False:
            return True
        return False

    def add_lag_interface(
        self,
        vpc_name,
        lag_name,
        lag_interface_name,
        lag_interface_mode,
        lag_interface_speed,
        lag_interface_vlan=None,
        lag_interface_ip=None,
        lag_interface_description=None,
    ):
        response = self.show(["system"])
        pprint.pprint(response)

        if response.error is False:
            return True
        return False

    def delete_lag_interface(self, vpc_name, lag_name, lag_interface_name):
        response = self.show(["system"])
        pprint.pprint(response)

        if response.error is False:
            return True
        return False

    def set_lag_interface_vlan(self, vpc_name, lag_name, lag_interface_name, lag_interface_vlan):
        response = self.show(["system"])
        pprint.pprint(response)

        if response.error is False:
            return True
        return False

    def unset_lag_interface_vlan(self, vpc_name, lag_name, lag_interface_name, lag_interface_vlan):
        response = self.show(["system"])
        pprint.pprint(response)

        if response.error is False:
            return True
        return False

    def set_lag_interface_ip(self, vpc_name, lag_name, lag_interface_name, lag_interface_ip):
        response = self.show(["system"])
        pprint.pprint(response)

        if response.error is False:
            return True
        return False

    def unset_lag_interface_ip(self, vpc_name, lag_name, lag_interface_name, lag_interface_ip):
        response = self.show(["system"])
        pprint.pprint(response)

        if response.error is False:
            return True
        return False

    def add_vrrp(
        self,
        vpc_name,
        vrrp_name,
        vrrp_priority,
        vrrp_ip,
        vrrp_interface,
        vrrp_description=None,
        vrrp_track=[],
    ):
        response = self.show(["system"])
        pprint.pprint(response)

        if response.error is False:
            return True
        return False

    def delete_vrrp(self, vpc_name, vrrp_name):
        response = self.show(["system"])
        pprint.pprint(response)

        if response.error is False:
            return True
        return False

    def set_vrrp_priority(self, vpc_name, vrrp_name, vrrp_priority):
        response = self.show(["system"])
        pprint.pprint(response)

        if response.error is False:
            return True
        return False

    def unset_vrrp_priority(self, vpc_name, vrrp_name, vrrp_priority):
        response = self.show(["system"])
        pprint.pprint(response)

        if response.error is False:
            return True
        return False

    def add_nat(
        self,
        vpc_name,
        nat_name,
        nat_type,
        nat_interface,
        nat_source_ip,
        nat_destination_ip,
        nat_description=None,
        nat_port_forwarding=[],
    ):
        response = self.show(["system"])
        pprint.pprint(response)

        if response.error is False:
            return True
        return False

    def delete_nat(self, vpc_name, nat_name):
        response = self.show(["system"])
        pprint.pprint(response)

        if response.error is False:
            return True
        return False

    def sg_associate(self, vpc_name, sg_name, interface_name):
        response = self.show(["system"])
        pprint.pprint(response)

        if response.error is False:
            return True
        return False

    def sg_dissociate(self, vpc_name, sg_name, interface_name):
        response = self.show(["system"])
        pprint.pprint(response)

        if response.error is False:
            return True
        return False
