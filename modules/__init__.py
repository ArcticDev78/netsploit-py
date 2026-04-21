# Import commonly used utilities
from utils.target import get_target, set_target
from utils.font_styles import info_message, success_message, error_message
from utils.colors import cyan, green, yellow  # type: ignore
# from utils.prompt import prompt

# Re-export these imports so they're available when importing from modules
__all__ = [
    "get_target",
    "set_target",
    "info_message",
    "success_message",
    "error_message",
    "cyan",
    "green",
    "yellow",
    # 'prompt'
]
