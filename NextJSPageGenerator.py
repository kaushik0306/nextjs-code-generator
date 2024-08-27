import streamlit as st
import os
import random

# Initialize session state variables if they don't exist
if "sections" not in st.session_state:
    st.session_state.sections = []
if "section_count" not in st.session_state:
    st.session_state.section_count = 0
if "input_fields" not in st.session_state:
    st.session_state.input_fields = {}
if "clear_flag" not in st.session_state:
    st.session_state.clear_flag = False

# Function to add section to the list
def add_section():
    section_type = st.session_state.input_fields.get('section_type', None)
    section_count = st.session_state.section_count

    if section_type == "h3 (Subheading)":
        content = st.session_state.input_fields.get(f"h3_{section_count}", "")
        if content:
            st.session_state.sections.append(f'<h3 className="mb-4 text-xl font-bold text-black dark:text-white sm:text-2xl lg:text-xl xl:text-2xl">{content}</h3>')
    
    elif section_type == "h4 (Sub-subheading)":
        content = st.session_state.input_fields.get(f"h4_{section_count}", "")
        if content:
            st.session_state.sections.append(f'<h4 className="mb-2 text-lg font-bold text-black dark:text-white sm:text-xl lg:text-lg xl:text-xl">{content}</h4>')
    
    elif section_type == "Paragraph":
        content = st.session_state.input_fields.get(f"para_{section_count}", "")
        if content:
            st.session_state.sections.append(f'<p className="text-justify text-base font-medium leading-relaxed text-body-color sm:text-lg sm:leading-relaxed">{content}</p>')
    
    elif section_type == "Unordered List (Bullet points)":
        items = st.session_state.input_fields.get(f"list_{section_count}", "").split("\n")
        if items:
            items_str = "\n    ".join([f'<li><strong>{item}</strong></li>' for item in items])
            st.session_state.sections.append(f'<ul className="list-disc pl-5 mb-4 text-base font-medium leading-relaxed text-body-color sm:text-lg sm:leading-relaxed">\n    {items_str}\n</ul>')
    
    elif section_type == "Code Chunk":
        code = st.session_state.input_fields.get(f"code_{section_count}", "").replace('\\n', '\n')
        if code:
            st.session_state.sections.append('<pre className="max-w-3xl mx-auto overflow-auto p-5 border border-gray-200 rounded-lg shadow-lg bg-gray-50 font-mono text-sm">\n' + "{`" + code + "`}\n</pre>")

    st.session_state.section_count += 1
    st.session_state.clear_flag = True  # Set the clear flag to True to clear the input fields

# Function to reset input fields
def reset_inputs():
    section_count = st.session_state.section_count
    st.session_state.input_fields[f"h3_{section_count}"] = ""
    st.session_state.input_fields[f"h4_{section_count}"] = ""
    st.session_state.input_fields[f"para_{section_count}"] = ""
    st.session_state.input_fields[f"list_{section_count}"] = ""
    st.session_state.input_fields[f"code_{section_count}"] = ""
    st.session_state.clear_flag = False  # Reset the clear flag

# Streamlit interface
st.set_page_config(layout="wide")  # Use wide layout

# Create two columns
col1, col2 = st.columns([1, 1])  # Adjust the ratio if you want different column widths

# Left column: Page generator options
with col1:
    st.title("Next.js Page Generator")

    # User inputs for page details
    page_name = st.text_input("Enter the module name for the page:")
    header1 = st.text_input("Enter the header1 text:")
    header2 = st.text_input("Enter the header2 text:")

    # Content type selection
    st.session_state.input_fields['section_type'] = st.selectbox(
        "Choose the content type to add:",
        ["h3 (Subheading)", "h4 (Sub-subheading)", "Paragraph", "Unordered List (Bullet points)", "Code Chunk"],
        key="section_type"
    )

    # Clear the input fields if the clear flag is set
    if st.session_state.clear_flag:
        reset_inputs()

    # Input for content based on type
    section_type = st.session_state.input_fields['section_type']
    section_count = st.session_state.section_count
    if section_type == "h3 (Subheading)":
        st.session_state.input_fields[f"h3_{section_count}"] = st.text_input("Enter the text for h3", key=f"h3_{section_count}")
    elif section_type == "h4 (Sub-subheading)":
        st.session_state.input_fields[f"h4_{section_count}"] = st.text_input("Enter the text for h4", key=f"h4_{section_count}")
    elif section_type == "Paragraph":
        st.session_state.input_fields[f"para_{section_count}"] = st.text_area("Enter the paragraph text", key=f"para_{section_count}")
    elif section_type == "Unordered List (Bullet points)":
        st.session_state.input_fields[f"list_{section_count}"] = st.text_area("Enter bullet points (one per line)", key=f"list_{section_count}")
    elif section_type == "Code Chunk":
        st.session_state.input_fields[f"code_{section_count}"] = st.text_area("Enter the code block (use \\n for new lines)", key=f"code_{section_count}")

    # Button to add a section
    if st.button("Add Section"):
        add_section()

    # Generate the file if sections have been added
    if st.session_state.sections and st.button("Generate Page"):
        # Directory to save the generated .tsx file based on the module name
        output_dir = os.path.join("generated_pages", page_name)
        os.makedirs(output_dir, exist_ok=True)

        # Join sections together
        content_sections = "\n\n".join(st.session_state.sections)

        # Generate a random number between 2 and 10 for the banner image
        random_number = random.randint(2, 10)
        banner_image_path = f'/images/banners/Banner-{random_number}.webp'

        # Template for the page
        PAGE_TEMPLATE = f"""
"use client"
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import Banner from '@/components/Common/Banner';

const {page_name} = () => {{
    return (
        <>
        <Header/>
        <Banner backgroundimage='{banner_image_path}'
        header1="{header1}"
        header2="{header2}" />

        <div className="container mx-auto p-4">
        {content_sections}
        </div>

        <Footer/>
        </>
    );
}};

export default {page_name};
"""

        # Write the generated content to a .tsx file
        file_path = os.path.join(output_dir, "page.tsx")
        with open(file_path, "w") as file:
            file.write(PAGE_TEMPLATE)

        st.success(f"Page generated successfully at {file_path}")

# Right column: Display added sections
with col2:
    st.header("Sections Added")
    if st.session_state.sections:
        for i, section in enumerate(st.session_state.sections):
            st.markdown(f"**Section {i + 1}:** {section}", unsafe_allow_html=True)
    else:
        st.write("No sections added yet.")
