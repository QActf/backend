# Константы для проекта

from enum import Enum


class Role(str, Enum):
    user = 'user'
    manager = 'manager'
    admin = 'admin'


class Gender(str, Enum):
    male = 'male'
    female = 'female'
