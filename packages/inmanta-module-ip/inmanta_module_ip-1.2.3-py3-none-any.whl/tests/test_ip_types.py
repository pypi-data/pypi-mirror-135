import inmanta.ast
import pytest

from common import assert_compilation_error


def run_test(project, thetype, value, is_ok):
    def make():
        project.compile(
            f"""
import ip
entity Holder:
    {thetype} value
end
implement Holder using std::none

Holder(value="{value}")
"""
        )

    if not is_ok:
        with pytest.raises(inmanta.ast.RuntimeException):
            make()
    else:
        make()


@pytest.mark.parametrize(
    "ip,is_ok",
    [
        ("192.168.5.3", True),
        ("5236", True),
        ("635.236.45.6", False),
        ("1.1.1.1/32", False),
        ("2001:0db8:85a3:0000:0000:8a2e:0370:7334", False),
    ],
)
def test_ip(project, ip, is_ok):
    run_test(project, "ip::ip", ip, is_ok)


@pytest.mark.parametrize(
    "ip,is_ok",
    [
        ("192.168.5.3", False),
        ("5236/24", False),
        ("635.236.45.6/32", False),
        ("1.1.1.1/32", True),
        ("2001:0db8:85a3:0000:0000:8a2e:0370:7334/36", False),
    ],
)
def test_cidr(project, ip, is_ok):
    run_test(project, "ip::cidr", ip, is_ok)


@pytest.mark.parametrize(
    "ip,is_ok",
    [
        ("192.168.5.3", False),
        ("5236", False),
        ("2z01:0db8:85a3:0000:0000:8a2e:0370:7334", False),
        ("2001:0db8:85a3::8a2e:0370:7334", True),
        ("2001:0db8:85a3:0000:0000:8a2e:0370:7334", True),
    ],
)
def test_ip_v6(project, ip, is_ok):
    run_test(project, "ip::ip_v6", ip, is_ok)


@pytest.mark.parametrize(
    "ip,is_ok",
    [
        ("192.168.5.3/32", False),
        ("2z01:0db8:85a3:0000:0000:8a2e:0370:7334/64", False),
        ("2001:0db8:85a3:0000:0000:8a2e:0370:7334/64", True),
        ("2001:0db8:85a3::8a2e:0370:7334/64", True),
    ],
)
def test_cidr_v6(project, ip, is_ok):
    run_test(project, "ip::cidr_v6", ip, is_ok)


@pytest.mark.parametrize(
    "ip,is_ok",
    [
        ("192.168.5.3", True),
        ("5236", True),
        ("2z01:0db8:85a3:0000:0000:8a2e:0370:7334", False),
        ("2001:0db8:85a3::8a2e:0370:7334", True),
        ("2001:0db8:85a3:0000:0000:8a2e:0370:7334", True),
    ],
)
def test_ip_v10(project, ip, is_ok):
    run_test(project, "ip::ip_v10", ip, is_ok)


@pytest.mark.parametrize(
    "ip,is_ok",
    [
        ("192.168.5.3/32", True),
        ("2z01:0db8:85a3:0000:0000:8a2e:0370:7334/64", False),
        ("2001:0db8:85a3:0000:0000:8a2e:0370:7334/64", True),
        ("2001:0db8:85a3::8a2e:0370:7334/64", True),
    ],
)
def test_cidr_v10(project, ip, is_ok):
    run_test(project, "ip::cidr_v10", ip, is_ok)


def test_is_valid_ip(project):
    ip = "10.20.30.40"
    assert project.get_plugin_function("is_valid_ip")(ip)
    ip = "10.555.30"
    assert not project.get_plugin_function("is_valid_ip")(ip)
    ip = "10.20.30.256"
    assert not project.get_plugin_function("is_valid_ip")(ip)


def test_is_valid_ip_in_model_invalid_ip(project):
    model = """
        import ip

        ip::is_valid_ip(true)
    """
    assert_compilation_error(project, model, "Invalid value 'True', expected String")


def test_is_valid_cidr_v10(project):
    cidr = "::/0"
    assert project.get_plugin_function("is_valid_cidr_v10")(cidr)
    cidr = "::/128"
    assert project.get_plugin_function("is_valid_cidr_v10")(cidr)
    cidr = "1111::1/128"
    assert project.get_plugin_function("is_valid_cidr_v10")(cidr)
    cidr = "1111::1/129"
    assert not project.get_plugin_function("is_valid_cidr_v10")(cidr)
    cidr = "ftff::1/64"
    assert not project.get_plugin_function("is_valid_cidr_v10")(cidr)


def test_test_is_valid_cidr_v10_in_model_invalid_ip(project):
    model = """
        import ip

        ip::is_valid_cidr_v10(true)
    """
    assert_compilation_error(project, model, "Invalid value 'True', expected String")


def test_is_valid_ip_v10(project):
    ip = "::"
    assert project.get_plugin_function("is_valid_ip_v10")(ip)
    ip = "1111::1"
    assert project.get_plugin_function("is_valid_ip_v10")(ip)
    ip = "1:fffq::1"
    assert not project.get_plugin_function("is_valid_ip_v10")(ip)
    ip = "1111::fffq"
    assert not project.get_plugin_function("is_valid_ip_v10")(ip)


def test_test_is_valid_ip_v10_in_model_invalid_ip(project):
    model = """
        import ip

        ip::is_valid_ip_v10(true)
    """
    assert_compilation_error(project, model, "Invalid value 'True', expected String")


def test_is_valid_netmask(project):
    netmask = "255.255.255.0"
    assert project.get_plugin_function("is_valid_netmask")(netmask)
    netmask = "255.255.252.0"
    assert project.get_plugin_function("is_valid_netmask")(netmask)
    netmask = "255.128.0.0"
    assert project.get_plugin_function("is_valid_netmask")(netmask)
    netmask = "255.128.0.255"
    assert not project.get_plugin_function("is_valid_netmask")(netmask)
    netmask = "255.120.0.0"
    assert not project.get_plugin_function("is_valid_netmask")(netmask)
