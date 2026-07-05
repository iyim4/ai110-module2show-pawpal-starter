# pawpal_system.py
"""
Pet task scheduling system for managing pet care activities.

PawPal is a task management system that helps pet owners organize and track
care activities for their pets. Owners can create pets, assign tasks to them,
and use the Scheduler to organize tasks by priority or other criteria.

Classes:
    Task: A single pet care activity with a name, description, and duration.
    Pet: A pet with a name, breed, and associated tasks.
    Owner: An owner who manages one or more pets.
    Scheduler: Utility class for organizing tasks across all pets.
"""

from dataclasses import dataclass, field
from typing import List
from enum import Enum, auto
from datetime import time


class Priority(Enum):
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()


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
        pass


@dataclass
class Pet:
    name: str
    breed: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(
        self,
        description: str,
        duration: int,
        due_time: time,
        frequency: TimeFrequency = TimeFrequency.DAILY,
        priority: Priority = Priority.LOW,
    ) -> None:
        pass

    def print_schedule(self) -> None:
        pass


class Owner:
    def __init__(
        self,
        name: str,
        start_time: time = time(hour=8, minute=00),
        time_increment: TimeIncrement = TimeIncrement.HOUR,
    ) -> None:
        self.name = name
        self.pets: List[Pet] = []
        self.start_time: time = start_time
        self.time_increment: TimeIncrement = time_increment

    def add_pet(self, name: str, breed: str) -> None:
        pass

    def get_tasks_for_pet(self, name: str) -> List[Task]:
        return []

    def print_schedule_for_pet(self, name: str) -> None:
        pass

    def print_schedule_for_all_pets(self) -> None:
        pass


class Scheduler:
    def create_schedule(self, tasks: List[Task]) -> List[Task]:
        return []

    def create_schedule_for_owner(self, owner: Owner) -> List[Task]:
        return []
