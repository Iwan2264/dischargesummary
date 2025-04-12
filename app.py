from groq import Groq
import os
import json
import streamlit as st
from dotenv import load_dotenv
from fpdf import FPDF
import unicodedata
from streamlit_quill import st_quill

# Set Streamlit to dark mode
st.set_page_config(page_title="Discharge Summary Generator", layout="wide", initial_sidebar_state="auto", page_icon="🩺")

# Custom CSS for dark mode Quill editor
dark_mode_css = """
<style>
/* Style the Quill editor container */
div[data-baseweb="quill"] .ql-container {
    background-color: #1e1e1e !important;
    color: #ffffff !important;
    border: 1px solid #444 !important;
}

/* Style the Quill editor text area */
div[data-baseweb="quill"] .ql-editor {
    background-color: #1e1e1e !important;
    color: #ffffff !important;
}

/* Style the Quill toolbar */
div[data-baseweb="quill"] .ql-toolbar {
    background-color: #2d2d2d !important;
    border: 1px solid #444 !important;
}

/* Style toolbar buttons */
div[data-baseweb="quill"] .ql-toolbar button {
    color: #ffffff !important;
}

/* Style toolbar button hover */
div[data-baseweb="quill"] .ql-toolbar button:hover {
    background-color: #444 !important;
}

/* Style selected text */
div[data-baseweb="quill"] .ql-editor .ql-snow .ql-picker-options {
    background-color: #2d2d2d !important;
    color: #ffffff !important;
}

/* Ensure text remains readable */
div[data-baseweb="quill"] .ql-editor p,
div[data-baseweb="quill"] .ql-editor li {
    color: #ffffff !important;
}
</style>
"""
st.markdown(dark_mode_css, unsafe_allow_html=True)

def sanitize_text(text):
    return unicodedata.normalize("NFKD", text).encode("latin-1", "ignore").decode("latin-1")

load_dotenv(".env")
api_key = os.getenv("GROQ_API_KEY")

# Load patient data from the JSON file
def load_patient_data(filepath="patients_data.json"):
    try:
        with open(filepath, "r") as file:
            return json.load(file)
    except Exception as e:
        st.error(f"Error loading patient data: {e}")
        return []

# Fetch patient by name and ID
def get_patient_by_id_and_name(patient_id, name, data):
    for patient in data:
        if patient["id"].strip() == patient_id.strip() and patient["name"].strip().lower() == name.strip().lower():
            return patient
    return None

# Generate discharge summary PDF in formatted layout
def generate_discharge_pdf(patient_data, summary):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Hospital header
    if os.path.exists("hospital_logo.png"):
        pdf.image("hospital_logo.png", x=10, y=8, w=25)

    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "S+ Care Hospital", ln=True, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.cell(200, 8, "Beside Amir Bank, Opp Mongolia Society, Newtown, Kolkata - 700135", ln=True, align='C')
    pdf.cell(200, 8, "Mobile: 70010 00000  Telephone: 90600 00000", ln=True, align='C')

    # Add horizontal line separator
    pdf.ln(10)
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())

    pdf.ln(2)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "DISCHARGE SUMMARY", ln=True, align='C')

    # Add horizontal line separator
    pdf.ln(2)
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())

    # Patient details
    pdf.set_font("Arial", '', 11)
    pdf.ln(2)

    # Left Column (Personal Info)
    left_x = pdf.get_x()
    left_y = pdf.get_y()
    pdf.multi_cell(90, 8, 
        f"Name: {patient_data['name']}\n"
        f"Age: {patient_data['age']}\n"
        f"Gender: {patient_data['gender']}\n"
        f"Address: {patient_data.get('address', 'Not Provided')}",
        border=0
    )

    # Right Column (Admission Info)
    pdf.set_xy(left_x + 100, left_y)
    pdf.multi_cell(90, 8,
        f"Patient UID: {patient_data['id']}\n"
        f"Admission Date: {patient_data['admission_date']}\n"
        f"Discharge Date: {patient_data['discharge_date']}\n"
        f"Status: Discharged",
        border=0
    )

    # Add horizontal line separator
    pdf.ln(2)
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    
    # Main Summary
    pdf.ln(2)
    pdf.set_font("Helvetica", size=11)
    pdf.multi_cell(0, 5.5, sanitize_text(summary))

    # Add horizontal line separator
    pdf.ln(5)
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())

    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 8, "Treating Consultant / Authorized Team Doctor :", ln=1)
    main_consultant_name = patient_data["primary_consultant_name"]
    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 8, f"Name: {main_consultant_name}", ln=1)
    pdf.cell(0, 8, "Signature: _________________________", ln=1)

    # Divider line
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.3)
    pdf.line(10, pdf.get_y() + 2, 200, pdf.get_y() + 2)
    pdf.ln(4)

    # Patient / Attendant Section
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 8, "Patient / Attendant :", ln=1)
    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(0, 8, "I/WE HAVE UNDERSTOOD THE INSTRUCTIONS GIVEN ABOUT THE MEDICATION DOSAGE AND DISCHARGE AFTER CARE.")
    pdf.cell(0, 8, "Name: _________________________", ln=1)
    pdf.cell(0, 8, "Signature: _________________________", ln=1)
    
    # Add bold horizontal line separator with decorative image
    pdf.ln(10)
    pdf.set_draw_color(0, 102, 153)
    pdf.set_line_width(1)
    y = pdf.get_y()
    pdf.line(10, y, 200, y)
    icon_path = "footer.png"
    icon_width = 10
    icon_height = 10
    center_x = (210 - icon_width) / 2
    if os.path.exists(icon_path):
        pdf.image(icon_path, x=center_x, y=y - (icon_height / 2), w=icon_width, h=icon_height)

    filename = f"Discharge_Summary_{patient_data['id']}.pdf"
    pdf.output(filename)
    return filename

# Streamlit App
st.title("Discharge Summary Generator")

# Initialize session state
if "summary" not in st.session_state:
    st.session_state.summary = ""
if "edited_summary" not in st.session_state:
    st.session_state.edited_summary = ""
if "patient_data" not in st.session_state:
    st.session_state.patient_data = None

data = load_patient_data()

patient_name = st.text_input("Enter Patient's Name")
patient_id = st.text_input("Enter Patient's ID")

if st.button("Generate Summary"):
    if not patient_name or not patient_id:
        st.warning("Please enter both patient name and ID.")
    else:
        patient_data = get_patient_by_id_and_name(patient_id, patient_name, data)

        if not patient_data:
            st.error("Patient not found.")
        else:
            st.session_state.patient_data = patient_data
            st.success("Patient found. Generating summary...")
            # Prepare prompt
            prompt = f"""
            Given the following patient hospital data, generate a discharge summary. Follow the structure below strictly and make sure the output is clean, readable, and suitable for PDF printing using FPDF (avoid special symbols, markdown or formatting that would break in plain text):
            CONSULTANTS INVOLVED:
            Primary Consultant:
            <primary_consultant_name>, <speciality>
            Other Consultants:
            <consultant_1_name> (<speciality>)
            <consultant_2_name> (<speciality>)
            ... (if any)
            DIAGNOSIS:
            Provisional Diagnosis: <provisional_diagnosis>  
            Final Diagnosis: <final_diagnosis>
            KEY FINDINGS AND CLINICAL COURSE:
            <clinical_course_description>  
            Mention presenting symptoms, relevant test results, clinical progression, any support provided, and response to treatment.
            INVESTIGATIONS AND TREATMENT:
            * <Test 1>
            * <Test 2>
            * <Medication with dosage and route>
            * <Other treatments: physiotherapy, oxygen, etc.>
            CLINICAL NOTES:
            * <Any observations: vitals, mobility, diet, compliance, etc.>
            SUMMARY:
            Provide a very detailed clinical summary of the admission, highlighting diagnosis, major treatments, progression, and condition at discharge in this section. For example: During his hospitalization, Mr. Mondal received antibiotic therapy for the treatment of pneumonia. Diagnostic
            studies included a Chest X-Ray and Blood Test, which showed improvement as evident from the Chest
            X-Ray report. Laboratory results revealed a normal Complete Blood Count (CBC).
            The patient responded well to treatment, and no complications were observed throughout his stay. On the
            day of discharge, his vital signs were stable, with a blood pressure of 120/80 mmHg, pulse rate of 76 beats
            per minute, and a temperature of 98.6°F.
            Medications prescribed at discharge include Azithromycin and Paracetamol.
            In conclusion, Mr. Mondal has demonstrated significant improvement and is being discharged in a stable
            condition.
            CONDITION AT DISCHARGE:
            <Stable / Unstable / Deceased>
            PRESCRIPTION ON DISCHARGE:
            1. <Medication> – <Dosage & Timing>
            2. <Medication> – <Dosage & Timing>
            3. ...
            ADVICE:
            * <Advice 1>
            * <Advice 2>
            * ...
            EMERGENCY INSTRUCTIONS:
            In case of <symptom1>, <symptom2>, or <symptom3>, report to the emergency department immediately.
            FOLLOW-UP:
            <Department> on <Follow-up Date>
            Now generate the summary based on this sample data Patient Data (in JSON format):
            {json.dumps(patient_data, indent=2)}
            """

            try:
                client = Groq()
                completion = client.chat.completions.create(
                    model="llama3-70b-8192",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=1,
                    max_tokens=1024,
                    top_p=1,
                    stream=False,
                    stop=None,
                )
                st.session_state.summary = completion.choices[0].message.content
                st.session_state.edited_summary = st.session_state.summary  # Initialize edited summary
            except Exception as e:
                st.error(f"Error generating summary: {e}")
                st.session_state.summary = ""
                st.session_state.edited_summary = ""

# Display patient info if available
if st.session_state.patient_data:
    patient_data = st.session_state.patient_data
    patient_info = f"""
- **Name:** {patient_data['name']}
- **Patient ID:** {patient_data['id']}
- **Age:** {patient_data['age']}
- **Gender:** {patient_data['gender']}
- **Admission Date:** {patient_data['admission_date']}
- **Discharge Date:** {patient_data['discharge_date']}
"""
    st.markdown("### 🧾 Patient Information")
    st.markdown(patient_info)

# Display and edit summary with Quill
if st.session_state.summary:
    st.subheader("📄 Discharge Summary")
    st.session_state.edited_summary = st_quill(
        value=st.session_state.edited_summary,
        toolbar=["bold", "italic", "underline", "bullet", "list", "align"],
        html=False,  # Plain text for PDF compatibility
        key="quill_editor"
    )

    # Generate and show download button whenever edited_summary exists
    if st.session_state.edited_summary and st.session_state.patient_data:
        try:
            pdf_path = generate_discharge_pdf(st.session_state.patient_data, st.session_state.edited_summary)
            with open(pdf_path, "rb") as file:
                st.download_button(
                    "📥 Download PDF", 
                    file, 
                    file_name=pdf_path, 
                    mime="application/pdf",
                    key="download_pdf"
                )
        except Exception as e:
            st.error(f"Error generating PDF: {e}")
