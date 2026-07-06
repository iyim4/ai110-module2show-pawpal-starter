import streamlit as st
import pandas as pd
import datetime
from pawpal_system import Owner, Priority, PRIORITY_STRINGS, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

with st.expander("Scenario", expanded=True):
    st.markdown("""
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
""")

st.divider()

# owner
col1, col2 = st.columns(2)
with col1:
    owner_name = st.text_input("Your name", value="Jordan")
with col2:
    start_time = st.time_input(
        "What time do you want the schedule to start?", value=datetime.time(8, 0)
    )

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name)
owner = st.session_state.owner

# pets
st.markdown("### Pets")

# Initialize previous pets state in session
if "previous_pets_state" not in st.session_state:
    st.session_state.previous_pets_state = []

# Create dataframe from owner.pets
pet_data = [{"name": p.name, "species": p.species} for p in owner.pets]
if not pet_data:
    pet_data = [{"name": "Biscuit", "species": "Golden Retriever"}]
df_display = pd.DataFrame(pet_data).reset_index(drop=True)

# Edit with data_editor
df_edited = st.data_editor(
    df_display,
    num_rows="dynamic",
    column_config={
        "name": st.column_config.TextColumn("Pet Name"),
        "species": st.column_config.TextColumn("Species"),
    },
    hide_index=True,
    key="pets_editor",
)

# Sync dataframe back to owner.pets
col1, col2 = st.columns([0.3, 0.7])
pet_errors = []
new_pets = []
with col1:
    if st.button("Save Changes"):

        # Build new pet list from edited dataframe
        for idx, (_, row) in enumerate(df_edited.iterrows(), 1):
            name = row["name"] if isinstance(row["name"], str) else ""
            species = row["species"] if isinstance(row["species"], str) else ""

            new_pets.append({"name": name, "species": species})

        # Match by position to detect renames and updates
        for i, new_pet in enumerate(new_pets):
            if i < len(owner.pets):
                # Existing pet at this position - update in place (handles renames)
                owner.pets[i].name = new_pet["name"]
                owner.pets[i].species = new_pet["species"]
            else:
                # New pet beyond current list - backend validates
                success, message = owner.add_pet(new_pet["name"], new_pet["species"])
                if not success:
                    pet_errors.append(message)

        # Remove pets that were deleted (list is now shorter)
        while len(owner.pets) > len(new_pets):
            owner.pets.pop()

with col2:
    if owner.pets:
        st.markdown(f"#### Your Pets: {', '.join([p.name for p in owner.pets])}")
    else:
        st.text("click 'Save Changes' to add your pet(s)")

# Display errors at bottom
if pet_errors:
    st.error(f"Error saving Pet(s): {', '.join(pet_errors)}")
else:
    # Update previous state for next rerun
    st.session_state.previous_pets_state = new_pets
    # st.success("Changes saved!")


# tasks. have a section for each pet
st.markdown("### Tasks")
if not owner.pets:
    st.caption("Add a pet first.")

for pet in owner.pets:
    st.markdown(f"#### {pet.name} Tasks")

    col1, col2, col3 = st.columns(3)
    with col1:
        task_desc = st.text_input(
            "Task description", value="Morning walk", key=f"task_desc_{pet.name}"
        )
    with col2:
        duration = st.number_input(
            "Duration (minutes)",
            min_value=1,
            max_value=240,
            value=20,
            key=f"duration_{pet.name}",
        )
    with col3:
        priority = st.selectbox(
            "Priority", PRIORITY_STRINGS.keys(), index=2, key=f"priority_{pet.name}"
        )

    if st.button("Add task", key=f"add_task_{pet.name}"):
        success = st.session_state.owner.add_task_for_pet(
            pet.name, task_desc, duration, priority=PRIORITY_STRINGS[priority]
        )
        if not success:
            st.warning("error adding task!")

    if pet.tasks:
        st.write(f"Current tasks: {pet.get_str_task_list()}")
    else:
        st.info(f"No tasks for {pet.name} yet. Add one above.")

# scheduler
st.divider()

col1, col2 = st.columns(2)
with col1:
    st.subheader("Build Schedule")
with col2:
    if owner.pets:
        options = ["All Pets"] + [(f"{p.name} ({p.species})") for p in owner.pets]
        pet_name_sch = st.selectbox(
            "Get the daily schedule for:",
            options,
        )
    else:
        pet_name_sch = None

if st.button("Generate schedule"):
    if pet_name_sch:
        if pet_name_sch == "All Pets":
            schedule = owner.generate_str_schedule_for_all_pets()
        else:
            # Extract just the name (before the parenthesis)
            pet_name = pet_name_sch.split(" (")[0]
            schedule = owner.generate_str_schedule_for_pet(pet_name)
        st.markdown(schedule)
    else:
        st.error("Please add a pet first.")
