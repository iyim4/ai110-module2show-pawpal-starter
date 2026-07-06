from pawpal_system import Pet, Task, Priority, TimeFrequency, Owner, Scheduler, TimeIncrement
from datetime import time


# ============================================================================
# PART 1: CORE FUNCTIONALITY TESTS
# ============================================================================

def test_add_pet():
    """Test 1.1: Verify that an owner can successfully add pets."""
    owner = Owner("Alice")

    success, msg = owner.add_pet("Biscuit", "Golden Retriever")
    assert success is True
    assert "Biscuit" in msg

    success, msg = owner.add_pet("Whiskers", "Siamese Cat")
    assert success is True
    assert "Whiskers" in msg

    assert len(owner.pets) == 2
    assert owner.pets[0].name == "Biscuit"
    assert owner.pets[0].species == "Golden Retriever"
    assert owner.pets[1].name == "Whiskers"
    assert owner.pets[1].species == "Siamese Cat"


def test_add_multiple_tasks_to_pet():
    """Test 1.2: Verify that multiple tasks can be added to a single pet."""
    owner = Owner("Alice")
    owner.add_pet("Biscuit", "Golden Retriever")

    success = owner.add_task_for_pet(
        "Biscuit", "Morning walk", 30, time(8, 0), priority=Priority.HIGH
    )
    assert success is True

    success = owner.add_task_for_pet(
        "Biscuit", "Lunch and playtime", 45, time(12, 30), priority=Priority.MEDIUM
    )
    assert success is True

    success = owner.add_task_for_pet(
        "Biscuit", "Evening walk", 30, time(18, 30), priority=Priority.HIGH
    )
    assert success is True

    tasks = owner.get_tasks_for_pet("Biscuit")
    assert len(tasks) == 3
    assert tasks[0].description == "Morning walk"
    assert tasks[0].duration == 30
    assert tasks[0].priority == Priority.HIGH
    assert tasks[1].description == "Lunch and playtime"
    assert tasks[2].description == "Evening walk"


def test_add_tasks_to_multiple_pets():
    """Test 1.3: Verify tasks are kept separate per pet."""
    owner = Owner("Alice")
    owner.add_pet("Biscuit", "Golden Retriever")
    owner.add_pet("Whiskers", "Siamese Cat")

    owner.add_task_for_pet("Biscuit", "Morning walk", 30, time(8, 0), priority=Priority.HIGH)
    owner.add_task_for_pet("Whiskers", "Feeding", 15, time(9, 0), priority=Priority.HIGH)
    owner.add_task_for_pet("Biscuit", "Lunch and playtime", 45, time(12, 30), priority=Priority.MEDIUM)
    owner.add_task_for_pet("Whiskers", "Litter box cleaning", 10, time(18, 0), priority=Priority.MEDIUM)

    biscuit_tasks = owner.get_tasks_for_pet("Biscuit")
    whiskers_tasks = owner.get_tasks_for_pet("Whiskers")

    assert len(biscuit_tasks) == 2
    assert len(whiskers_tasks) == 2
    assert biscuit_tasks[0].description == "Morning walk"
    assert biscuit_tasks[1].description == "Lunch and playtime"
    assert whiskers_tasks[0].description == "Feeding"
    assert whiskers_tasks[1].description == "Litter box cleaning"


def test_view_schedule_for_single_pet():
    """Test 1.4: Verify viewing schedule for a specific pet."""
    owner = Owner("Alice", start_time=time(8, 0))
    owner.add_pet("Biscuit", "Golden Retriever")
    owner.add_task_for_pet("Biscuit", "Morning walk", 30, time(8, 0), priority=Priority.HIGH)
    owner.add_task_for_pet("Biscuit", "Lunch and playtime", 45, time(12, 30), priority=Priority.MEDIUM)

    schedule = owner.generate_str_schedule_for_pet("Biscuit")

    assert "Biscuit" in schedule
    assert "Golden Retriever" in schedule
    assert "Morning walk" in schedule
    assert "Lunch and playtime" in schedule

    # Test non-existent pet
    schedule_invalid = owner.generate_str_schedule_for_pet("NonExistent")
    assert "not found" in schedule_invalid


def test_view_schedule_for_all_pets():
    """Test 1.5: Verify viewing schedule for all pets."""
    owner = Owner("Alice", start_time=time(8, 0))
    owner.add_pet("Biscuit", "Golden Retriever")
    owner.add_pet("Whiskers", "Siamese Cat")
    owner.add_task_for_pet("Biscuit", "Morning walk", 30, time(8, 0), priority=Priority.HIGH)
    owner.add_task_for_pet("Whiskers", "Feeding", 15, time(9, 0), priority=Priority.HIGH)
    owner.add_task_for_pet("Biscuit", "Lunch and playtime", 45, time(12, 30), priority=Priority.MEDIUM)
    owner.add_task_for_pet("Whiskers", "Litter box cleaning", 10, time(18, 0), priority=Priority.MEDIUM)

    schedule = owner.generate_str_schedule_for_all_pets()

    assert "Biscuit" in schedule
    assert "Whiskers" in schedule
    assert "Morning walk" in schedule
    assert "Feeding" in schedule
    assert "Lunch and playtime" in schedule
    assert "Litter box cleaning" in schedule

    # Test empty owner
    empty_owner = Owner("Bob")
    empty_schedule = empty_owner.generate_str_schedule_for_all_pets()
    assert "No pets found" in empty_schedule


# ============================================================================
# PART 2: SORTING CORRECTNESS TESTS
# ============================================================================

def test_tasks_sorted_by_scheduled_time():
    """Test 2.1: Verify tasks are sorted chronologically after scheduling."""
    owner = Owner("Alice", start_time=time(8, 0))
    owner.add_pet("Buddy", "Dog")

    # Add tasks in non-chronological order
    owner.add_task_for_pet("Buddy", "Evening task", 30, time(18, 0), priority=Priority.MEDIUM)
    owner.add_task_for_pet("Buddy", "Morning task", 30, time(8, 0), priority=Priority.MEDIUM)
    owner.add_task_for_pet("Buddy", "Afternoon task", 30, time(14, 0), priority=Priority.MEDIUM)
    owner.add_task_for_pet("Buddy", "Noon task", 30, time(12, 0), priority=Priority.MEDIUM)

    pet = owner.pets[0]
    tasks_with_pet = [(pet.name, task) for task in pet.tasks]
    scheduled, _ = Scheduler.create_schedule(tasks_with_pet, time(8, 0), TimeIncrement.HOUR)

    # Verify chronological order (filter out unscheduled tasks)
    scheduled_with_times = [t for t in scheduled if t.scheduled_time is not None]
    for i in range(len(scheduled_with_times) - 1):
        curr_time = scheduled_with_times[i].scheduled_time
        next_time = scheduled_with_times[i + 1].scheduled_time
        assert curr_time is not None and next_time is not None
        assert curr_time <= next_time


def test_unscheduled_tasks_appear_last():
    """Test 2.2: Verify tasks that can't fit before due_time are skipped."""
    owner = Owner("Alice", start_time=time(8, 0))
    owner.add_pet("Buddy", "Dog")

    # Task 1: too long to fit before due_time (120 min task, due at 09:00)
    owner.add_task_for_pet("Buddy", "Long task", 120, time(9, 0), priority=Priority.HIGH)
    # Task 2: fits easily (30 min task, due at 12:00)
    owner.add_task_for_pet("Buddy", "Short task", 30, time(12, 0), priority=Priority.MEDIUM)

    pet = owner.pets[0]
    tasks_with_pet = [(pet.name, task) for task in pet.tasks]
    scheduled, skipped_str = Scheduler.create_schedule(tasks_with_pet, time(8, 0), TimeIncrement.HOUR)

    # Verify scheduled list only contains successfully scheduled tasks
    assert len(scheduled) == 1  # Only "Short task" gets scheduled
    assert scheduled[0].description == "Short task"
    assert scheduled[0].scheduled_time is not None

    # Verify skipped report mentions the conflicting task
    assert "Long task" in skipped_str
    assert "09:00" in skipped_str


def test_sort_by_priority_then_due_time():
    """Test 2.3: Verify scheduler prioritizes by priority first, then due_time."""
    owner = Owner("Alice", start_time=time(8, 0))
    owner.add_pet("Buddy", "Dog")

    # Create tasks with generous due times so they all fit
    # Task A: LOW priority, due 14:00 (plenty of time)
    owner.add_task_for_pet("Buddy", "Task A", 20, time(14, 0), priority=Priority.LOW)
    # Task B: HIGH priority, due 13:00 (plenty of time)
    owner.add_task_for_pet("Buddy", "Task B", 20, time(13, 0), priority=Priority.HIGH)
    # Task C: HIGH priority, due 12:00 (due earlier than B)
    owner.add_task_for_pet("Buddy", "Task C", 20, time(12, 0), priority=Priority.HIGH)
    # Task D: MEDIUM priority, due 13:30 (plenty of time)
    owner.add_task_for_pet("Buddy", "Task D", 20, time(13, 30), priority=Priority.MEDIUM)

    pet = owner.pets[0]
    tasks_with_pet = [(pet.name, task) for task in pet.tasks]
    scheduled, _ = Scheduler.create_schedule(tasks_with_pet, time(8, 0), TimeIncrement.HOUR)

    # Verify only scheduled tasks in result
    scheduled_tasks = [t for t in scheduled if t.scheduled_time is not None]
    descriptions = [t.description for t in scheduled_tasks]

    # Expected order: C (HIGH, 12:00), B (HIGH, 13:00), D (MEDIUM), A (LOW)
    assert descriptions[0] == "Task C"  # HIGH priority, earliest due_time
    assert descriptions[1] == "Task B"  # HIGH priority, later due_time
    assert descriptions[2] == "Task D"  # MEDIUM priority
    assert descriptions[3] == "Task A"  # LOW priority


# ============================================================================
# PART 3: TASK COMPLETION & FILTERING TESTS
# ============================================================================

def test_task_completion():
    """Test 3.1: Verify that calling mark_complete() changes the task's status."""
    task = Task(
        description="Feed the dog",
        duration=10,
        due_time=time(8, 0),
        frequency=TimeFrequency.DAILY,
        priority=Priority.HIGH,
    )

    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_filter_out_completed_tasks():
    """Test 3.2: Verify that filter_out_completed removes completed tasks."""
    pet = Pet(name="Buddy", species="Dog")

    pet.add_task("Task 1", 30, time(8, 0))
    pet.add_task("Task 2", 30, time(9, 0))
    pet.add_task("Task 3", 30, time(10, 0))

    # Mark task 1 and 3 as complete
    pet.tasks[0].mark_complete()
    pet.tasks[2].mark_complete()

    filtered = Scheduler.filter_out_completed(pet)

    assert len(filtered) == 1
    assert filtered[0].description == "Task 2"
    # Verify original list still has all 3
    assert len(pet.tasks) == 3


def test_filter_with_all_tasks_complete():
    """Test 3.3: Verify filtering when all tasks are complete."""
    pet = Pet(name="Buddy", species="Dog")

    pet.add_task("Task 1", 30, time(8, 0))
    pet.add_task("Task 2", 30, time(9, 0))

    pet.tasks[0].mark_complete()
    pet.tasks[1].mark_complete()

    filtered = Scheduler.filter_out_completed(pet)

    assert len(filtered) == 0
    assert len(pet.tasks) == 2


def test_filter_with_no_tasks_complete():
    """Test 3.4: Verify filtering when no tasks are complete."""
    pet = Pet(name="Buddy", species="Dog")

    pet.add_task("Task 1", 30, time(8, 0))
    pet.add_task("Task 2", 30, time(9, 0))
    pet.add_task("Task 3", 30, time(10, 0))

    filtered = Scheduler.filter_out_completed(pet)

    assert len(filtered) == 3
    assert filtered[0].description == "Task 1"
    assert filtered[1].description == "Task 2"
    assert filtered[2].description == "Task 3"


def test_add_tasks_to_pet():
    """Test 3.5: Verify that adding a task to a Pet increases that pet's task count."""
    pet = Pet(name="Buddy", species="Golden Retriever")

    assert len(pet.tasks) == 0

    pet.add_task(description="Morning walk", duration=30, due_time=time(8, 0))
    assert len(pet.tasks) == 1

    pet.add_task(
        description="Feeding", duration=10, due_time=time(12, 0), priority=Priority.HIGH
    )
    assert len(pet.tasks) == 2


def test_filtering_does_not_modify_original():
    """Test 3.5b: Verify filtering doesn't modify the original list."""
    pet = Pet(name="Buddy", species="Dog")

    pet.add_task("Task 1", 30, time(8, 0))
    pet.add_task("Task 2", 30, time(9, 0))
    pet.add_task("Task 3", 30, time(10, 0))

    pet.tasks[1].mark_complete()
    original_length = len(pet.tasks)

    filtered = Scheduler.filter_out_completed(pet)

    assert len(pet.tasks) == original_length
    assert len(filtered) == 2
    assert filtered is not pet.tasks


# ============================================================================
# PART 4: CONFLICT DETECTION TESTS
# ============================================================================

def test_detect_task_cannot_fit_before_due_time():
    """Test 4.1: Verify tasks too long to fit before due_time are skipped."""
    owner = Owner("Alice", start_time=time(8, 0))
    owner.add_pet("Buddy", "Dog")

    # Task 1: 120 min task with due time 09:00 (won't fit, needs to complete by 09:00)
    owner.add_task_for_pet("Buddy", "Long task", 120, time(9, 0), priority=Priority.HIGH)
    # Task 2: 30 min task with due time 11:00 (fits easily)
    owner.add_task_for_pet("Buddy", "Short task", 30, time(11, 0), priority=Priority.LOW)

    pet = owner.pets[0]
    tasks_with_pet = [(pet.name, task) for task in pet.tasks]
    scheduled, skipped_str = Scheduler.create_schedule(tasks_with_pet, time(8, 0), TimeIncrement.HOUR)

    # Scheduled list only contains tasks that were successfully scheduled
    assert len(scheduled) == 1
    assert scheduled[0].description == "Short task"

    # Skipped tasks are reported in skipped_str
    assert "Long task" in skipped_str
    assert "09:00" in skipped_str


def test_detect_overlapping_scheduled_tasks():
    """Test 4.2: Verify overlapping tasks are handled correctly."""
    owner = Owner("Alice", start_time=time(8, 0))
    owner.add_pet("Buddy", "Dog")

    owner.add_task_for_pet("Buddy", "Task 1", 60, time(10, 0), priority=Priority.MEDIUM)
    owner.add_task_for_pet("Buddy", "Task 2", 60, time(11, 0), priority=Priority.MEDIUM)
    owner.add_task_for_pet("Buddy", "Task 3", 30, time(12, 0), priority=Priority.LOW)

    pet = owner.pets[0]
    tasks_with_pet = [(pet.name, task) for task in pet.tasks]
    scheduled, _ = Scheduler.create_schedule(tasks_with_pet, time(8, 0), TimeIncrement.HOUR)

    # Task 1 should be scheduled at 08:00
    task1 = [t for t in scheduled if t.description == "Task 1"][0]
    assert task1.scheduled_time == time(8, 0)

    # Task 2 should be scheduled at 09:00 (after task 1 which ends at 09:00)
    task2 = [t for t in scheduled if t.description == "Task 2"][0]
    assert task2.scheduled_time == time(9, 0)


def test_conflict_detection_across_multiple_pets():
    """Test 4.3: Verify conflicts are detected across multiple pets."""
    owner = Owner("Alice", start_time=time(8, 0))
    owner.add_pet("Biscuit", "Dog")
    owner.add_pet("Whiskers", "Cat")

    owner.add_task_for_pet("Biscuit", "Biscuit Task 1", 45, time(9, 0), priority=Priority.HIGH)
    owner.add_task_for_pet("Biscuit", "Biscuit Task 2", 30, time(10, 0), priority=Priority.MEDIUM)
    owner.add_task_for_pet("Whiskers", "Whiskers Task 1", 60, time(9, 30), priority=Priority.HIGH)
    owner.add_task_for_pet("Whiskers", "Whiskers Task 2", 20, time(11, 0), priority=Priority.LOW)

    scheduled, skipped_str = Scheduler.create_schedule_for_owner(owner)

    # Whiskers Task 1 (60 min, due 09:30) cannot fit and should be skipped
    whiskers_task1 = owner.pets[1].tasks[0]
    assert whiskers_task1.scheduled_time is None

    # Check skipped report mentions pet name and task
    assert "Whiskers" in skipped_str
    assert "Whiskers Task 1" in skipped_str


def test_no_conflicts_with_properly_spaced_tasks():
    """Test 4.4: Verify well-spaced tasks are all scheduled."""
    owner = Owner("Alice", start_time=time(8, 0))
    owner.add_pet("Buddy", "Dog")

    owner.add_task_for_pet("Buddy", "Task 1", 30, time(9, 0), priority=Priority.HIGH)
    owner.add_task_for_pet("Buddy", "Task 2", 30, time(10, 0), priority=Priority.MEDIUM)
    owner.add_task_for_pet("Buddy", "Task 3", 30, time(11, 0), priority=Priority.MEDIUM)
    owner.add_task_for_pet("Buddy", "Task 4", 30, time(12, 0), priority=Priority.LOW)

    pet = owner.pets[0]
    tasks_with_pet = [(pet.name, task) for task in pet.tasks]
    scheduled, skipped_str = Scheduler.create_schedule(tasks_with_pet, time(8, 0), TimeIncrement.HOUR)

    # All tasks should be scheduled
    assert all(t.scheduled_time is not None for t in scheduled)
    assert len(scheduled) == 4
    assert skipped_str == ""


def test_skipped_task_report_includes_details():
    """Test 4.5: Verify skipped task report includes all required details."""
    owner = Owner("Alice", start_time=time(8, 0))
    owner.add_pet("Buddy", "Dog")

    # 90-minute task that can't fit before 09:00 due_time
    owner.add_task_for_pet("Buddy", "Long appointment", 90, time(9, 0), priority=Priority.MEDIUM)

    pet = owner.pets[0]
    tasks_with_pet = [(pet.name, task) for task in pet.tasks]
    scheduled, skipped_str = Scheduler.create_schedule(tasks_with_pet, time(8, 0), TimeIncrement.HOUR)

    assert "Skipped due to conflicts:" in skipped_str
    assert "Buddy" in skipped_str
    assert "Long appointment" in skipped_str
    assert "09:00" in skipped_str
    assert "90 min" in skipped_str
    assert "Medium" in skipped_str
