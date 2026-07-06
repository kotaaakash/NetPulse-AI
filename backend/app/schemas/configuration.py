from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.enums.configuration import ConfigurationType


class ConfigurationCreate(BaseModel):
    config_type: ConfigurationType
    content: str


class ConfigurationResponse(BaseModel):
    id: int
    device_id: int
    version: int
    config_type: ConfigurationType
    checksum: str
    content: str
    collected_at: datetime
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class ConfigurationHistoryResponse(BaseModel):
    configurations: list[ConfigurationResponse]