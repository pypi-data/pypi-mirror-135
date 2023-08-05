import pytest

from common import assert_compilation_error


def test_hostname(project):
    hostname = "test"
    fqdn = f"{hostname}.something.com"
    assert project.get_plugin_function("hostname")(fqdn) == hostname


def test_hostname_in_model(project):
    model = """
        import ip

        ip::hostname(true)
    """
    assert_compilation_error(project, model, "Invalid value 'True', expected String")


def test_network(project):
    ip = "192.168.2.10"
    cidr = "24"
    network_address = "192.168.2.0"
    assert project.get_plugin_function("network")(ip, cidr) == network_address


def test_network_in_model_invalid_ip_address(project):
    model = """
        import ip

        ip::network("192.168.333.40", "24")
    """
    assert_compilation_error(project, model, "Invalid value '192.168.333.40'")


def test_network_in_model_invalid_cidr(project):
    model = """
        import ip

        # Pass cidr as number instead of string
        ip::network("192.168.125.40", 24)
    """
    assert_compilation_error(project, model, "Invalid value '24', expected String")


def test_cidr_to_network(project):
    cidr = "192.168.2.10/24"
    network_address = "192.168.2.0"
    assert project.get_plugin_function("cidr_to_network")(cidr) == network_address


def test_cidr_to_network_in_model_invalid_cidr(project):
    model = """
        import ip

        ip::cidr_to_network(true)
    """
    assert_compilation_error(project, model, "Invalid value 'True', expected String")


def test_netmask(project):
    cidr = 20
    netmask = "255.255.240.0"
    assert project.get_plugin_function("netmask")(cidr) == netmask


def test_netmask_in_model_invalid_type(project):
    model = """
        import ip

        # Pass string type instead of number
        ip::netmask("16")
    """
    assert_compilation_error(project, model, "Invalid value '16', expected Number")


def test_concat(project):
    host = "ahost"
    domain = "domain.com"
    fqdn = f"{host}.{domain}"
    assert project.get_plugin_function("concat")(host, domain) == fqdn


def test_concat_in_model_invalid_host(project):
    model = """
        import ip

        ip::concat("a$b", "domain.test")
    """
    assert_compilation_error(project, model, "Invalid value 'a$b'")


def test_concat_in_model_invalid_domain(project):
    model = """
        import ip

        ip::concat("test", "domain.test!")
    """
    assert_compilation_error(project, model, "Invalid value 'domain.test!'")


def test_net_to_nm(project):
    network_address = "192.168.10.0/24"
    netmask = "255.255.255.0"
    assert project.get_plugin_function("net_to_nm")(network_address) == netmask


def test_net_to_nm_in_model_invalid_network_address(project):
    model = """
        import ip

        ip::net_to_nm(true)
    """
    assert_compilation_error(project, model, "Invalid value 'True', expected String")


@pytest.mark.parametrize(
    "cidr,ip,prefixlen,netmask,network",
    [
        ("192.168.5.3/16", "192.168.5.3", "16", "255.255.0.0", "192.168.0.0"),
        (
            "2001:0db8:85a3::8a2e:0370:7334/64",
            "2001:db8:85a3::8a2e:370:7334",
            "64",
            "ffff:ffff:ffff:ffff::",
            "2001:db8:85a3::",
        ),
    ],
)
def test_ipnet(project, cidr, ip, prefixlen, netmask, network):
    ipnet = project.get_plugin_function("ipnet")

    assert ipnet(cidr, "ip") == ip
    assert ipnet(cidr, "prefixlen") == prefixlen
    assert ipnet(cidr, "netmask") == netmask
    assert ipnet(cidr, "network") == network
    assert ipnet(cidr, "invalid") is None


def test_ipnet_in_model_invalid_cidr(project):
    model = """
        import ip

        # Pass ip instead of cidr
        ip::ipnet("192.125.125.22", "ip")
    """
    assert_compilation_error(project, model, "Invalid value '192.125.125.22'")


@pytest.mark.parametrize(
    "cidr, idx, result",
    [
        ("192.168.5.3/16", 1, "192.168.0.1"),
        ("192.168.5.3/16", 256, "192.168.1.0"),
        ("2001:0db8:85a3::8a2e:0370:7334/64", 1, "2001:db8:85a3::1"),
        ("2001:0db8:85a3::8a2e:0370:7334/64", 10000, "2001:db8:85a3::2710"),
        ("2001:0db8:85a3::8a2e:0370:7334/64", 100000, "2001:db8:85a3::1:86a0"),
    ],
)
def test_ipindex(project, cidr, idx, result):
    ipnet = project.get_plugin_function("ipindex")
    assert ipnet(cidr, idx) == result


def test_ipindex_in_model_invalid_cidr(project):
    model = """
        import ip

        # Pass ip instead of cidr
        ip::ipindex("192.125.125.22", 16)
    """
    assert_compilation_error(project, model, "Invalid value '192.125.125.22'")


def test_ipindex_in_model_invalid_position(project):
    model = """
        import ip

        # Pass position as string type instead of number
        ip::ipindex("192.125.125.22/24", "16")
    """
    assert_compilation_error(project, model, "Invalid value '16', expected Number")


def test_add(project):
    ip = "192.168.22.11"
    increment = 22
    result = "192.168.22.33"
    assert project.get_plugin_function("add")(ip, increment) == result
    ip = "192.168.22.250"
    increment = 22
    result = "192.168.23.16"
    assert project.get_plugin_function("add")(ip, increment) == result
    ip = "::1"
    increment = 15
    result = "::10"
    assert project.get_plugin_function("add")(ip, increment) == result


def test_add_in_model_invalid_ipv4_addr(project):
    model = """
        import ip

        ip::add("192.125.123.1111", 8)
    """
    assert_compilation_error(project, model, "Invalid value '192.125.123.1111'")


def test_add_in_model_invalid_ipv6_addr(project):
    model = """
        import ip

        ip::add("ffff::fffff", 128)
    """
    assert_compilation_error(project, model, "Invalid value 'ffff::fffff'")


def test_add_in_model_invalid_n_value(project):
    model = """
        import ip

        ip::add("ffff::ffff", "128")
    """
    assert_compilation_error(project, model, "Invalid value '128', expected Number")
