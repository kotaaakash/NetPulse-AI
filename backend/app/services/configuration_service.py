from __future__ import annotations

import hashlib
from app.enums.configuration import ConfigurationType
from sqlalchemy.orm import Session

from app.models.configuration import Configuration
class ConfigurationService:
    """
    Business logic for device configurations.
    """
    @staticmethod
    def calculate_checksum(config: str) -> str:
        return hashlib.sha256(
        config.encode("utf-8")
    ).hexdigest()
        
    @staticmethod
    def get_latest_configuration(
        db: Session,
        device_id: int,
    ) -> Configuration | None:
        return (
            db.query(Configuration)
            .filter(Configuration.device_id == device_id)
            .order_by(Configuration.version.desc())
            .first()
        )

    @staticmethod
    def get_next_version(
        db: Session,
        device_id: int,
    ) -> int:
        latest = ConfigurationService.get_latest_configuration(
            db,
            device_id,
        )

        if latest is None:
            return 1

        return latest.version + 1
    
    @staticmethod
    def has_configuration_changed(
        db: Session,
        device_id: int,
        new_configuration: str,
    ) -> bool:
        latest = ConfigurationService.get_latest_configuration(
            db,
            device_id,
        )

        if latest is None:
            return True

        new_checksum = ConfigurationService.calculate_checksum(
            new_configuration,
        )

        return latest.checksum != new_checksum
    
    @staticmethod
    def save_configuration(
        db: Session,
        device_id: int,
        config_type: ConfigurationType,
        content: str,
    ) -> Configuration:

        if not ConfigurationService.has_configuration_changed(
            db,
            device_id,
            content,
        ):
            return ConfigurationService.get_latest_configuration(
                db,
                device_id,
            )

        version = ConfigurationService.get_next_version(
            db,
            device_id,
        )

        checksum = ConfigurationService.calculate_checksum(
            content,
        )

        configuration = Configuration(
            device_id=device_id,
            version=version,
            config_type=config_type,
            checksum=checksum,
            content=content,
        )

        db.add(configuration)
        db.commit()
        db.refresh(configuration)

        return configuration
    
    @staticmethod
    def get_configuration_history(
        db: Session,
        device_id: int,
    ) -> list[Configuration]:
        return (
            db.query(Configuration)
            .filter(Configuration.device_id == device_id)
            .order_by(Configuration.version.desc())
            .all()
        )