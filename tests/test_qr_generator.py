from pathlib import Path

import pytest
from PIL import Image

from wifi_qr.core.qr_generator import QRGenerator
from wifi_qr.core.wifi import SecurityType, WifiNetwork


@pytest.fixture
def network() -> WifiNetwork:
    return WifiNetwork(
        ssid="Office WiFi",
        security=SecurityType.WPA,
        password="secure-password",
    )


def test_generate_returns_pillow_image(network: WifiNetwork) -> None:
    generator = QRGenerator()

    image = generator.generate(network)

    assert isinstance(image, Image.Image)
    assert image.width > 0
    assert image.height > 0
    assert image.width == image.height


def test_generate_creates_monochrome_qr(network: WifiNetwork) -> None:
    generator = QRGenerator()

    image = generator.generate(network)

    colors = image.convert("RGB").getcolors(maxcolors=256)

    assert colors is not None
    assert len(colors) == 2


def test_save_creates_png(
    tmp_path: Path,
    network: WifiNetwork,
) -> None:
    generator = QRGenerator()
    destination = tmp_path / "wifi.png"

    result = generator.save(network, destination)

    assert result == destination
    assert destination.is_file()

    with Image.open(destination) as image:
        assert image.format == "PNG"


def test_save_adds_png_extension(
    tmp_path: Path,
    network: WifiNetwork,
) -> None:
    generator = QRGenerator()
    destination = tmp_path / "wifi"

    result = generator.save(network, destination)

    assert result == tmp_path / "wifi.png"
    assert result.is_file()


def test_invalid_box_size_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="Box size must be greater than zero",
    ):
        QRGenerator(box_size=0)


def test_negative_border_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match="Border cannot be negative",
    ):
        QRGenerator(border=-1)
