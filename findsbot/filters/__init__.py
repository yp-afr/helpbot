from .admin import IsAdmin
from .text_button import TextButton
from .block import IsBlocked


def setup(dp):
    dp.filters_factory.bind(IsBlocked)
    dp.filters_factory.bind(IsAdmin)
    dp.filters_factory.bind(TextButton)
