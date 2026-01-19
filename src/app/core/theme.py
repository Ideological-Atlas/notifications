from dataclasses import dataclass


@dataclass
class Theme:
    background: str = "#020617"
    foreground: str = "#f8fafc"

    card: str = "#0f172a"
    card_foreground: str = "#f8fafc"
    border: str = "#1e293b"

    primary: str = "#16a34a"
    primary_foreground: str = "#ffffff"

    secondary: str = "#1e293b"
    secondary_foreground: str = "#f8fafc"

    muted_foreground: str = "#94a3b8"

    destructive: str = "#ef4444"
    destructive_foreground: str = "#ffffff"


theme = Theme()
