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
    - Recurrence: enum representing Task recurrence frequency

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- My scheduler considers the constraints for priority and due_time (by when the task should be completed), using priority as a tie breaker. I thought that priority was more important.

**b. Tradeoffs**

- One tradeoff is that during merging pet schedules, tasks with conflicting times may have a task removed from the schedule. It is explained at the end of the schedule, and up to the owner's discretion to organize it themselves. Additionally, if they want to add more tasks, there is the flexibility of changing the task frequency increment to quarter hour, which gives less buffer time but tighter scheduling

---

## 3. AI Collaboration

**a. How you used AI**

- I used Claude AI extensively during this project to brainstorm designs, debug, and refactor. It was very helpful in automating code skeletons and creating rough drafts.
- Good results came from prompts that included more information with the goal of what I expect and instructions on what to modify. I tried giving the AI a 'role', a strategy covered in class recently. I did not see a noticable positive nor negative impact.

**b. Judgment and verification**

- For system design, AI can create a rough outline, but I believe a human should finalize the design. I tried to use AI more than last project, but it went "off the rails" and was overly vague, since it could not keep track of all the requirements. Not to mention, the requirements were split into three files, and did not align with each other.
- I experienced frustration due using a mostly AI generated design for this project, and will not be using AI to this extent for system design for the foreseeable future. The design was disorganized and not easily modifiable/scalable.

---

## 4. Testing and Verification

**a. What you tested**

- I tested the basics of adding a pet and task, then the main features of Priority-Based Task Scheduling, Conflict Detection & Smart Skipping, Interactive Multi-Pet Dashboard
- Tests are important to ensure the system runs as intended. The code is only as good as the tests.

**b. Confidence**

- I am 4.5/5 confident the scheduler works correctly. I did not have time to thoroughly read all the tests.
- With more time, I would like to test edgecases involving 3+ pets and out-of-order tasks with mixed completion.

---

## 5. Reflection

**a. What went well**

- I am most satisfied with the clean streamlit interface and logic branches

**b. What you would improve**

- I would first clarify project goals, then use the clearer focus to completely redesign the system to cater to those goals. The project requirements were vague, and felt like it guided students to a more programmatic over OO design.

**c. Key takeaway**

- The most important takeaway I learned on this project was to not trust AI with full project designs. Following instructions to use AI for system design resulting in a glaringly awful and tightly-coupled design. AI will not replace system design any time soon. Clear system goals are just as important - AI becomes overly detail-focused and cannot create clear, cohesive goals across multiple files.
- tl;dr AI sucks at system design right now. I'm glad I had the no-impact opportunity to experiement with AI, but perhaps I'll try again in 10 years.
