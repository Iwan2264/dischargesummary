# 🏥 Discharge Summary Generator – AI-Powered (Prototype)

This is a **work-in-progress AI-powered Discharge Summary Generator** intended for future use **within hospital environments**.  
It’s designed to connect to a hospital’s internal system and fetch structured patient data — such as diagnosis, vitals, medications, and procedures — to generate professional discharge summaries using AI.

> ⚙️ Currently under development and **not yet connected to any real hospital database**.

---

## 🚧 Not a Public Medical Tool

> ⚠️ **Important Notice:**  
> This tool is **not meant for public or clinical use at this stage**.  
> It's a prototype created for **testing, demo, and research purposes only**.

In production, it is meant to be accessed by **authorized medical staff** using a patient's **name and unique hospital ID**.

---

## 🧪 Try It Out – Test Patients

To let users explore how the app works, a **demo mode** is enabled using mock patient data.  
Feel free to try it with the following sample entries:

| Name               | Patient ID |
|--------------------|------------|
| Safwan Mondal      | 0001       |

---

## ⚙️ Key Features (Planned & Functional)

- 🔐 **Patient Verification** using Name + ID  
- 🤖 **AI-Powered Summary Generation** using LLM (Groq API)  
- 🗃️ **Structured Data Input** *(simulated for now)*  
- 📝 **Editable Summaries** before finalization  
- 📄 **PDF Export** for the generated reports  
- 🌐 **Live Deployment on Streamlit Cloud**

---

## 🚀 Launch the App
<a href="https://amir9117-discharge-summary-generator-app-efjwsy.streamlit.app/" target="_blank">Try the Discharge Summary Generator</a>


---

## 🛠️ Tech Stack

- **Python 3.12**
- **Streamlit** (UI + Hosting)
- **Groq API** (Language Model Backend)
- **`.env` / `st.secrets`** for secure API key management
- **Git + GitHub** for development and version control

---

## 🔒 Security

Sensitive credentials like API keys are handled securely using environment variables during local development and `st.secrets` on Streamlit Cloud.

---

[GitHub](https://github.com/amir9117) • [LinkedIn](https://www.linkedin.com/in/amirsohel1)
