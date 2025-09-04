import pytest
import tkinter as tk
from unittest.mock import patch
from ACEest_Fitness import FitnessTrackerApp

@pytest.fixture
def app_instance():
    root = tk.Tk()
    app = FitnessTrackerApp(root)
    yield app
    root.destroy()

@patch("tkinter.messagebox.showinfo")
def test_add_valid_workout(_mock_info, app_instance):
    app = app_instance
    app.workout_entry.insert(0, "Pushups")
    app.duration_entry.insert(0, "15")
    app.add_workout()
    assert len(app.workouts) == 1
    assert app.workouts[0]["workout"] == "Pushups"
    assert app.workouts[0]["duration"] == 15

@patch("tkinter.messagebox.showerror")
def test_add_invalid_duration(_mock_error, app_instance):
    app = app_instance
    app.workout_entry.insert(0, "Running")
    app.duration_entry.insert(0, "abc")
    app.add_workout()
    assert len(app.workouts) == 0

@patch("tkinter.messagebox.showerror")
def test_add_empty_fields(_mock_error, app_instance):
    app = app_instance
    app.workout_entry.insert(0, "")
    app.duration_entry.insert(0, "")
    app.add_workout()
    assert len(app.workouts) == 0

@patch("tkinter.messagebox.showinfo")
def test_multiple_workouts(_mock_info, app_instance):
    app = app_instance
    # First workout
    app.workout_entry.insert(0, "Squats")
    app.duration_entry.insert(0, "10")
    app.add_workout()
    # Second workout
    app.workout_entry.insert(0, "Plank")
    app.duration_entry.insert(0, "5")
    app.add_workout()
    assert len(app.workouts) == 2
    assert app.workouts[0]["workout"] == "Squats"
    assert app.workouts[1]["workout"] == "Plank"

@patch("tkinter.messagebox.showinfo")
def test_view_workouts_empty(mock_info, app_instance):
    app = app_instance
    app.view_workouts()
    mock_info.assert_called_once_with("Workouts", "No workouts logged yet.")

@patch("tkinter.messagebox.showinfo")
def test_view_workouts_nonempty(mock_info, app_instance):
    app = app_instance
    app.workout_entry.insert(0, "Yoga")
    app.duration_entry.insert(0, "30")
    app.add_workout()
    app.view_workouts()
    assert mock_info.call_count == 2  # one from add_workout, one from view_workouts
    call_args = mock_info.call_args_list[-1][0]
    assert "Yoga" in call_args[1]  # message text contains "Yoga"
