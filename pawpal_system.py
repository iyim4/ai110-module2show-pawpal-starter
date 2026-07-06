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
from typing import List, Optional, Tuple
from enum import Enum, auto
from datetime import time, timedelta, datetime


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
    HALF_HOUR = auto()
    QUARTER_HOUR = auto()


TIME_INCREMENT_STRINGS = {
    "Hourly": TimeIncrement.HOUR,
    "Half Hourly": TimeIncrement.HALF_HOUR,
    "Quarter Hourly": TimeIncrement.QUARTER_HOUR,
}
REVERSE_TIME_INCREMENT = {v: k for k, v in TIME_INCREMENT_STRINGS.items()}


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
    scheduled_time: Optional[time] = None

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
            time_str = (
                task.scheduled_time.strftime("%H:%M")
                if task.scheduled_time
                else "unscheduled"
            )
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

    def generate_str_schedule_for_pet(self, name: str) -> str:
        """Generate and return the daily schedule for a specific pet by name."""
        pet = None
        for p in self.pets:
            if p.name == name:
                pet = p
                break

        if pet is None:
            return f"Pet '{name}' not found."

        scheduler = Scheduler()
        tasks_with_pet = [(pet.name, task) for task in pet.tasks]
        scheduled, skipped = scheduler.create_schedule(
            tasks_with_pet, self.start_time, self.time_increment
        )

        lines = [f"#### Daily plan for {pet.name} ({pet.species})"]
        for task in scheduled:
            time_str = (
                task.scheduled_time.strftime("%H:%M")
                if task.scheduled_time
                else "unscheduled"
            )
            priority_str = task.priority.name.lower()
            lines.append(
                f"  - {time_str} — {task.description} ({task.duration} min) [priority: {priority_str}]"
            )

        output = "\n".join(lines)
        if skipped:
            output += f"\n\n{skipped}"
        return output

    def generate_str_schedule_for_all_pets(self) -> str:
        """Generate and return the daily schedule for all pets."""
        if not self.pets:
            return "No pets found."

        scheduler = Scheduler()
        scheduled, skipped = scheduler.create_schedule_for_owner(self)

        output = []
        for pet in self.pets:
            pet_tasks = [task for task in scheduled if task in pet.tasks]
            lines = [f"#### Daily plan for {pet.name} ({pet.species})"]
            for task in pet_tasks:
                time_str = (
                    task.scheduled_time.strftime("%H:%M")
                    if task.scheduled_time
                    else "unscheduled"
                )
                priority_str = task.priority.name.lower()
                lines.append(
                    f"  - {time_str} — {task.description} ({task.duration} min) [priority: {priority_str}]"
                )
            output.append("\n".join(lines))

        result = "\n\n".join(output)
        if skipped:
            result += f"\n\n{skipped}"
        return result

    def get_str_schedule_for_all_pets(self) -> str:
        """Return the daily schedule for all owned pets as a string."""
        if not self.pets:
            return "No pets found."
        lines = [pet.get_str_schedule() for pet in self.pets]
        return "\n".join(lines)


class Scheduler:
    @staticmethod
    def _add_time_minutes(base_time: time, minutes: int) -> time:
        """Add minutes to a time object and return the result."""
        combined = datetime.combine(datetime.today(), base_time)
        result = combined + timedelta(minutes=minutes)
        return result.time()

    @staticmethod
    def _round_up_to_increment(base_time: time, increment: TimeIncrement) -> time:
        """Round up a time to the next increment boundary."""
        increment_minutes = {
            TimeIncrement.QUARTER_HOUR: 15,
            TimeIncrement.HALF_HOUR: 30,
            TimeIncrement.HOUR: 60,
        }
        minutes = increment_minutes[increment]
        total_minutes = base_time.hour * 60 + base_time.minute
        if total_minutes % minutes == 0:
            return base_time
        next_slot = ((total_minutes // minutes) + 1) * minutes
        hours = next_slot // 60
        mins = next_slot % 60
        return time(hour=hours, minute=mins)

    @staticmethod
    def _format_skipped_tasks(skipped: List[Tuple[str, Task]]) -> str:
        """Return a formatted string of skipped tasks with pet names."""
        if not skipped:
            return ""
        lines = ["Skipped due to conflicts:"]
        for pet_name, task in skipped:
            due_str = task.due_time.strftime("%H:%M")
            priority_str = task.priority.name.capitalize()
            lines.append(
                f"  - {pet_name}: {task.description} (due: {due_str}, duration: {task.duration} min, priority {priority_str})"
            )
        return "\n".join(lines)

    @staticmethod
    def create_schedule(
        tasks_with_pet: List[Tuple[str, Task]],
        start_time: time,
        interval: TimeIncrement,
    ) -> Tuple[List[Task], str]:
        """
        Schedule tasks by priority (primary) and due_time (secondary).
        Assigns scheduled_time to each task, skipping those that can't fit before due_time.
        Args:
            tasks_with_pet: List of (pet_name, task) tuples
        Returns (scheduled_tasks, skipped_summary_string).
        """
        # Sort by priority (high to low) first, then by due_time (earliest first) as tiebreaker
        sorted_tasks = sorted(
            tasks_with_pet, key=lambda x: (-x[1].priority.value, x[1].due_time)
        )

        current_slot_time = start_time
        scheduled = []
        skipped = []

        for pet_name, task in sorted_tasks:
            # Calculate when task would end if scheduled at current slot
            end_time = Scheduler._add_time_minutes(current_slot_time, task.duration)

            # Check if task fits before its due_time
            if end_time > task.due_time:
                skipped.append((pet_name, task))
            else:
                task.scheduled_time = current_slot_time
                scheduled.append(task)
                # Move to next slot, rounding up to the increment boundary
                current_slot_time = Scheduler._round_up_to_increment(end_time, interval)

        skipped_str = Scheduler._format_skipped_tasks(skipped)
        return scheduled, skipped_str

    @staticmethod
    def create_schedule_for_owner(owner: Owner) -> Tuple[List[Task], str]:
        """Create an ordered schedule for all tasks across an owner's pets."""
        all_tasks_with_pet = []
        for pet in owner.pets:
            for task in pet.tasks:
                all_tasks_with_pet.append((pet.name, task))
        return Scheduler.create_schedule(
            all_tasks_with_pet, owner.start_time, owner.time_increment
        )
