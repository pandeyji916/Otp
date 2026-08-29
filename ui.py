from hydrogram.types import InlineKeyboardButton as _InlineKeyboardButton

def _auto_style(text):
    t = (text or "").lower()
    if any(x in t for x in ("decline", "delete", "cancel", "reject", "ban", "remove", "stop")):
        return "danger"
    if any(x in t for x in ("accept", "verify", "confirm", "approve", "pay", "buy", "deposit", "add", "submit", "done")):
        return "success"
    return "primary"

class InlineKeyboardButton(_InlineKeyboardButton):
    def __init__(self, *args, style="", **kwargs):
        super().__init__(*args, **kwargs)
        self.style = style or _auto_style(args[0] if args else kwargs.get("text", ""))

    def to_dict(self):
        data = super().to_dict()
        data["style"] = self.style
        return data
