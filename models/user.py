#!/usr/bin/python3
"""Defines a class User"""
from models.base_model import BaseModel


class User(BaseModel):
    """Represents a class that inherits from BaseModel
        Public class attributes:
           email: string - empty string
           password: string - empty string
           first_name: string - empty string
           last_name: string - empty string
    """

    email = ""
    password = ""
    first_name = ""
    last_name = ""
