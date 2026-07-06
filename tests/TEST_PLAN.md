# PawPal+ Test Plan
> Interesting! Claude unexpectedly created this file after being asked to "create a draft of tests and do not write code"

## Overview
This document outlines test cases to verify core PawPal functionality and key scheduling behaviors. Tests are organized into four main categories:

1. **Core Functionality** - Basic user workflows (add pet, schedule tasks, view schedule)
2. **Sorting Correctness** - Chronological ordering of tasks
3. **Task Completion & Filtering** - Marking tasks complete and filtering out completed tasks
4. **Conflict Detection** - Detecting and reporting scheduling conflicts

---

## Part 1: Core Functionality Tests

These tests validate the three main user workflows described in requirements.

### Test 1.1: Add a Pet
**Purpose:** Verify that an owner can successfully add a pet to their collection.

**Setup:**
- Create an Owner with name "Alice"

**Steps:**
1. Call `Owner.add_pet()` with name="Biscuit", species="Golden Retriever"
2. Call `Owner.add_pet()` with name="Whiskers", species="Siamese Cat"

**Assertions:**
- Verify `len(owner.pets) == 2`
- Verify first pet has name="Biscuit" and species="Golden Retriever"
- Verify second pet has name="Whiskers" and species="Siamese Cat"
- Verify `add_pet()` returns `(True, message)` with success message

---

### Test 1.2: Add Multiple Tasks for a Pet
**Purpose:** Verify that an owner can add multiple tasks to a single pet.

**Setup:**
- Create Owner and add one pet ("Biscuit")

**Steps:**
1. Add task: "Morning walk", duration=30, due_time=08:00, priority=HIGH
2. Add task: "Lunch and playtime", duration=45, due_time=12:30, priority=MEDIUM
3. Add task: "Evening walk", duration=30, due_time=18:30, priority=HIGH

**Assertions:**
- Verify `len(pet.tasks) == 3`
- Verify each task is in the pet's task list with correct attributes (description, duration, due_time, priority)
- Verify `Owner.add_task_for_pet()` returns `True` for all additions
- Verify adding task to non-existent pet returns `False`

---

### Test 1.3: Add Tasks to Multiple Pets
**Purpose:** Verify that tasks can be added to different pets and kept separate.

**Setup:**
- Create Owner and add two pets ("Biscuit", "Whiskers")

**Steps:**
1. Add "Morning walk" to Biscuit (30 min, due 08:00, HIGH)
2. Add "Feeding" to Whiskers (15 min, due 09:00, HIGH)
3. Add "Lunch and playtime" to Biscuit (45 min, due 12:30, MEDIUM)
4. Add "Litter box cleaning" to Whiskers (10 min, due 18:00, MEDIUM)

**Assertions:**
- Verify Biscuit has 2 tasks
- Verify Whiskers has 2 tasks
- Verify tasks are correctly attributed to each pet (no mixing)
- Verify `Owner.get_tasks_for_pet("Biscuit")` returns Biscuit's tasks only

---

### Test 1.4: View Schedule for Single Pet
**Purpose:** Verify that a user can view the daily schedule for a specific pet.

**Setup:**
- Create Owner with pets and tasks (from Test 1.3)

**Steps:**
1. Call `Owner.generate_str_schedule_for_pet("Biscuit")`

**Assertions:**
- Verify returned string contains "Biscuit" and its species
- Verify returned string includes all of Biscuit's tasks
- Verify tasks appear in the string with scheduled times, descriptions, durations, and priorities
- Verify `generate_str_schedule_for_pet("NonExistent")` returns error message with "not found"

---

### Test 1.5: View Schedule for All Pets
**Purpose:** Verify that a user can view the combined daily schedule for all pets.

**Setup:**
- Create Owner with multiple pets and tasks (from Test 1.3)

**Steps:**
1. Call `Owner.generate_str_schedule_for_all_pets()`

**Assertions:**
- Verify returned string contains "Biscuit" and "Whiskers"
- Verify returned string includes all tasks from all pets
- Verify tasks appear in chronological order by scheduled_time
- Verify each pet's section is clearly labeled
- Verify empty owner (no pets) returns "No pets found." message

---

## Part 2: Sorting Correctness Tests

These tests verify that tasks are correctly ordered chronologically.

### Test 2.1: Tasks Sorted by Scheduled Time
**Purpose:** Verify that after scheduling, tasks appear in chronological order.

**Setup:**
- Create Owner and pet with 4 tasks added in non-chronological order
- Task 1: description="Evening task", due_time=18:00
- Task 2: description="Morning task", due_time=08:00
- Task 3: description="Afternoon task", due_time=14:00
- Task 4: description="Noon task", due_time=12:00

**Steps:**
1. Call `Scheduler.create_schedule()` to schedule all tasks
2. Retrieve scheduled tasks list

**Assertions:**
- Verify tasks are sorted by `scheduled_time` in ascending order
- Verify Task 2 (08:00) appears before Task 4 (12:00)
- Verify Task 4 (12:00) appears before Task 3 (14:00)
- Verify Task 3 (14:00) appears before Task 1 (18:00)

---

### Test 2.2: Unscheduled Tasks Appear Last
**Purpose:** Verify that tasks that couldn't be scheduled appear at the end.

**Setup:**
- Create Owner and pet with 3 tasks:
- Task 1: duration=60, due_time=08:30, priority=HIGH (too long to fit before due_time)
- Task 2: duration=30, due_time=09:00, priority=MEDIUM (fits)
- Task 3: duration=10, due_time=08:45, priority=LOW (fits)

**Steps:**
1. Call `Scheduler.create_schedule()` with start_time=08:00

**Assertions:**
- Verify tasks that fit (Task 2, Task 3) have `scheduled_time` set
- Verify Task 1 has `scheduled_time == None` (couldn't fit)
- Verify unscheduled Task 1 appears after scheduled tasks in output
- Verify `scheduled_time is None` sort key causes unscheduled tasks to sort last

---

### Test 2.3: Sort By Priority Then Due Time
**Purpose:** Verify that scheduler sorts by priority first, then by due_time.

**Setup:**
- Create Owner and pet with 4 tasks:
- Task A: priority=LOW, due_time=08:00, duration=20
- Task B: priority=HIGH, due_time=09:00, duration=20
- Task C: priority=HIGH, due_time=08:30, duration=20
- Task D: priority=MEDIUM, due_time=08:15, duration=20

**Steps:**
1. Call `Scheduler.create_schedule()` with start_time=08:00
2. Examine the sort order before scheduling begins

**Assertions:**
- Verify scheduler sorts HIGH priority tasks before MEDIUM and LOW
- Verify within same priority, earlier due_time comes first (Task C before Task B)
- Verify final scheduled order is: C, B, D, A (HIGH by due_time, then MEDIUM, then LOW)

---

## Part 3: Task Completion & Filtering Tests

These tests verify that completed tasks can be marked and filtered out.

### Test 3.1: Mark Task Complete
**Purpose:** Verify that a task's completion status can be changed.

**Setup:**
- Create a Task with description="Feed dog", due_time=08:00

**Steps:**
1. Verify `task.completed == False` initially
2. Call `task.mark_complete()`
3. Verify `task.completed == True`

**Assertions:**
- Verify initial completed status is False
- Verify mark_complete() sets completed to True
- Verify can mark multiple tasks complete independently

---

### Test 3.2: Filter Out Completed Tasks
**Purpose:** Verify that `Scheduler.filter_out_completed()` removes completed tasks from a pet's list.

**Setup:**
- Create pet with 3 tasks
- Mark Task 1 and Task 3 as complete using `mark_complete()`

**Steps:**
1. Call `Scheduler.filter_out_completed(pet)`

**Assertions:**
- Verify returned list contains only Task 2 (the incomplete task)
- Verify returned list has length 1
- Verify original `pet.tasks` list still has all 3 tasks (not modified)
- Verify completed tasks are excluded from filtered list

---

### Test 3.3: Filter With All Tasks Complete
**Purpose:** Verify filtering behavior when all tasks are marked complete.

**Setup:**
- Create pet with 2 tasks
- Mark both tasks as complete

**Steps:**
1. Call `Scheduler.filter_out_completed(pet)`

**Assertions:**
- Verify returned list is empty
- Verify original pet.tasks list still contains the 2 complete tasks

---

### Test 3.4: Filter With No Tasks Complete
**Purpose:** Verify filtering behavior when no tasks are marked complete.

**Setup:**
- Create pet with 3 tasks
- Do not mark any tasks as complete

**Steps:**
1. Call `Scheduler.filter_out_completed(pet)`

**Assertions:**
- Verify returned list has length 3
- Verify all tasks are included in filtered list
- Verify list matches original pet.tasks

---

### Test 3.5: Filtering Does Not Modify Original List
**Purpose:** Verify that filtering creates a new list without modifying the pet's task list.

**Setup:**
- Create pet with 3 tasks
- Mark one task as complete
- Get original task list length

**Steps:**
1. Call `Scheduler.filter_out_completed(pet)`
2. Check pet.tasks length again

**Assertions:**
- Verify `len(pet.tasks)` is unchanged (still 3)
- Verify filtered list is a new list (different object)
- Verify modifications to filtered list don't affect pet.tasks

---

## Part 4: Conflict Detection Tests

These tests verify that the scheduler detects and reports conflicts.

### Test 4.1: Detect Task That Cannot Fit Before Due Time
**Purpose:** Verify that a task too long to complete before its due_time is marked as skipped.

**Setup:**
- Create Owner and pet with 2 tasks:
- Task 1: description="Long task", duration=120, due_time=09:00, priority=HIGH
- Task 2: description="Short task", duration=30, due_time=10:00, priority=LOW

**Steps:**
1. Call `Scheduler.create_schedule()` with start_time=08:00
2. Check scheduled tasks and skipped_str output

**Assertions:**
- Verify Task 1 is in skipped list (can't fit 120 min before 09:00)
- Verify Task 1 has `scheduled_time == None`
- Verify Task 2 is scheduled (fits before its due_time)
- Verify skipped_str contains "Long task" and mentions the conflict
- Verify skipped_str mentions due_time "09:00"

---

### Test 4.2: Detect Overlapping Scheduled Tasks
**Purpose:** Verify that when tasks would overlap, later ones are skipped appropriately.

**Setup:**
- Create Owner and pet with 3 tasks all with different priorities:
- Task 1: duration=60, due_time=10:00, priority=MEDIUM
- Task 2: duration=60, due_time=11:00, priority=MEDIUM
- Task 3: duration=30, due_time=12:00, priority=LOW

**Steps:**
1. Call `Scheduler.create_schedule()` with start_time=08:00, interval=HOUR
2. Check which tasks are scheduled and which are skipped

**Assertions:**
- Verify Task 1 is scheduled at 08:00 (ends 09:00)
- Verify Task 2 cannot fit (would need 10:00-11:00 but due time is 11:00, ends at 11:00 which is okay)
- Actually: Task 2 starts 09:00 (after Task 1), ends 10:00, fits before due_time 11:00
- Verify Task 3 starts 10:00 (after Task 2), ends 10:30, fits before due_time 12:00

---

### Test 4.3: Conflict Detection Across Multiple Pets
**Purpose:** Verify that the scheduler detects conflicts when scheduling tasks from multiple pets together.

**Setup:**
- Create Owner with 2 pets and 4 tasks total:
- Biscuit Task 1: duration=45, due_time=09:00, priority=HIGH
- Biscuit Task 2: duration=30, due_time=10:00, priority=MEDIUM
- Whiskers Task 1: duration=60, due_time=09:30, priority=HIGH
- Whiskers Task 2: duration=20, due_time=11:00, priority=LOW

**Steps:**
1. Call `Scheduler.create_schedule_for_owner()`
2. Check scheduled and skipped tasks

**Assertions:**
- Verify high-priority tasks are scheduled first
- Verify Whiskers Task 1 (HIGH, due 09:30) cannot fit 60 minutes before 09:30 - should be skipped
- Verify Biscuit Task 1 (HIGH, due 09:00) fits before 09:00
- Verify skipped_str names both pet and task for each conflict
- Verify skipped_str includes due_time and duration for each skipped task

---

### Test 4.4: No Conflicts With Properly Spaced Tasks
**Purpose:** Verify that well-spaced tasks are all successfully scheduled with no conflicts.

**Setup:**
- Create Owner and pet with 4 tasks with ample time spacing:
- Task 1: duration=30, due_time=09:00, priority=HIGH
- Task 2: duration=30, due_time=10:00, priority=MEDIUM
- Task 3: duration=30, due_time=11:00, priority=MEDIUM
- Task 4: duration=30, due_time=12:00, priority=LOW

**Steps:**
1. Call `Scheduler.create_schedule()` with start_time=08:00, interval=HOUR

**Assertions:**
- Verify all 4 tasks are scheduled (no skipped tasks)
- Verify skipped_str is empty
- Verify scheduled_time is set on all tasks
- Verify Task 1 at 08:00, Task 2 at 09:00, Task 3 at 10:00, Task 4 at 11:00

---

### Test 4.5: Skipped Task Report Includes Required Details
**Purpose:** Verify that the skipped task summary includes all relevant information.

**Setup:**
- Create Owner and pet with 1 task that will be skipped:
- Task: description="Afternoon nap", duration=90, due_time=14:00, priority=MEDIUM

**Steps:**
1. Call `Scheduler.create_schedule()` with start_time=08:00
2. Capture skipped_str output

**Assertions:**
- Verify skipped_str contains "Skipped due to conflicts:"
- Verify skipped_str contains pet name
- Verify skipped_str contains task description ("Afternoon nap")
- Verify skipped_str contains due_time ("14:00")
- Verify skipped_str contains duration ("90 min")
- Verify skipped_str contains priority level

---

## Test Execution Summary

**Total Test Cases:** 20+

**Test Coverage:**
- Core Functionality: 5 tests (pet/task management, viewing schedules)
- Sorting Correctness: 3 tests (chronological order, priority, edge cases)
- Task Completion & Filtering: 5 tests (marking, filtering, non-modification)
- Conflict Detection: 5+ tests (individual conflicts, multi-pet, spacing, reporting)

**Testing Tools:** pytest

**Run Command:** `pytest tests/test_pawpal.py -v`

---

## Integration Test (Bonus)

### Test 5.1: Full Workflow
**Purpose:** Verify the entire workflow from scratch.

**Steps:**
1. Create Owner with start_time and time_increment
2. Add two pets
3. Add multiple tasks to each pet
4. Generate schedule for all pets
5. Mark some tasks complete
6. Generate filtered schedule
7. Verify no conflicts in final output

**Assertions:**
- All three main user tasks work together correctly
- Data persists across operations
- UI would receive properly formatted, sorted schedule data
