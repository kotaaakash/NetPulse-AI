from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.services.diff_service import DiffService

router=APIRouter(
    prefix="/configurations",
    tags=["Configuration Diff"],
)

@router.get(
    "/diff/{old_configuration_id}/{new_configuration_id}",
    summary="Compare two config versions",
)
def compare_configurations(
    old_configuration_id:int,
    new_configuration_id:int,
    db:Session=Depends(get_db),
):
    try:
        diff=DiffService.compare_configurations(
            db,
            old_configuration_id,
            new_configuration_id,
        )
        
        return{
            "old_configuration_id": old_configuration_id,
            "new_configuration_id": new_configuration_id,
            "diff":diff,
        }
    except ValueError as error:
        raise HTTPException(
            status_code=404,
            details=str(error),
        )
        