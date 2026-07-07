from __future__ import annotations

import difflib

from sqlalchemy.orm import Session

from app.models.configuration import Configuration

class DiffService:
    @staticmethod
    def get_configuration(
        db: Session,
        configuration_id:int,
    )-> Configuration | None:
        return(
            db.query(Configuration)
            .filter(
                Configuration.id==configuration_id
            )
            .first()
        )
    @staticmethod
    def generate_diff(
        old_config:str,
        new_config:str,
    )-> str:
        diff=difflib.unified_diff(
            old_config.splitlines(),
            new_config.splitlines(),
            fromfile="Previous Config",
            tofile="Current Config",
            lineterm="",
        )
        return "\n".join(diff)
    