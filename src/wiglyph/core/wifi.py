from dataclasses import dataclass
from enum import StrEnum


class SecurityType(StrEnum):
    WPA = "WPA"
    WEP = "WEP"
    OPEN = "nopass"


def escape_wifi_value(value: str) -> str:
    """Escape reserved characters used by the Wi-Fi QR Code format."""
    translation = {
        "\\": "\\\\",
        ";": "\\;",
        ",": "\\,",
        ":": "\\:",
        '"': '\\"',
    }

    return "".join(translation.get(character, character) for character in value)


@dataclass(frozen=True, slots=True)
class WifiNetwork:
    ssid: str
    security: SecurityType = SecurityType.WPA
    password: str = ""
    hidden: bool = False

    def __post_init__(self) -> None:
        ssid = self.ssid.strip()

        if not ssid:
            raise ValueError("SSID cannot be empty.")

        if self.security is not SecurityType.OPEN and not self.password:
            raise ValueError("Password is required for secured networks.")

        object.__setattr__(self, "ssid", ssid)

    def to_payload(self) -> str:
        ssid = escape_wifi_value(self.ssid)

        fields = [
            f"T:{self.security.value}",
            f"S:{ssid}",
        ]

        if self.security is not SecurityType.OPEN:
            fields.append(f"P:{escape_wifi_value(self.password)}")

        if self.hidden:
            fields.append("H:true")

        return f"WIFI:{';'.join(fields)};;"
