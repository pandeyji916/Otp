"""Safe Telegram keyboard helpers.

Colour styling is attempted only when the installed Hydrogram build supports
the underlying MTProto button style fields. Standard builds fall back to
normal Telegram buttons instead of breaking the keyboard.
"""

from hydrogram import raw
from hydrogram.types import InlineKeyboardButton as _InlineKeyboardButton
from hydrogram.types import KeyboardButton as _KeyboardButton


def _auto_style(text: str) -> str:
    t = (text or "").lower()
    if any(word in t for word in ("decline", "delete", "cancel", "reject", "ban", "remove", "close", "retry")):
        return "danger"
    if any(word in t for word in ("accept", "verify", "confirm", "approve", "pay", "buy", "deposit", "add", "submit", "redeem", "claim")):
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
    """Inline button that safely attempts native colour styling."""

    def __init__(self, *args, style="", **kwargs):
        super().__init__(*args, **kwargs)
        text = args[0] if args else kwargs.get("text", "")
        self.style = style or _auto_style(text)

    async def write(self, client):
        button = await super().write(client)
        if button is None:
            return button
        try:
            button.style = _style_object(self.style)
        except Exception:
            pass
        return button


class KeyboardButton(_KeyboardButton):
    """Reply keyboard button with a safe styled-build fallback."""

    def __init__(self, text, *args, style="", **kwargs):
        super().__init__(text, *args, **kwargs)
        self.style = style or _auto_style(str(text))

    def write(self):
        # Never let an unsupported Hydrogram version make the whole keyboard disappear.
        if not getattr(self, "request_contact", None) and not getattr(self, "request_location", None) and not getattr(self, "web_app", None):
            try:
                return raw.types.KeyboardButton(
                    text=self.text,
                    style=_style_object(self.style)
                )
            except Exception:
                pass
        return super().write()
