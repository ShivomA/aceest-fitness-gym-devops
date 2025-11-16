import pytest
import tkinter as tk
from unittest.mock import patch
from ACEest_Fitness import FitnessTrackerApp
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


@pytest.fixture
def app_instance():
    root = tk.Tk()
    root.withdraw()  # Prevent actual GUI popup
    app = FitnessTrackerApp(root)
    yield app
    root.destroy()


# ---------------------------
# TEST 1: Add Valid Workout
# ---------------------------
@patch("tkinter.messagebox.showinfo")
def test_add_valid_workout(mock_info, app_instance):
    app = app_instance

    app.category_var.set("Workout")
    app.workout_entry.insert(0, "Pushups")
    app.duration_entry.insert(0, "20")

    with patch.object(app, "update_progress_charts") as mock_chart:
        app.add_workout()

    assert len(app.workouts["Workout"]) == 1
    entry = app.workouts["Workout"][0]

    assert entry["exercise"] == "Pushups"
    assert entry["duration"] == 20
    assert "timestamp" in entry

    mock_info.assert_called_once()
    mock_chart.assert_called_once()


# ---------------------------
# TEST 2: Invalid Duration
# ---------------------------
@patch("tkinter.messagebox.showerror")
def test_invalid_duration(mock_error, app_instance):
    app = app_instance

    app.workout_entry.insert(0, "Running")
    app.duration_entry.insert(0, "abc")

    app.add_workout()

    assert len(app.workouts["Workout"]) == 0
    mock_error.assert_called_once()


# ---------------------------
# TEST 3: Empty Fields
# ---------------------------
@patch("tkinter.messagebox.showerror")
def test_empty_inputs(mock_error, app_instance):
    app = app_instance

    app.workout_entry.insert(0, "")
    app.duration_entry.insert(0, "")

    app.add_workout()

    assert not any(app.workouts.values())
    mock_error.assert_called_once()


# ---------------------------
# TEST 4: Add to Multiple Categories
# ---------------------------
@patch("tkinter.messagebox.showinfo")
def test_add_multiple_categories(_mock_info, app_instance):
    app = app_instance

    # Warm-up
    app.category_var.set("Warm-up")
    app.workout_entry.insert(0, "Stretching")
    app.duration_entry.insert(0, "5")
    app.add_workout()

    # Cool-down
    app.category_var.set("Cool-down")
    app.workout_entry.insert(0, "Yoga")
    app.duration_entry.insert(0, "7")
    app.add_workout()

    assert len(app.workouts["Warm-up"]) == 1
    assert len(app.workouts["Cool-down"]) == 1
    assert app.workouts["Warm-up"][0]["exercise"] == "Stretching"
    assert app.workouts["Cool-down"][0]["exercise"] == "Yoga"


# ---------------------------
# TEST 5: Summary View (Empty)
# ---------------------------
@patch("tkinter.messagebox.showinfo")
def test_view_summary_empty(mock_info, app_instance):
    app = app_instance
    app.view_summary()
    mock_info.assert_called_once_with("Summary", "No sessions logged yet!")


# ---------------------------
# TEST 6: Summary View (Non-empty)
# ---------------------------
@patch("tkinter.Toplevel")
@patch("tkinter.messagebox.showinfo")
def test_view_summary_nonempty(mock_info, mock_top, app_instance):
    app = app_instance

    app.category_var.set("Workout")
    app.workout_entry.insert(0, "Curl")
    app.duration_entry.insert(0, "10")
    app.add_workout()

    app.view_summary()

    # one "Success" popup + summary window created
    assert mock_info.call_count == 1
    assert mock_top.called


# ---------------------------
# TEST 7: Status Bar Updates
# ---------------------------
@patch("tkinter.messagebox.showinfo")
def test_status_bar_update(_mock_info, app_instance):
    app = app_instance

    app.category_var.set("Workout")
    app.workout_entry.insert(0, "Squats")
    app.duration_entry.insert(0, "15")

    app.add_workout()

    assert "Added Squats (15 min) to Workout!" in app.status_label.cget("text")


# ---------------------------
# TEST 8: Progress Chart Updates
# ---------------------------
@patch.object(FigureCanvasTkAgg, "draw")
def test_progress_chart_update(mock_draw, app_instance):
    app = app_instance

    # Build initial chart
    app.update_progress_charts()
    assert app.progress_canvas is not None

    # Add workout
    app.category_var.set("Warm-up")
    app.workout_entry.insert(0, "Jogging")
    app.duration_entry.insert(0, "10")

    with patch("tkinter.messagebox.showinfo"):
        app.add_workout()

    # draw() should have been called at least once when the chart refreshed
    assert mock_draw.call_count >= 1
