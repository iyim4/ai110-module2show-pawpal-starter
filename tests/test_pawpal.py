from pawpal_system import Pet, Task, Priority, TimeFrequency
from datetime import time


def test_task_completion():
    """Verify that calling mark_complete() changes the task's status."""
    task = Task(
        description="Feed the dog",
        duration=10,
        due_time=time(8, 0),
        frequency=TimeFrequency.DAILY,
        priority=Priority.HIGH,
    )

    # Initially, task should not be completed
    assert task.completed is False

    # After marking complete, status should change
    task.mark_complete()
    assert task.completed is True


def test_add_tasks_to_pet():
    """Verify that adding a task to a Pet increases that pet's task count."""
    pet = Pet(name="Buddy", species="Golden Retriever")

    # Initially, pet should have no tasks
    assert len(pet.tasks) == 0

    # Add first task
    pet.add_task(description="Morning walk", duration=30, due_time=time(8, 0))
    assert len(pet.tasks) == 1

    # Add second task
    pet.add_task(
        description="Feeding", duration=10, due_time=time(12, 0), priority=Priority.HIGH
    )
    assert len(pet.tasks) == 2
