# Константы для проекта

from enum import Enum


class Role(str, Enum):
    user = "user"
    manager = "manager"
    admin = "admin"
