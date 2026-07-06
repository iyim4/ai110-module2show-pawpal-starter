# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
==================================================
Today's Schedule for Alice
==================================================

Daily plan for Biscuit (Golden Retriever):
  08:00 — Morning walk (30 min) [priority: high]
  12:30 — Lunch and playtime (45 min) [priority: medium]
  18:30 — Evening walk (30 min) [priority: high]

Daily plan for Whiskers (Siamese Cat):
  09:00 — Feeding (15 min) [priority: high]
  18:00 — Litter box cleaning (10 min) [priority: medium]
==================================================
```

## 🧪 Testing PawPal+

Tests verify the three core user tasks: adding pets, scheduling tasks, and viewing schedules. They validate data integrity through sorting (chronological order, priority-based), filtering (completed tasks), and conflict detection (tasks that can't fit before due times). Coverage spans single and multi-pet scenarios with edge cases for empty states and scheduling constraints.

```bash
# Run the full test suite:
python -m pytest tests/test_pawpal.py -v

# Run with coverage:
pytest --cov
```

Sample test output:

```
================================ test session starts =================================
platform win32 -- Python 3.13.1, pytest-9.0.3, pluggy-1.6.0 -- C:\Python313\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\isayi\CLASSES\AI110\ai110-module2show-pawpal-starter
plugins: anyio-4.13.0
collected 19 items                                                                    

tests/test_pawpal.py::test_add_pet PASSED                                       [  5%]
tests/test_pawpal.py::test_add_multiple_tasks_to_pet PASSED                     [ 10%]
tests/test_pawpal.py::test_add_tasks_to_multiple_pets PASSED                    [ 15%]
tests/test_pawpal.py::test_view_schedule_for_single_pet PASSED                  [ 21%]
tests/test_pawpal.py::test_view_schedule_for_all_pets PASSED                    [ 26%]
tests/test_pawpal.py::test_tasks_sorted_by_scheduled_time PASSED                [ 31%]
tests/test_pawpal.py::test_unscheduled_tasks_appear_last PASSED                 [ 36%]
tests/test_pawpal.py::test_sort_by_priority_then_due_time PASSED                [ 42%]
tests/test_pawpal.py::test_task_completion PASSED                               [ 47%]
tests/test_pawpal.py::test_filter_out_completed_tasks PASSED                    [ 52%]
tests/test_pawpal.py::test_filter_with_all_tasks_complete PASSED                [ 57%]
tests/test_pawpal.py::test_filter_with_no_tasks_complete PASSED                 [ 63%]
tests/test_pawpal.py::test_add_tasks_to_pet PASSED                              [ 68%]
tests/test_pawpal.py::test_filtering_does_not_modify_original PASSED            [ 73%]
tests/test_pawpal.py::test_detect_task_cannot_fit_before_due_time PASSED        [ 78%]
tests/test_pawpal.py::test_detect_overlapping_scheduled_tasks PASSED            [ 84%]
tests/test_pawpal.py::test_conflict_detection_across_multiple_pets PASSED       [ 89%]
tests/test_pawpal.py::test_no_conflicts_with_properly_spaced_tasks PASSED       [ 94%]
tests/test_pawpal.py::test_skipped_task_report_includes_details PASSED          [100%]

================================= 19 passed in 0.06s =================================
```
- Confidence Level 5/5 system reliablity, thorough tests

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler._task_sort_key()`, `Scheduler.sort_by_time()`, `Scheduler.create_schedule()` | Primary sort by priority (high to low); secondary sort by due_time (early to late) |
| Filtering | `Scheduler.filter_out_completed()`, `Scheduler.create_schedule()` | Filter out completed tasks, skip tasks that can't fit before their due_time |
| Conflict handling | `Scheduler.create_schedule()`, `Scheduler._format_skipped_tasks()` | Detects when tasks conflict with time slots; generates skipped task summary with reason |
| Recurring tasks | `Task.frequency` property, `TimeFrequency` enum (DAILY/WEEKLY) | Frequency stored on each task |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
