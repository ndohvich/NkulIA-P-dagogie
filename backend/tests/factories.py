"""Fabriques factory_boy — génèrent des objets de test réalistes sans
répéter les mêmes valeurs à la main dans chaque test.

On utilise `factory.Factory` (pas `SQLAlchemyModelFactory`) : la
factory construit l'objet Python, mais c'est le test qui l'ajoute à sa
session (voir tests/conftest.py) et la commite. Plus explicite, plus
simple à faire cohabiter avec une session isolée par test.
"""

from __future__ import annotations

import factory

from app.core.security import hash_password
from app.db.models import Institution, Teacher


class InstitutionFactory(factory.Factory):
    class Meta:
        model = Institution

    name = factory.Sequence(lambda n: f"Établissement de test {n}")
    department = "Informatique"


class TeacherFactory(factory.Factory):
    class Meta:
        model = Teacher

    email = factory.Sequence(lambda n: f"enseignant{n}@exemple.cm")
    password_hash = factory.LazyFunction(lambda: hash_password("MotDePasse123"))
    last_name = "Yannick"
    first_name = "Jules"
    subject_taught = "Informatique"
