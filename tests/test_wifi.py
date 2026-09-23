import pytest

from wifi_qr.core.wifi import SecurityType, WifiNetwork, escape_wifi_value


def test_wpa_payload() -> None:
    network = WifiNetwork(
        ssid="Office WiFi",
        security=SecurityType.WPA,
        password="secure-password",
    )

    assert network.to_payload() == (
        "WIFI:T:WPA;S:Office WiFi;P:secure-password;;"
    )


def test_wep_payload() -> None:
    network = WifiNetwork(
        ssid="Legacy Network",
        security=SecurityType.WEP,
        password="12345",
    )

    assert network.to_payload() == (
        "WIFI:T:WEP;S:Legacy Network;P:12345;;"
    )


def test_open_network_payload() -> None:
    network = WifiNetwork(
        ssid="Guest",
        security=SecurityType.OPEN,
    )

    assert network.to_payload() == "WIFI:T:nopass;S:Guest;;"


def test_hidden_network_payload() -> None:
    network = WifiNetwork(
        ssid="Hidden Network",
        security=SecurityType.WPA,
        password="secret",
        hidden=True,
    )

    assert network.to_payload() == (
        "WIFI:T:WPA;S:Hidden Network;P:secret;H:true;;"
    )


def test_reserved_characters_are_escaped() -> None:
    assert escape_wifi_value(r'Office;WiFi:5G,"Lab"\Test') == (
        r'Office\;WiFi\:5G\,\"Lab\"\\Test'
    )


def test_payload_escapes_credentials() -> None:
    network = WifiNetwork(
        ssid="Office;5G",
        security=SecurityType.WPA,
        password=r"abc:def,test\123",
    )

    assert network.to_payload() == (
        r"WIFI:T:WPA;S:Office\;5G;P:abc\:def\,test\\123;;"
    )


def test_ssid_is_trimmed() -> None:
    network = WifiNetwork(
        ssid="  Office WiFi  ",
        security=SecurityType.OPEN,
    )

    assert network.ssid == "Office WiFi"


def test_empty_ssid_is_rejected() -> None:
    with pytest.raises(ValueError, match="SSID cannot be empty"):
        WifiNetwork(
            ssid="   ",
            security=SecurityType.OPEN,
        )


def test_secured_network_requires_password() -> None:
    with pytest.raises(ValueError, match="Password is required"):
        WifiNetwork(
            ssid="Office",
            security=SecurityType.WPA,
            password="",
        )


def test_open_network_does_not_require_password() -> None:
    network = WifiNetwork(
        ssid="Guest",
        security=SecurityType.OPEN,
        password="",
    )

    assert network.to_payload() == "WIFI:T:nopass;S:Guest;;"
