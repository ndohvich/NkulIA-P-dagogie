"""Modèles de contexte enseignant.

Ces tables correspondent au schéma de départ décrit dans
docs/ARCHITECTURE.md : teacher, institution, school_year, subject,
classroom, teaching_assignment. On y ajoute `AuthSession`, nécessaire
pour la connexion locale (issue #7) mais absente du schéma initial —
c'est le genre de petit écart qu'on documente plutôt que de cacher.

Notes pédagogiques (niveau 0) :
- `Mapped[str]` etc. sont des annotations de type : elles disent à
  SQLAlchemy (et à vous) quel type Python correspond à quelle colonne.
- `mapped_column(unique=True)` crée une contrainte d'unicité en base :
  la base de données elle-même refusera un deuxième enseignant avec le
  même email, même si le code applicatif avait un bug.
- Les relations (`relationship`) ne créent pas de colonne ; elles
  donnent juste un raccourci Python pratique (ex. `teacher.institution`).
"""

from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


def _utcnow() -> datetime:
    return datetime.now(UTC)


class Institution(Base):
    """Un établissement scolaire (ex. Lycée Technique d'Ébolowa)."""

    __tablename__ = "institution"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), unique=True)
    department: Mapped[str | None] = mapped_column(String(120), nullable=True)

    teachers: Mapped[list[Teacher]] = relationship(back_populates="institution")


class Teacher(Base):
    """Un enseignant — le compte utilisateur principal de NkulIA."""

    __tablename__ = "teacher"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))

    last_name: Mapped[str] = mapped_column(String(120))
    first_name: Mapped[str] = mapped_column(String(120))
    subject_taught: Mapped[str | None] = mapped_column(String(120), nullable=True)
    specialty: Mapped[str | None] = mapped_column(String(120), nullable=True)
    grade: Mapped[str | None] = mapped_column(String(80), nullable=True)
    function: Mapped[str | None] = mapped_column(String(120), nullable=True)

    institution_id: Mapped[int | None] = mapped_column(ForeignKey("institution.id"), nullable=True)
    institution: Mapped[Institution | None] = relationship(back_populates="teachers")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)

    sessions: Mapped[list[AuthSession]] = relationship(
        back_populates="teacher", cascade="all, delete-orphan"
    )


class SchoolYear(Base):
    """Une année scolaire (ex. 2025-2026), rattachée à un établissement."""

    __tablename__ = "school_year"
    __table_args__ = (UniqueConstraint("institution_id", "label"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    institution_id: Mapped[int] = mapped_column(ForeignKey("institution.id"))
    label: Mapped[str] = mapped_column(String(20))  # ex. "2025-2026"


class Subject(Base):
    """Une matière enseignée (ex. Informatique)."""

    __tablename__ = "subject"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True)


class Classroom(Base):
    """Une classe (ex. Seconde C, Niveau 1)."""

    __tablename__ = "classroom"

    id: Mapped[int] = mapped_column(primary_key=True)
    institution_id: Mapped[int] = mapped_column(ForeignKey("institution.id"))
    school_year_id: Mapped[int] = mapped_column(ForeignKey("school_year.id"))
    label: Mapped[str] = mapped_column(String(80))  # ex. "Seconde C", "Niveau 1"
    track: Mapped[str] = mapped_column(String(20))  # "generale" | "technique"
    headcount: Mapped[int | None] = mapped_column(nullable=True)


class TeachingAssignment(Base):
    """Le lien entre un enseignant, une classe et une matière."""

    __tablename__ = "teaching_assignment"
    __table_args__ = (UniqueConstraint("teacher_id", "classroom_id", "subject_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teacher.id"))
    classroom_id: Mapped[int] = mapped_column(ForeignKey("classroom.id"))
    subject_id: Mapped[int] = mapped_column(ForeignKey("subject.id"))


class AuthSession(Base):
    """Une session de connexion locale (issue #7).

    Volontairement simple : un jeton opaque stocké côté serveur, avec
    une date d'expiration. Pas de JWT ici — inutile en local, et plus
    facile à révoquer immédiatement (il suffit de supprimer la ligne).
    """

    __tablename__ = "auth_session"

    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teacher.id"))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)

    teacher: Mapped[Teacher] = relationship(back_populates="sessions")
