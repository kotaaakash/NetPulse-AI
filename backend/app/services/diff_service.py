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
    @staticmethod
    def compare_configurations(
        db: Session,
        old_configuration_id: int,
        new_configuration_id: int,
    ) -> str:

        old_configuration = DiffService.get_configuration(
            db,
            old_configuration_id,
        )

        new_configuration = DiffService.get_configuration(
            db,
            new_configuration_id,
        )

        if old_configuration is None:
            raise ValueError(
                f"Configuration {old_configuration_id} not found."
            )

        if new_configuration is None:
            raise ValueError(
                f"Configuration {new_configuration_id} not found."
            )

        return DiffService.generate_diff(
            old_configuration.content,
            new_configuration.content,
        )
    