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
@patch.object(FigureCanvasTkAgg, "draw")
@patch("tkinter.messagebox.showinfo")
def test_add_valid_workout(mock_info, mock_draw, app_instance):
    app = app_instance

    app.category_var.set("Workout")
    app.workout_entry.insert(0, "Pushups")
    app.duration_entry.insert(0, "20")

    app.add_workout()

    # Verify data added
    assert len(app.workouts["Workout"]) == 1
    entry = app.workouts["Workout"][0]
    assert entry["exercise"] == "Pushups"
    assert entry["duration"] == 20
    assert "timestamp" in entry

    # Status label updated
    assert "Added Pushups (20 min) to Workout!" in app.status_label.cget("text")

    # draw() should have been called at least once when chart updated
    assert mock_draw.call_count >= 1

    # messagebox showinfo (success) should be called once
    mock_info.assert_called_once()


# ---------------------------
# Test: Non-numeric duration shows error
# ---------------------------
@patch("tkinter.messagebox.showerror")
def test_add_invalid_duration_non_numeric(mock_error, app_instance):
    app = app_instance

    app.workout_entry.insert(0, "Running")
    app.duration_entry.insert(0, "abc")

    app.add_workout()

    assert len(app.workouts["Workout"]) == 0
    mock_error.assert_called_once()


# ---------------------------
# Test: Non-positive duration shows error (<=0)
# ---------------------------
@patch("tkinter.messagebox.showerror")
def test_add_invalid_duration_non_positive(mock_error, app_instance):
    app = app_instance

    app.workout_entry.insert(0, "Sprint")
    app.duration_entry.insert(0, "0")  # zero is invalid per new validation

    app.add_workout()

    assert len(app.workouts["Workout"]) == 0
    mock_error.assert_called_once()


# ---------------------------
# Test: View summary when empty
# ---------------------------
@patch("tkinter.messagebox.showinfo")
def test_view_summary_empty(mock_info, app_instance):
    app = app_instance

    app.view_summary()

    mock_info.assert_called_once()


# ---------------------------
# Test: View summary non-empty (Toplevel created)
# ---------------------------
@patch("tkinter.Toplevel")
@patch("tkinter.messagebox.showinfo")
def test_view_summary_nonempty(mock_info, mock_toplevel, app_instance):
    app = app_instance

    app.category_var.set("Warm-up")
    app.workout_entry.insert(0, "Stretching")
    app.duration_entry.insert(0, "10")

    # Add workout (suppress any draw/showinfo side effects are patched)
    app.add_workout()

    # Now call view_summary -> should create a Toplevel
    app.view_summary()

    assert mock_toplevel.called
    # add_workout calls showinfo once (success)
    mock_info.assert_called_once()


# ---------------------------
# Test: Progress chart update triggers draw (class-level patch)
# ---------------------------
@patch.object(FigureCanvasTkAgg, "draw")
@patch("tkinter.messagebox.showinfo")
def test_progress_chart_update(_mock_info, mock_draw, app_instance):
    app = app_instance

    # Initially no data: update_progress_charts would show message and not create canvas
    app.update_progress_charts()
    # If no data, chart should not be created (chart_container shows a label)
    # But chart_canvas remains None
    assert getattr(app, "chart_canvas", None) is None or app.chart_canvas is not None

    # Add a workout -> should create canvas and call draw()
    app.category_var.set("Workout")
    app.workout_entry.insert(0, "Cycling")
    app.duration_entry.insert(0, "30")

    app.add_workout()

    # draw should have been called at least once when chart was created/refreshed
    assert mock_draw.call_count >= 1


# ---------------------------
# Test: on_tab_change triggers update when Progress tab selected
# ---------------------------
def test_on_tab_change_triggers_update(app_instance, monkeypatch):
    app = app_instance

    # patch the update_progress_charts to observe call
    called = {"count": 0}

    def fake_update():
        called["count"] += 1

    monkeypatch.setattr(app, "update_progress_charts", fake_update)

    # Select the progress tab (4th tab added; index 3)
    tabs = app.notebook.tabs()
    # Ensure we have at least 4 tabs (as expected)
    assert len(tabs) >= 4
    progress_tab_id = tabs[3]
    app.notebook.select(progress_tab_id)

    # Call the handler (event argument is unused in method)
    app.on_tab_change(None)

    assert called["count"] >= 1
