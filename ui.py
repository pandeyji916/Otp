from hydrogram.types import KeyboardButton as _KeyboardButton
from hydrogram import raw

def _auto_style(text: str):
    t = text.lower()
    if any(x in t for x in ('❌','decline','delete','cancel','remove','admin')):
        return 'danger'
    if any(x in t for x in ('✅','buy','deposit','earn','accept','verify')):
        return 'success'
    return 'primary'

def _style_object(style: str):
    style = (style or 'primary').lower()
    if style == 'danger':
        return raw.types.KeyboardButtonStyle(bg_danger=True)
    if style == 'success':
        return raw.types.KeyboardButtonStyle(bg_success=True)
    return raw.types.KeyboardButtonStyle(bg_primary=True)

class KeyboardButton(_KeyboardButton):
    def __init__(self, text, *args, style='', **kwargs):
        super().__init__(text, *args, **kwargs)
        self.style = style or _auto_style(str(text))

    def write(self):
        data = super().write()
        try:
            data.style = _style_object(self.style)
        except Exception:
            pass
        return data
