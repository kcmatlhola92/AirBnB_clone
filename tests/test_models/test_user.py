#!/usr/bin/python3
"""Unittests for testing models/user module
    Unittest classes:
        TestUser_instantiation
        TestUser_save
        TestUser_to_dict
"""
import os
import unittest
import models
from datetime import datetime
from models.user import User


class TestUser_instantiation(unittest.TestCase):
    """Defines the unittests for testing instantiation of `User class`
    """

    def test_user_instantiation_with_no_args(self):
        self.assertEqual(User, type(User()))

    def test_user_instance_stored_in_objects(self):
        self.assertIn(User(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(User().id))

    def test_created_at_public_datetime(self):
        self.assertEqual(datetime, type(User().created_at))

    def test_updated_at_public_datetime(self):
        self.assertEqual(datetime, type(User().updated_at))

    def test_email_is_public_str(self):
        self.assertEqual(str, type(User.email))

    def test_password_is_public_str(self):
        self.assertEqual(str, type(User.password))

    def test_first_name_is_public_str(self):
        self.assertEqual(str, type(User.first_name))

    def test_last_name_is_public_str(self):
        self.assertEqual(str, type(User.last_name))

    def test_two_users_ids_unique(self):
        user1 = User()
        user2 = User()
        self.assertNotEqual(user1.id, user2.id)

    def test_two_users_different_created_at(self):
        user1 = User()
        user2 = User()
        self.assertLess(user1.created_at, user2.created_at)

    def test_two_users_different_updated_at(self):
        user1 = User()
        user2 = User()
        self.assertLess(user1.updated_at, user2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        user = User()
        user.id = "987"
        user.created_at = user.updated_at = dt
        user_str = user.__str__()
        self.assertIn("[User] (987)", user_str)
        self.assertIn("'id': '987'", user_str)
        self.assertIn("'updated_at': " + dt_repr, user_str)

    def test_args_unused(self):
        user = User(None)
        self.assertNotIn(None, user.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        user = User(id="789", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(user.id, "789")
        self.assertEqual(user.created_at, dt)
        self.assertEqual(user.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            User(id=None, created_at=None, updated_at=None)


class TestUser_save(unittest.TestCase):
    """Defines unittests for testing `save` method of `User` class
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

    def test_one_save(self):
        user = User()
        first_updated_at = user.updated_at
        user.save()
        self.assertLess(first_updated_at, user.updated_at)

    def test_save_with_args_None_type(self):
        user = User()
        with self.assertRaises(TypeError):
            user.save(None)

    def test_save_updates_file(self):
        user = User()
        user.save()
        user_id = "User." + user.id
        with open("file.json", "r") as f:
            self.assertIn(user_id, f.read())


class TestUser_to_dict(unittest.TestCase):
    """Defines unittests for testing `to_dict` method of User class
    """

    def test_to_dict_type(self):
        self.assertTrue(dict, type(User().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        user = User()
        self.assertIn("id", user.to_dict().keys())
        self.assertIn("created_at", user.to_dict().keys())
        self.assertIn("updated_at", user.to_dict().keys())
        self.assertIn("__class__", user.to_dict().keys())

    def test_to_dict_contains_added_attributes(self):
        user = User()
        user.middle_name = "Best School"
        user.my_number = 89
        self.assertEqual("Best School", user.middle_name)
        self.assertEqual(89, user.my_number)

    def test_to_dict_attributes_are_strs(self):
        user = User()
        user_dict = user.to_dict()
        self.assertEqual(str, type(user_dict["id"]))
        self.assertEqual(str, type(user_dict["created_at"]))
        self.assertEqual(str, type(user_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        user = User()
        user.id = "789"
        user.created_at = user.updated_at = dt
        t_dict = {
            'id': '789',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
            '__class__': 'User'
        }
        self.assertDictEqual(user.to_dict(), t_dict)

    def test_contrast_to_dict_dunder_dict(self):
        user = User()
        self.assertNotEqual(user.to_dict(), user.__dict__)

    def test_to_dict_with_args(self):
        user = User()
        with self.assertRaises(TypeError):
            user.to_dict(None)


if __name__ == "__main__":
    unittest.main()
