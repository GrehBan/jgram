from dataclasses import dataclass, field
from typing import Dict, Optional

from ..loggers import context_logger


@dataclass(unsafe_hash=True)
class Context:
    """
    User's context
    """
    
    user_id: str
    locale: str
    data: Dict = field(default_factory=dict)
    window_name: Optional[str] = None

    def __post_init__(self):
        context_logger.debug(
            f'builded context {self}'
        )

    def reset(self):
        """
        Reset user's context
        """
        self.data.clear()
        self.window_name = None

        context_logger.debug(
            'context data and window_name cleared'
        )
