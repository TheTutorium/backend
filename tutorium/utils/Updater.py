from datetime import date
from typing import Any


def update(obj: Any, obj_update: Any):
    setattr(obj, "updated_at", date.today())
    for attr, value in obj_update:
        if value is not None and attr != "id":
            setattr(obj, attr, value)

    return obj
