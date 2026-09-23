from pathlib import Path

import qrcode
from PIL import Image
from qrcode.constants import ERROR_CORRECT_M

from wiglyph.core.wifi import WifiNetwork


class QRGenerator:
    def __init__(
        self,
        *,
        box_size: int = 10,
        border: int = 4,
    ) -> None:
        if box_size < 1:
            raise ValueError("Box size must be greater than zero.")

        if border < 0:
            raise ValueError("Border cannot be negative.")

        self.box_size = box_size
        self.border = border

    def generate(self, network: WifiNetwork) -> Image.Image:
        qr = qrcode.QRCode(
            version=None,
            error_correction=ERROR_CORRECT_M,
            box_size=self.box_size,
            border=self.border,
        )
        qr.add_data(network.to_payload())
        qr.make(fit=True)

        image = qr.make_image(
            fill_color="black",
            back_color="white",
        )

        return image.get_image()

    def save(
        self,
        network: WifiNetwork,
        destination: str | Path,
    ) -> Path:
        path = Path(destination)

        if path.suffix.lower() != ".png":
            path = path.with_suffix(".png")

        image = self.generate(network)
        image.save(path, format="PNG")

        return path
