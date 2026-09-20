"""Route de gestion du profil (issue #7) — nécessite d'être connecté."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_teacher
from app.api.routes.auth import _profile_out
from app.db.models import Teacher
from app.db.session import get_db
from app.schemas.teacher import TeacherProfileOut, TeacherProfileUpdate

router = APIRouter(tags=["profile"])


@router.get("/me", response_model=TeacherProfileOut)
def read_my_profile(teacher: Teacher = Depends(get_current_teacher)) -> TeacherProfileOut:
    return _profile_out(teacher)


@router.patch("/me", response_model=TeacherProfileOut)
def update_my_profile(
    payload: TeacherProfileUpdate,
    teacher: Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db),
) -> TeacherProfileOut:
    # `exclude_unset=True` : seuls les champs réellement envoyés par le
    # client sont pris en compte — un champ omis n'écrase pas la valeur
    # existante avec `None`.
    updates = payload.model_dump(exclude_unset=True)
    for field_name, value in updates.items():
        setattr(teacher, field_name, value)

    db.commit()
    db.refresh(teacher)
    return _profile_out(teacher)
