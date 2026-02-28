"""Learning path view component."""

from __future__ import annotations

from typing import Dict

import streamlit as st
from ui.design_system import section_header, spacing


def render_learning_path():
    """Render goal-focused learning paths generated from repository analysis."""
    st.markdown("# Learning Paths")
    section_header(
        "Goal-Focused Path",
        "Structured steps derived from your analyzed repository and learning intent",
    )

    session_manager = st.session_state.get("session_manager")
    progress_tracker = st.session_state.get("progress_tracker")

    if not session_manager:
        st.warning("Session is not initialized. Reload the app.")
        return

    artifacts = session_manager.get_learning_artifacts() or {}
    generated_paths = artifacts.get("learning_paths", []) or []

    if not generated_paths:
        st.info("No generated learning path yet. Run repository analysis to create one.")
        if st.button("Go to Upload & Analysis", type="primary", use_container_width=True):
            st.session_state.current_page = "Upload Code"
            st.rerun()
        return

    _render_generated_paths(generated_paths, progress_tracker)


def _render_generated_paths(paths, progress_tracker) -> None:
    path_options = {path.title: path for path in paths}
    selected_name = st.selectbox("Select Path", options=list(path_options.keys()))
    path = path_options[selected_name]

    if "generated_path_progress" not in st.session_state:
        st.session_state.generated_path_progress = {}
    if path.path_id not in st.session_state.generated_path_progress:
        st.session_state.generated_path_progress[path.path_id] = {}

    progress_map: Dict[str, bool] = st.session_state.generated_path_progress[path.path_id]
    completed_steps = [step for step in path.steps if progress_map.get(step.step_id, False)]
    total_steps = len(path.steps)
    completion_ratio = (len(completed_steps) / total_steps) if total_steps else 0.0

    st.subheader(path.title)
    st.write(path.description)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Steps", total_steps)
    with col2:
        st.metric("Completed", len(completed_steps))
    with col3:
        st.metric("Remaining", max(0, total_steps - len(completed_steps)))
    with col4:
        st.metric("Est. Time", f"{path.estimated_total_time_minutes} min")

    st.progress(completion_ratio, text=f"{int(completion_ratio * 100)}% complete")

    next_step = _find_next_available_step(path, progress_map)
    if next_step:
        st.info(f"Next recommended step: **{next_step.step_number}. {next_step.title}**")
    elif total_steps:
        st.success("All steps completed in this learning path.")

    spacing("md")
    st.markdown("### Path Steps")

    for step in path.steps:
        is_completed = progress_map.get(step.step_id, False)
        prerequisites_met = all(progress_map.get(req, False) for req in step.prerequisites)

        if is_completed:
            status = "✅ Completed"
        elif prerequisites_met:
            status = "📘 Ready"
        else:
            status = "🔒 Locked"

        with st.expander(f"{status} - Step {step.step_number}: {step.title}", expanded=False):
            st.write(step.description)
            st.caption(f"Estimated time: {step.estimated_time_minutes} min")

            if step.concepts_covered:
                st.caption(f"Concepts: {', '.join(step.concepts_covered)}")

            if step.recommended_files:
                st.caption("Recommended files:")
                for file_path in step.recommended_files:
                    st.write(f"- `{file_path}`")

            if step.prerequisites:
                prereq_labels = ", ".join(step.prerequisites)
                st.caption(f"Prerequisites: {prereq_labels}")

            if is_completed:
                st.success("Step completed.")
            elif not prerequisites_met:
                st.warning("Complete prerequisites first.")
            else:
                if st.button("Mark Step Complete", key=f"complete_path_step_{path.path_id}_{step.step_id}", use_container_width=True):
                    progress_map[step.step_id] = True
                    if progress_tracker:
                        progress_tracker.record_activity(
                            "topic_completed",
                            {
                                "path": path.title,
                                "topic": step.title,
                                "topic_name": step.title,
                                "topic_id": f"{path.path_id}:{step.step_id}",
                                "skill": path.path_id,
                                "minutes_spent": step.estimated_time_minutes,
                            },
                        )
                    st.success("Step marked complete.")
                    st.rerun()

    spacing("sm")
    if st.button("Reset Path Progress", use_container_width=True):
        st.session_state.generated_path_progress[path.path_id] = {}
        st.rerun()


def _find_next_available_step(path, progress_map):
    for step in path.steps:
        if progress_map.get(step.step_id, False):
            continue
        if all(progress_map.get(req, False) for req in step.prerequisites):
            return step
    return None
