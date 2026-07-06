# PawPal+ Project Reflection

## 1. System Design

The three main tasks a user should be able to do is:
- add a pet they own
- schedule a task related to that pet
- view the full schedule of tasks for that pet or all the pets 

**a. Initial design**

- UML Design: The Owner contains many pets, and each pet contains a list of tasks. The scheduler can create a schedule given a list of tasks, and merge schedules for all the pets of one owner.
- owner, pet, and task contain data. scheduler is stateless
- scheduler combines pet schedules given an owner's preferences
- Classes:
    - Task: A single pet care activity with a name, description, and duration.
    - Pet: A pet with a name, breed, and associated tasks.
    - Owner: An owner who manages one or more pets.
    - Scheduler: Utility class for organizing tasks across all pets.

**b. Design changes**

- After reviewing the rubic, I added due_time to the Task class and moved time-related scheduling responsibilities from Owner to Scheduler. 
- I also added three utility enum classes to communicate timing-related settings
    - Priority: enum representing task importance
    - TimeIncrement: enum representing Task scheduling blocks
    - TimeFrequency: enum representing Task frequency

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- My scheduler considers the constraints for priority and due_time (by when the task should be completed), using priority as a tie breaker. I thought that priority was more important.

**b. Tradeoffs**

- One tradeoff is that during merging pet schedules, tasks with conflicting times may have a task removed from the schedule. It is explained at the end of the schedule, and up to the owner's discretion to organize it themselves. Additionally, if they want to add more tasks, there is the flexibility of changing the task frequency increment to quarter hour, which gives less buffer time but tighter scheduling

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
