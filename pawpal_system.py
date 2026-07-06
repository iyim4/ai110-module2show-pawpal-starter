# pawpal_system.py
"""
Pet task scheduling system for managing pet care activities.

PawPal is a task management system that helps pet owners organize and track
care activities for their pets. Owners can create pets, assign tasks to them,
and use the Scheduler to organize tasks by priority or other criteria.

Classes:
    Task: A single pet care activity with description, due_time, and other data.
    Pet: A pet with a name, species, and associated tasks.
    Owner: An owner who manages one or more pets.
    Scheduler: Utility class for organizing tasks across all pets.
    Priority: enum representing task importance
    TimeIncrement: enum representing Task scheduling blocks
    TimeFrequency: enum representing Task frequency
"""

from dataclasses import dataclass, field
from typing import List
from enum import Enum, auto
from datetime import time


class Priority(Enum):
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()


PRIORITY_STRINGS = {
    "Low": Priority.LOW,
    "Medium": Priority.MEDIUM,
    "High": Priority.HIGH,
}
REVERSE_PRIORITY = {v: k for k, v in PRIORITY_STRINGS.items()}


class TimeIncrement(Enum):
    HOUR = auto()
    QUARTER_HOUR = auto()
    HALF_HOUR = auto()


class TimeFrequency(Enum):
    DAILY = auto()
    WEEKLY = auto()


@dataclass
class Task:
    description: str
    duration: int
    due_time: time
    frequency: TimeFrequency = TimeFrequency.DAILY
    priority: Priority = Priority.LOW
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True


@dataclass
class Pet:
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(
        self,
        description: str,
        duration: int,
        due_time: time,
        frequency: TimeFrequency = TimeFrequency.DAILY,
        priority: Priority = Priority.LOW,
    ) -> None:
        """Create and add a task to this pet's task list."""
        task = Task(description, duration, due_time, frequency, priority)
        self.tasks.append(task)

    def get_str_schedule(self) -> str:
        """Return this pet's daily task schedule as a string."""
        lines = [f"#### Daily plan for {self.name} ({self.species})"]
        for task in self.tasks:
            time_str = task.due_time.strftime("%H:%M")
            priority_str = task.priority.name.lower()
            lines.append(
                f"  - {time_str} — {task.description} ({task.duration} min) [priority: {priority_str}]"
            )
        return "\n".join(lines)

    def get_str_task_list(self) -> str:
        """Return a list of tasks as a string"""
        if not self.tasks:
            return "No Tasks added yet"

        strtasks = []
        for task in self.tasks:
            pri = REVERSE_PRIORITY.get(task.priority, "Low")
            strtasks.append(
                f"{task.description} ({task.duration} mins, {pri} priority)"
            )

        return ", ".join(strtasks)


class Owner:
    def __init__(
        self,
        name: str,
        start_time: time = time(hour=8, minute=00),
        time_increment: TimeIncrement = TimeIncrement.HOUR,
    ) -> None:
        """Initialize an owner with name, start time, and time increment preferences."""
        self.name = name
        self.pets: List[Pet] = []
        self.start_time: time = start_time
        self.time_increment: TimeIncrement = time_increment

    def add_pet(self, name: str, species: str) -> tuple[bool, str]:
        """Create and add a pet to this owner's pet list. Return (success, message)."""
        # Validate inputs
        if not name or not name.strip():
            return False, "Pet name cannot be empty"
        if not species or not species.strip():
            return False, "Species cannot be empty"

        # Clean up whitespace
        name = name.strip()
        species = species.strip()

        # Your existing logic
        for pet in self.pets:
            if pet.name == name:
                pet.species = species
                return True, f"Updated {name} species to {species}"

        pet = Pet(name, species)
        self.pets.append(pet)
        return True, f"Added pet {name} ({species})"

    def remove_pet(self, name: str) -> None:
        """removes a pet, silently fails if not found"""
        self.pets = [pet for pet in self.pets if pet.name != name]

    def add_task_for_pet(
        self,
        name: str,
        description: str,
        duration: int,
        due_time: time = time(hour=23, minute=59),
        frequency: TimeFrequency = TimeFrequency.DAILY,
        priority: Priority = Priority.LOW,
    ) -> bool:
        """Add a task to the pet with the given name; return True if found, False otherwise."""
        for pet in self.pets:
            if pet.name == name:
                pet.add_task(
                    description=description,
                    duration=duration,
                    due_time=due_time,
                    frequency=frequency,
                    priority=priority,
                )
                return True
        return False

    def get_tasks_for_pet(self, name: str) -> List[Task]:
        """Return the task list for the pet with the given name, or an empty list if not found."""
        for pet in self.pets:
            if pet.name == name:
                return pet.tasks
        return []

    def get_str_schedule_for_pet(self, name: str) -> str:
        """Return the daily schedule for a specific pet by name as a string."""
        pet = None
        for p in self.pets:
            print("checking pet", p.name)
            if p.name == name:
                pet = p
                break

        if pet is None:
            return f"Pet '{name}' not found."

        return pet.get_str_schedule()

    def get_str_schedule_for_all_pets(self) -> str:
        """Return the daily schedule for all owned pets as a string."""
        if not self.pets:
            return "No pets found."
        lines = [pet.get_str_schedule() for pet in self.pets]
        return "\n".join(lines)


class Scheduler:
    def create_schedule(self, tasks: List[Task]) -> List[Task]:
        """Return tasks sorted by priority (high to low)."""
        # sort by high to low priority
        return sorted(tasks, key=lambda task: task.priority.value, reverse=True)

    def create_schedule_for_owner(self, owner: Owner) -> List[Task]:
        """Create an ordered schedule for all tasks across an owner's pets (not yet implemented)."""
        # all_tasks = []
        # for pet in owner.pets:
        #     all_tasks.extend(pet.tasks)
        # return self.create_schedule(all_tasks)

        # No, this won't work since we don't know what pet's task to do. must attach pet name to each task.

        return []
