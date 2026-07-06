import streamlit as st
from pawpal_system import Owner, Priority, PRIORITY_STRINGS

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown("""
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
""")

with st.expander("Scenario", expanded=True):
    st.markdown("""
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
""")

with st.expander("What you need to build", expanded=True):
    st.markdown("""
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
""")

st.divider()

# create owner

st.subheader("Quick Demo Inputs (UI only)")
# pet_name = st.text_input("Pet name", value="Mochi")
# species = st.selectbox("Species", ["dog", "cat", "other"])

# owner
owner_name = st.text_input("Your name", value="Jordan")
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name)
owner = st.session_state.owner

# pets
col1, col2 = st.columns(2)
with col1:
    pet_name = st.text_input("Pet Name", value="Biscuit")
with col2:
    species = st.text_input("Species", value="Golden Retriever")
if st.button("Add pet"):
    st.session_state.owner.add_pet(pet_name, species)

if owner.pets:
    st.write("Current pets:", owner.pets)
    # st.table(pet.tasks)
else:
    st.info("No pets yet. Add one above.")


# tasks. have a section for each pet
st.markdown("### Tasks")
st.caption(f"Add a few tasks for {','.join([p.name for p in owner.pets])}")
owner = st.session_state.owner
for pet in owner.pets:
    st.markdown(f"#### {pet.name} Tasks")

    col1, col2, col3 = st.columns(3)
    with col1:
        task_desc = st.text_input("Task description", value="Morning walk")
    with col2:
        duration = st.number_input(
            "Duration (minutes)", min_value=1, max_value=240, value=20
        )
    with col3:
        priority = st.selectbox("Priority", PRIORITY_STRINGS.keys(), index=2)

    if st.button("Add task"):
        success = st.session_state.owner.add_task_for_pet(
            pet.name, task_desc, duration, priority=PRIORITY_STRINGS[priority]
        )
        if not success:
            st.warning("error adding task!")

    if pet.tasks:
        st.write("Current tasks:", pet.tasks)
        # st.table(pet.tasks)
    else:
        st.info(f"No tasks for {pet.name} yet. Add one above.")

# scheduler
st.divider()

st.subheader("Build Schedule")
# col1, col2 = st.columns(2)
# with col1:
#     st.caption("Get the daily schedule for")
# with col2:
pet_name = st.selectbox("Get the daily schedule for pet", [p.name for p in owner.pets])


if st.button("Generate schedule"):
    owner.print_schedule_for_pet(pet_name)
    #     st.warning(
    #         "Not implemented yet. Next step: create your scheduling logic (classes/functions) and call it here."
    #     )
    #     st.markdown("""
    # Suggested approach:
    # 1. Design your UML (draft).
    # 2. Create class stubs (no logic).
    # 3. Implement scheduling behavior.
    # 4. Connect your scheduler here and display results.
    # """)
