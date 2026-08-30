"""Telegram native coloured button helpers for Hydrogram."""

from hydrogram import raw
from hydrogram.types import InlineKeyboardButton as _InlineKeyboardButton
from hydrogram.types import KeyboardButton as _KeyboardButton


def _auto_style(text: str) -> str:
    """Choose a native Telegram colour while keeping destructive actions red."""
    t = (text or "").lower()

    danger_words = (
        "decline", "delete", "cancel", "reject", "ban", "unban", "remove",
        "stop", "kill", "clear", "deduct", "close", "try again", "retry",
    )
    success_words = (
        "accept", "verify", "confirm", "approve", "pay", "buy", "deposit",
        "add", "submit", "done", "join", "fund", "redeem", "claim",
    )

    if any(word in t for word in danger_words):
        return "danger"
    if any(word in t for word in success_words):
        return "success"
    return "primary"


def _style_object(style: str):
    style = (style or "primary").lower()
    if style == "danger":
        return raw.types.KeyboardButtonStyle(bg_danger=True)
    if style == "success":
        return raw.types.KeyboardButtonStyle(bg_success=True)
    return raw.types.KeyboardButtonStyle(bg_primary=True)


class InlineKeyboardButton(_InlineKeyboardButton):
    """Hydrogram button with MTProto KeyboardButtonStyle support."""

    def __init__(self, *args, style="", **kwargs):
        super().__init__(*args, **kwargs)
        text = args[0] if args else kwargs.get("text", "")
        self.style = style or _auto_style(text)

    async def write(self, client):
        button = await super().write(client)
        if button is not None:
            try:
                button.style = _style_object(self.style)
            except AttributeError:
                # This project pins a Hydrogram build with button-style support.
                pass
        return button


class KeyboardButton(_KeyboardButton):
    """Reply keyboard button with Telegram native blue/green/red styling."""

    def __init__(self, text, *args, style="", **kwargs):
        super().__init__(text, *args, **kwargs)
        self.style = style or _auto_style(str(text))

    def write(self):
        # Main keyboard buttons in this project are plain text buttons.
        if not getattr(self, "request_contact", None) and not getattr(self, "request_location", None) and not getattr(self, "web_app", None):
            return raw.types.KeyboardButton(text=self.text, style=_style_object(self.style))
        return super().write()
