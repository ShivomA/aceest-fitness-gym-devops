import pytest
import tkinter as tk
from unittest.mock import patch
from datetime import datetime
from ACEest_Fitness import FitnessTrackerApp


@pytest.fixture
def app_instance():
    root = tk.Tk()
    app = FitnessTrackerApp(root)
    yield app
    root.destroy()


# ---------------------------
# TEST: Add Valid Workout
# ---------------------------
@patch("tkinter.messagebox.showinfo")
def test_add_valid_workout(mock_info, app_instance):
    app = app_instance

    app.category_var.set("Warm-up")
    app.workout_entry.insert(0, "Jumping Jacks")
    app.duration_entry.insert(0, "5")

    app.add_workout()

    assert len(app.workouts["Warm-up"]) == 1
    entry = app.workouts["Warm-up"][0]
    assert entry["exercise"] == "Jumping Jacks"
    assert entry["duration"] == 5
    assert "timestamp" in entry

    mock_info.assert_called_once()


# ---------------------------
# TEST: Invalid Duration
# ---------------------------
@patch("tkinter.messagebox.showerror")
def test_add_invalid_duration(mock_error, app_instance):
    app = app_instance

    app.category_var.set("Workout")
    app.workout_entry.insert(0, "Pushups")
    app.duration_entry.insert(0, "abc")

    app.add_workout()

    assert len(app.workouts["Workout"]) == 0
    mock_error.assert_called_once()


# ---------------------------
# TEST: Empty Inputs
# ---------------------------
@patch("tkinter.messagebox.showerror")
def test_add_empty_fields(mock_error, app_instance):
    app = app_instance

    app.workout_entry.insert(0, "")
    app.duration_entry.insert(0, "")

    app.add_workout()
    assert not any(app.workouts.values())
    mock_error.assert_called_once()


# ---------------------------
# TEST: Multiple Categories
# ---------------------------
@patch("tkinter.messagebox.showinfo")
def test_add_workouts_in_multiple_categories(_mock_info, app_instance):
    app = app_instance

    # Warm-up entry
    app.category_var.set("Warm-up")
    app.workout_entry.insert(0, "Stretching")
    app.duration_entry.insert(0, "10")
    app.add_workout()

    # Workout entry
    app.category_var.set("Workout")
    app.workout_entry.insert(0, "Deadlifts")
    app.duration_entry.insert(0, "20")
    app.add_workout()

    assert len(app.workouts["Warm-up"]) == 1
    assert len(app.workouts["Workout"]) == 1
    assert app.workouts["Warm-up"][0]["exercise"] == "Stretching"
    assert app.workouts["Workout"][0]["exercise"] == "Deadlifts"


# ---------------------------
# TEST: Summary With No Entries
# ---------------------------
@patch("tkinter.messagebox.showinfo")
def test_view_summary_empty(mock_info, app_instance):
    app = app_instance
    app.view_summary()
    mock_info.assert_called_once_with("Summary", "No sessions logged yet!")


# ---------------------------
# TEST: Summary With Entries
# ---------------------------
@patch("tkinter.Toplevel")
@patch("tkinter.messagebox.showinfo")
def test_view_summary_nonempty(mock_info, mock_window, app_instance):
    app = app_instance

    # Add one entry
    app.category_var.set("Cool-down")
    app.workout_entry.insert(0, "Light Walk")
    app.duration_entry.insert(0, "8")
    app.add_workout()

    app.view_summary()

    # Called once for "Success" popup
    assert mock_info.call_count == 1

    # Summary should create a Toplevel window
    assert mock_window.called


# ---------------------------
# TEST: Status Bar Update
# ---------------------------
@patch("tkinter.messagebox.showinfo")
def test_status_bar_updates(_mock_info, app_instance):
    app = app_instance

    app.category_var.set("Workout")
    app.workout_entry.insert(0, "Squats")
    app.duration_entry.insert(0, "15")
    app.add_workout()

    assert "Added Squats (15 min) to Workout!" in app.status_label.cget("text")
