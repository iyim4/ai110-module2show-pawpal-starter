from datetime import time
from pawpal_system import Owner, Priority, Scheduler


def main():
    # Create an Owner
    alice = Owner("Alice", start_time=time(hour=8, minute=0))

    # Create and add pets to the owner
    alice.add_pet("Biscuit", "Golden Retriever")
    alice.add_pet("Whiskers", "Siamese Cat")

    # Add tasks to biscuit (first pet)
    success = alice.add_task_for_pet(
        name="Biscuit",
        description="Morning walk",
        duration=30,
        due_time=time(hour=8, minute=0),
        priority=Priority.HIGH,
    )
    assert success
    success = alice.add_task_for_pet(
        name="Biscuit",
        description="Lunch and playtime",
        duration=45,
        due_time=time(hour=12, minute=30),
        priority=Priority.MEDIUM,
    )
    assert success

    # Add tasks to Whiskers (second pet)
    success = alice.add_task_for_pet(
        name="Whiskers",
        description="Feeding",
        duration=15,
        due_time=time(hour=9, minute=0),
        priority=Priority.HIGH,
    )
    assert success
    success = alice.add_task_for_pet(
        name="Whiskers",
        description="Litter box cleaning",
        duration=10,
        due_time=time(hour=18, minute=0),
        priority=Priority.MEDIUM,
    )
    assert success

    # Add a third task to biscuit
    success = alice.add_task_for_pet(
        name="Biscuit",
        description="Evening walk",
        duration=30,
        due_time=time(hour=18, minute=30),
        priority=Priority.HIGH,
    )
    assert success

    # Print today's schedule
    print(f"\n{'='*50}")
    print(f"Today's Schedule for {alice.name}")
    print(f"{'='*50}")
    print(alice.get_str_schedule_for_all_pets())
    print(f"{'='*50}\n")

    # Create scheduler and schedule all tasks
    scheduled, skipped = Scheduler.create_schedule_for_owner(owner=alice)

    # print(f"\n{'='*50}")
    # print("Scheduled Daily Plan")
    # print(f"{'='*50}")
    # print(alice.get_str_schedule_for_all_pets())

    # if skipped:
    #     print(f"\n{skipped}")


if __name__ == "__main__":
    main()
