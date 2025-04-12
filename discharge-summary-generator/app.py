from groq import Groq
import os
import json
import streamlit as st
from dotenv import load_dotenv
from fpdf import FPDF

load_dotenv(".env")
api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")


# Load patient data from the JSON file
def load_patient_data(filepath="patients_data.json"):
    with open(filepath, "r") as file:
        return json.load(file)

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
    pdf.cell(200, 10, "Care Hospital", ln=True, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.cell(200, 8, "Beside Axis bank, Opp Kalyani Society, Kothrud, Pune - 411038", ln=True, align='C')
    pdf.cell(200, 8, "Ph: 094233 80390, Timing: 09:00 AM - 02:00 PM, 03:30 PM - 7:00 PM | Closed: Thursday", ln=True, align='C')

    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "DISCHARGE SUMMARY", ln=True, align='C')

    pdf.set_font("Arial", '', 11)
    pdf.ln(8)
    pdf.multi_cell(0, 8, f"""
Patient UID: {patient_data['id']}               Admission Date: {patient_data['admission_date']}
Name: {patient_data['name']} ({patient_data['gender']})       Discharge Date: {patient_data['discharge_date']}
Age: {patient_data['age']}                     Status: Discharged
Address: {patient_data.get('address', 'Not Provided')}
""")

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Summary:", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(0, 8, summary)

    filename = f"Discharge_Summary_{patient_data['id']}.pdf"
    pdf.output(filename)
    return filename

# Main Streamlit UI
st.title("Discharge Summary Generator")

# Load patient data
data = load_patient_data()

# User inputs
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
            st.success("Patient found. Generating summary...")

            # Prepare prompt
            prompt = f"""
            You are a professional medical documentation assistant. Your task is to generate a formal hospital discharge summary based solely on the following structured patient data.

            Do not include anything outside the data provided.

            Output the summary in proper paragraph format with appropriate medical tone and coherence.

            Patient Data:
            {patient_data}
            """

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
                stream=True,
                stop=None,
            )

            summary = ""
            for chunk in completion:
                content = chunk.choices[0].delta.content or ""
                summary += content

            # Display Info
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

            st.subheader("📄 Discharge Summary")
            st.text_area("Full Summary", summary, height=300)

            # Generate PDF and download
            pdf_path = generate_discharge_pdf(patient_data, summary)
            with open(pdf_path, "rb") as file:
                st.download_button("📥 Download PDF", file, file_name=pdf_path, mime="application/pdf")
