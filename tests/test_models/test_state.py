#!/usr/bin/python3
"""Unittests for testing models/state module
Unittest classes:
    TestState_instantiation
    TestState_save
    TestState_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from models.state import State


class TestState_instantiation(unittest.TestCase):
    """Defines unittest for testing the State class
    """

    def test_no_args_instantiation(self):
        self.assertEqual(State, type(State()))

    def test_new_instance_stored(self):
        self.assertIn(State(), models.storage.all().values())

    def test_create_at_is_public_datetime(self):
        self.assertEqual(datetime, type(State().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(State().updated_at))

    def test_id_is_public_str(self):
        self.assertEqual(str, type(State().id))

    def test_name_is_public_class_attribute(self):
        state = State()
        self.assertEqual(str, type(State.name))
        self.assertIn("name", dir(state))
        self.assertNotIn("name", state.__dict__)

    def test_two_states_unique_ids(self):
        state1 = State()
        state2 = State()
        self.assertNotEqual(state1.id, state2.id)

    def test_two_states_different_created_at(self):
        state1 = State()
        state2 = State()
        self.assertLess(state1.created_at, state2.created_at)

    def test_two_states_different_updated_at(self):
        state1 = State()
        state2 = State()
        self.assertLess(state1.updated_at, state2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        state = State()
        state.id = "789"
        state.created_at = state.updated_at = dt
        state_str = state.__str__()
        self.assertIn("[State] (789)", state_str)
        self.assertIn("'id': '789'", state_str)
        self.assertIn("'created_at': " + dt_repr, state_str)
        self.assertIn("'updated_at': " + dt_repr, state_str)

    def test_args(self):
        state = State(None)
        self.assertNotIn(None, state.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        state = State(id="789", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(state.id, "789")
        self.assertEqual(state.created_at, dt)
        self.assertEqual(state.updated_at, dt)

    def test_instantiation_with_kwargs_None_value(self):
        with self.assertRaises(TypeError):
            State(id=None, created_at=None, updated_at=None)


class TestState_save(unittest.TestCase):
    """Defines unittests for testing the `save` method for State class
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
        state = State()
        first_updated_at = state.updated_at
        state.save()
        self.assertLess(first_updated_at, state.updated_at)

    def test_two_saves(self):
        state = State()
        first_updated_at = state.updated_at
        state.save()
        self.assertLess(first_updated_at, state.updated_at)

        second_updated_at = state.updated_at
        state.save()
        self.assertLess(second_updated_at, state.updated_at)

    def test_save_with_arg(self):
        state = State()
        with self.assertRaises(TypeError):
            state.save(None)

    def test_save_updates_file(self):
        state = State()
        state.save()
        state_id = "State." + state.id
        with open("file.json", "r") as f:
            self.assertIn(state_id, f.read())


class TestState_to_dict(unittest.TestCase):
    """Defines unittests for testing to_dict method of State class
    """

    def test_to_dict_type(self):
        self.assertTrue(dict, type(State().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        state = State()
        self.assertIn("id", state.to_dict())
        self.assertIn("created_at", state.to_dict())
        self.assertIn("updated_at", state.to_dict())
        self.assertIn("__class__", state.to_dict())

    def test_to_dict_contains_added_attributes(self):
        state = State()
        state.middle_name = "Best School"
        state.my_number = 89
        self.assertEqual("Best School", state.middle_name)
        self.assertEqual(89, state.my_number)

    def test_to_dict_datetime_attributes_are_strs(self):
        state = State()
        state_dict = state.to_dict()
        self.assertEqual(str, type(state_dict["id"]))
        self.assertEqual(str, type(state_dict["created_at"]))
        self.assertEqual(str, type(state_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        state = State()
        state.id = "789"
        state.created_at = state.updated_at = dt
        t_dict = {
            'id': '789',
            '__class__': 'State',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(state.to_dict(), t_dict)

    def test_contrast_to_dict_dunder_dict(self):
        state = State()
        self.assertNotEqual(state.to_dict(), state.__dict__)

    def test_to_dict_with_arg(self):
        state = State()
        with self.assertRaises(TypeError):
            state.to_dict(None)


if __name__ == "__main__":
    unittest.main()
