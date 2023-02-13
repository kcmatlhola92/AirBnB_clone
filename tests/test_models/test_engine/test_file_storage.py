#!/usr/bin/python3
"""Unittests for testing `file_storage` module
"""
import os
import models
import unittest
from datetime import datetime
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class TestFileStorage_instantiation(unittest.TestCase):
    """Defines unittests for testing instantiation of `FileStorage class`
    """

    def test_instatiation_no_args(self):
        self.assertEqual(type(FileStorage()), FileStorage)

    def test_instantiation_with_args_None_type(self):
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_file_path_is_private_str(self):
        self.assertEqual(str, type(FileStorage._FileStorage__file_path))

    def test_objects_is_priave_dict(self):
        self.assertEqual(dict, type(FileStorage._FileStorage__objects))

    def test_storage_intance(self):
        self.assertEqual(type(models.storage), FileStorage)


class TestFileStorage_methods(unittest.TestCase):
    """Defines unittests for testing `FileStorage class` methods
    """
    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "demo")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("demo", "file.json")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    def test_all(self):
        self.assertEqual(dict, type(models.storage.all()))

    def test_all_with_args_None_type(self):
        with self.assertRaises(TypeError):
            models.storage.all(None)

    def test_new(self):
        inst = BaseModel()
        models.storage.new(inst)
        inst_key = "BaseModel." + inst.id
        self.assertIn(inst_key, models.storage.all().keys())
        self.assertIn(inst, models.storage.all().values())

    def test_new_with_invalid_args(self):
        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), 1)

    def test_new_with_args_None_type(self):
        with self.assertRaises(AttributeError):
            models.storage.new(None)

    def test_save(self):
        inst = BaseModel()
        models.storage.new(inst)
        models.storage.save()
        txt = ""

        with open("file.json", "r") as f:
            txt = f.read()
            inst_key = "BaseModel." + inst.id
            self.assertIn(inst_key, txt)

    def test_save_with_args_None_type(self):
        with self.assertRaises(TypeError):
            models.storage.save(None)

    def test_reload(self):
        inst = BaseModel()
        models.storage.new(inst)
        models.storage.save()
        models.storage.reload()
        objs = FileStorage._FileStorage__objects
        inst_key = "BaseModel." + inst.id
        self.assertIn(inst_key, objs)

    def test_reload_with_args_None_type(self):
        with self.assertRaises(TypeError):
            models.storage.reload(None)


if __name__ == "__main__":
    unittest.main()
