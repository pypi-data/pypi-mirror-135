from quo.keys.key_binding.key_processor import KeyPressEvent
from quo.keys import Keys, KeyBinder


__all__ = [
    "load_cpr_bindings",
]

E = KeyPressEvent


def load_cpr_bindings() -> KeyBinder:
    key_bindings = KeyBinder()

    @key_bindings.add(Keys.CPRResponse, save_before=lambda e: False)
    def _(event: E) -> None:
        """
        Handle incoming Cursor-Position-Request response.
        """
        # The incoming data looks like u'\x1b[35;1R'
        # Parse row/col information.
        row, col = map(int, event.data[2:-1].split(";"))

        # Report absolute cursor position to the renderer.
        event.app.renderer.report_absolute_cursor_row(row)

    return key_bindings
