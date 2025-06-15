import streamlit as st
import re

# ────────────────────────────────────────────────────────────── #
# Helper – derive title from uploaded filename
# Example "Unda_01_A3.jpg" → "Unda 01"
# Make sure your upload widget sets:
#     st.session_state.uploaded_file_name = uploaded_file.name
# before calling description_form().
# ────────────────────────────────────────────────────────────── #
def _derive_title(filename: str) -> str:
    stem = filename.split(".")[0]                 # drop extension
    word_num = "_".join(stem.split("_")[:2])      # keep word + number
    return re.sub(r"_", " ", word_num).strip().title()


# ────────────────────────────────────────────────────────────── #
# Form: collects (or auto-generates) metadata for the print
# ────────────────────────────────────────────────────────────── #
def description_form() -> bool:
    """
    Renders the lean metadata form per new business rules.
    Returns True when user clicks “Generate Description”.
    """
    with st.form(key="print_details_form"):
        st.markdown("### Print Metadata")

        # 1 · Title derived from filename
        filename = st.session_state.get("uploaded_file_name", "Untitled_01.jpg")
        title = _derive_title(filename)
        st.session_state.print_title = title
        st.text_input("Print Title", value=title, disabled=True)

        # 2 · Hard-coded attributes
        st.session_state.artist_name = "Anna Ciok"
        st.text_input("Artist Name", value="Anna Ciok", disabled=True)

        st.session_state.art_style = "Watercolor"
        st.text_input("Art Style", value="Watercolor", disabled=True)

        st.session_state.medium = "paper"
        st.text_input("Print Medium", value="paper", disabled=True)

        st.session_state.dimensions = "multiple sizes available"
        st.text_input("Dimensions", value="multiple sizes available", disabled=True)

        st.session_state.year_created = "2025"
        st.text_input("Year Created", value="2025", disabled=True)

        # 3 · Tone selector
        tone = st.radio(
            "Description Tone",
            options=["SEO", "Shopify Product Page"],
            index=1,
            horizontal=True,
        )
        st.session_state.description_tone = tone

        # 4 · Conditional SEO keywords
        if tone == "SEO":
            st.session_state.keywords = st.text_input(
                "SEO Keywords (comma-separated)",
                value=st.session_state.get("keywords", ""),
                placeholder="e.g., abstract art, watercolor print, blue wall decor",
            )
        else:
            st.session_state.keywords = ""  # ignored downstream

        # 5 · Submit
        submitted = st.form_submit_button("Generate Description")
        return submitted


# ────────────────────────────────────────────────────────────── #
# Preview: show & optionally edit the generated description
# ────────────────────────────────────────────────────────────── #
def description_preview() -> None:
    """
    Displays the generated description with edit / copy / download controls.
    """
    if st.session_state.get("current_description"):
        with st.container():
            st.markdown("##### Generated Description")

            edited = st.text_area(
                "Edit Description",
                value=st.session_state.current_description,
                height=300,
                label_visibility="collapsed",
            )
            # save edits
            if edited != st.session_state.current_description:
                st.session_state.current_description = edited

            col1, col2 = st.columns(2)

            with col1:
                if st.button("Copy to Clipboard"):
                    st.code(st.session_state.current_description)
                    st.success("Copied! Use Ctrl+C / Cmd+C")

            with col2:
                st.download_button(
                    label="Download as Text",
                    data=st.session_state.current_description,
                    file_name=f"{st.session_state.print_title.replace(' ', '_').lower()}_description.txt",
                    mime="text/plain",
                )

            with st.expander("How to use in Shopify"):
                st.markdown(
                    "1. Copy the description\n"
                    "2. In Shopify admin, open Products → Add/Edit\n"
                    "3. Paste into the **Description** field\n"
                    "4. Save"
                )
    else:
        st.info("Upload an image and submit the form — your description will appear here.")
        st.session_state.current_description = ""
