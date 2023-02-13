#!/usr/bin/python3
"""Defines a class City"""
from models.base_model import BaseModel


class City(BaseModel):
    """Represents a class that inherits from BaseModel
          Public class attributes:
             state_id: string - empty string: it will be the State.id
             name: string - empty string
    """

    state_id = ""
    name = ""
