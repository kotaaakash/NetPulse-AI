from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.change_request import (
    ChangeRequestCreate,
    ChangeRequestListResponse,
    ChangeRequestResponse,
)
from app.services.change_request_service import ChangeRequestService
router = APIRouter(
    prefix="/change-requests",
    tags=["Change Requests"],
)
@router.post(
    "",
    response_model=ChangeRequestResponse,
    summary="Create a change request",
)
def create_change_request(
    payload: ChangeRequestCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new network change request.
    """

    change_request = ChangeRequestService.create_change_request(
        db=db,
        title=payload.title,
        description=payload.description,
        device_id=payload.device_id,
        configuration_id=payload.configuration_id,
        priority=payload.priority,
    )

    return change_request


@router.get(
    "",
    response_model=ChangeRequestListResponse,
    summary="Get all change requests",
)
def get_all_change_requests(
    db: Session = Depends(get_db),
):
    """
    Retrieve all change requests.
    """

    change_requests = ChangeRequestService.get_all_change_requests(
        db=db,
    )

    return ChangeRequestListResponse(
        change_requests=change_requests,
    )


@router.get(
    "/{change_request_id}",
    response_model=ChangeRequestResponse,
    summary="Get a change request",
)
def get_change_request(
    change_request_id: int,
    db: Session = Depends(get_db),
):
    """
    Retrieve a single change request.
    """

    change_request = ChangeRequestService.get_change_request(
        db=db,
        change_request_id=change_request_id,
    )

    if change_request is None:
        raise HTTPException(
            status_code=404,
            detail="Change request not found",
        )

    return change_request
@router.post(
    "/{change_request_id}/submit",
    response_model=ChangeRequestResponse,
    summary="Submit a change request",
)
def submit_change_request(
    change_request_id: int,
    db: Session = Depends(get_db),
):
    try:
        return ChangeRequestService.submit_change_request(
            db=db,
            change_request_id=change_request_id,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )
    
@router.post(
    "/{change_request_id}/approve",
    response_model=ChangeRequestResponse,
    summary="Approve a change request",
)
def approve_change_request(
    change_request_id: int,
    db: Session = Depends(get_db),
):
    try:
        return ChangeRequestService.approve_change_request(
            db=db,
            change_request_id=change_request_id,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )
    
@router.post(
    "/{change_request_id}/reject",
    response_model=ChangeRequestResponse,
    summary="Reject a change request",
)
def reject_change_request(
    change_request_id: int,
    db: Session = Depends(get_db),
):
    try:
        return ChangeRequestService.reject_change_request(
            db=db,
            change_request_id=change_request_id,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )
@router.post(
    "/{change_request_id}/deploy",
    response_model=ChangeRequestResponse,
    summary="Deploy a change request",
)
def deploy_change_request(
    change_request_id: int,
    db: Session = Depends(get_db),
):
    try:
        return ChangeRequestService.deploy_change_request(
            db=db,
            change_request_id=change_request_id,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )
    
@router.post(
    "/{change_request_id}/rollback",
    response_model=ChangeRequestResponse,
    summary="Rollback a deployed change request",
)
def rollback_change_request(
    change_request_id: int,
    db: Session = Depends(get_db),
):
    try:
        return ChangeRequestService.rollback_change_request(
            db=db,
            change_request_id=change_request_id,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )
        
        