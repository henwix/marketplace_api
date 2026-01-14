from dataclasses import dataclass, fields

from src.apps.common.types import UNSET


@dataclass(frozen=True, eq=False)
class BaseUpdateCommand:
    _skip_fields = {'user_id'}

    @property
    def is_empty(self) -> bool:
        """Returns True if all updatable fields are equal to UNSET (except for skip_fields)."""
        all_fields = fields(self)
        has_changes = any(getattr(self, f.name) is not UNSET for f in all_fields if f.name not in self._skip_fields)
        return not has_changes
