from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.configuration import (
    ConfigurationCreate,
    ConfigurationHistoryResponse,
    ConfigurationResponse,
)
from app.services.configuration_service import ConfigurationService

router = APIRouter(
    prefix="/devices",
    tags=["Configurations"],
)


@router.post(
    "/{device_id}/configurations",
    response_model=ConfigurationResponse,
    summary="Upload a device configuration",
)
def upload_configuration(
    device_id: int,
    payload: ConfigurationCreate,
    db: Session = Depends(get_db),
):
    """
    Upload a new configuration for a device.

    If the configuration has not changed, the latest version
    is returned without creating a new record.
    """
    configuration = ConfigurationService.save_configuration(
        db=db,
        device_id=device_id,
        config_type=payload.config_type,
        content=payload.content,
    )

    return configuration


@router.get(
    "/{device_id}/configurations",
    response_model=ConfigurationHistoryResponse,
    summary="Get configuration history",
)
def get_configuration_history(
    device_id: int,
    db: Session = Depends(get_db),
):
    """
    Retrieve all configuration versions for a device,
    ordered from newest to oldest.
    """
    configurations = ConfigurationService.get_configuration_history(
        db=db,
        device_id=device_id,
    )

    return ConfigurationHistoryResponse(
        configurations=configurations
    )


@router.get(
    "/{device_id}/configurations/latest",
    response_model=ConfigurationResponse,
    summary="Get latest configuration",
)
def get_latest_configuration(
    device_id: int,
    db: Session = Depends(get_db),
):
    """
    Retrieve the latest configuration for a device.
    """
    configuration = ConfigurationService.get_latest_configuration(
        db=db,
        device_id=device_id,
    )

    if configuration is None:
        raise HTTPException(
            status_code=404,
            detail="Configuration not found",
        )

    return configuration