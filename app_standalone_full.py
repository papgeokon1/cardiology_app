import streamlit as st
import requests
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# --- DATABASE SETUP ---
DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- MODELS ---
class Patient(Base):
    __tablename__ = "patients"
    patient_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    age = Column(Integer)
    medical_history = Column(String)

class MedicalHistory(Base):
    __tablename__ = "medical_history"
    history_id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.patient_id"))
    gender = Column(String)
    hypertension = Column(Boolean)
    smoking = Column(Boolean)
    diabetes = Column(String)
    hereditary = Column(Boolean)
    BMI = Column(Float)
    atrial_fibrillation = Column(Boolean)

class Lesion(Base):
    __tablename__ = "lesions"
    lesion_id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.patient_id"))
    LAD = Column(Boolean)
    LCX = Column(Boolean)
    RCA = Column(Boolean)

class Vessel(Base):
    __tablename__ = "vessels"
    vessel_id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.patient_id"))
    num_vessels = Column(Integer)
    angioplasty = Column(Boolean)
    imaging = Column(String)

class PCI(Base):
    __tablename__ = "pci"
    pci_id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.patient_id"))
    balloon = Column(Boolean)
    IVL = Column(Boolean)
    ROTA = Column(Boolean)

Base.metadata.create_all(bind=engine)
API_URL = "http://127.0.0.1:8000"
# --- STREAMLIT APP ---
st.title("🫀 Cardiology Database Web App")

# Επιλογή λειτουργίας
option = st.sidebar.selectbox(
    "Επιλέξτε λειτουργία",
    (
        "Προσθήκη Ασθενή",
        "Λίστα Ασθενών",
        "Προσθήκη Ιατρικού Ιστορικού",
        "Λίστα Ιατρικών Ιστορικών",
        "Προσθήκη Βλαβών Αγγείων",
        "Προβολή Βλαβών",
        "Προσθήκη Αγγείων",
        "Προβολή Αγγείων",
        "Προσθήκη PCI",
        "Προβολή PCI",
        "Διαγραφή Ασθενή",
        "Προβολή Όλων των Ασθενών (Πλήρη Δεδομένα)",
        "Αναζήτηση Ασθενών με Κριτήρια"
    )
)

### 📌 Προσθήκη Ασθενούς
if option == "Προσθήκη Ασθενή":
    st.header("➕ Προσθήκη Νέου Ασθενή")
    first_name = st.text_input("Όνομα")
    last_name = st.text_input("Επώνυμο")
    age = st.number_input("Ηλικία", min_value=1, max_value=120, step=1)
    medical_history = st.text_area("Ιατρικό Ιστορικό")
    if st.button("📝 Καταχώρηση"):
        data = {"first_name": first_name, "last_name": last_name, "age": age, "medical_history": medical_history}
        response = requests.post(f"{API_URL}/patients/", json=data)
        if response.status_code == 200:
            st.success("✅ Ο ασθενής προστέθηκε με επιτυχία!")
        else:
            st.error("❌ Κάτι πήγε στραβά!")

### 📌 Λίστα Ασθενών
elif option == "Λίστα Ασθενών":
    st.header("📜 Λίστα Ασθενών")
    response = requests.get(f"{API_URL}/patients/")
    if response.status_code == 200:
        patients = response.json()
        for patient in patients:
            st.write(f"🆔 {patient['patient_id']} - {patient['first_name']} {patient['last_name']}, {patient['age']} ετών")
    else:
        st.error("❌ Δεν βρέθηκαν ασθενείς.")

### 📌 Προσθήκη Ιατρικού Ιστορικού
elif option == "Προσθήκη Ιατρικού Ιστορικού":
    st.header("➕ Προσθήκη Ιατρικού Ιστορικού")
    patient_id = st.number_input("ID Ασθενή", min_value=1, step=1)
    hypertension = st.checkbox("Υπέρταση")
    smoking = st.checkbox("Κάπνισμα")
    diabetes = st.selectbox("Διαβήτης", ["None", "Type 1", "Type 2"])
    hereditary = st.checkbox("Κληρονομικό Ιστορικό")
    gender = st.radio("Φύλο", ["Male", "Female"])
    BMI = st.number_input("BMI", min_value=10.0, max_value=50.0, step=0.1)
    atrial_fibrillation = st.checkbox("Κολπική Μαρμαρυγή")
    if st.button("📝 Καταχώρηση"):
        data = {"patient_id": patient_id, "hypertension": hypertension, "smoking": smoking,
                "diabetes": diabetes, "hereditary": hereditary, "gender": gender, "BMI": BMI,
                "atrial_fibrillation": atrial_fibrillation}
        response = requests.post(f"{API_URL}/medical_history/", json=data)
        if response.status_code == 200:
            st.success("✅ Ιατρικό Ιστορικό προστέθηκε με επιτυχία!")
        else:
            st.error("❌ Κάτι πήγε στραβά!")

### 📌 Λίστα Ιατρικών Ιστορικών
elif option == "Λίστα Ιατρικών Ιστορικών":
    st.header("📜 Λίστα Ιατρικών Ιστορικών")
    patient_id = st.number_input("ID Ασθενή για Αναζήτηση", min_value=1, step=1)
    if st.button("🔍 Αναζήτηση"):
        response = requests.get(f"{API_URL}/medical_history/{patient_id}")
        if response.status_code == 200:
            st.json(response.json())
        else:
            st.error("❌ Δεν βρέθηκε ιατρικό ιστορικό για τον ασθενή.")

### 📌 Προσθήκη Βλαβών Αγγείων
elif option == "Προσθήκη Βλαβών Αγγείων":
    st.header("➕ Προσθήκη Βλαβών Αγγείων")
    patient_id = st.number_input("ID Ασθενή", min_value=1, step=1)
    LAD = st.checkbox("LAD")
    LCX = st.checkbox("LCX")
    RCA = st.checkbox("RCA")
    if st.button("📝 Καταχώρηση"):
        data = {"patient_id": patient_id, "LAD": LAD, "LCX": LCX, "RCA": RCA}
        response = requests.post(f"{API_URL}/lesions/", json=data)
        if response.status_code == 200:
            st.success("✅ Οι βλάβες προστέθηκαν με επιτυχία!")
        else:
            st.error("❌ Σφάλμα στην προσθήκη βλαβών.")

### 📌 Προβολή Βλαβών
elif option == "Προβολή Βλαβών":
    st.header("📋 Προβολή Βλαβών")
    patient_id = st.number_input("ID Ασθενή για Αναζήτηση", min_value=1, step=1)
    if st.button("🔍 Αναζήτηση"):
        response = requests.get(f"{API_URL}/lesions/{patient_id}")
        if response.status_code == 200:
            st.json(response.json())
        else:
            st.error("❌ Δεν βρέθηκαν βλάβες για αυτόν τον ασθενή.")

### 📌 Προσθήκη Αγγείων
elif option == "Προσθήκη Αγγείων":
    st.header("➕ Προσθήκη Δεδομένων Αγγείων")
    patient_id = st.number_input("ID Ασθενή", min_value=1, step=1)
    num_vessels = st.number_input("Αριθμός Αγγείων", min_value=0, max_value=10, step=1)
    angioplasty = st.checkbox("Αγγειοπλαστική")
    imaging = st.selectbox("Απεικόνιση", ["NONE", "OCT", "IVUS"])
    if st.button("📝 Καταχώρηση"):
        data = {"patient_id": patient_id, "num_vessels": num_vessels, "angioplasty": angioplasty, "imaging": imaging}
        response = requests.post(f"{API_URL}/vessels/", json=data)
        if response.status_code == 200:
            st.success("✅ Δεδομένα αγγείων προστέθηκαν!")
        else:
            st.error("❌ Σφάλμα στην προσθήκη αγγείων.")

### 📌 Προβολή PCI
elif option == "Προβολή PCI":
    st.header("📋 Προβολή PCI")
    patient_id = st.number_input("ID Ασθενή για Αναζήτηση", min_value=1, step=1)
    if st.button("🔍 Αναζήτηση"):
        response = requests.get(f"{API_URL}/pci/{patient_id}")
        if response.status_code == 200:
            st.json(response.json())
        else:
            st.error("❌ Δεν βρέθηκαν δεδομένα PCI.")

### 📌 Προσθήκη PCI
elif option == "Προσθήκη PCI":
    st.header("➕ Προσθήκη PCI")
    patient_id = st.number_input("ID Ασθενή", min_value=1, step=1)
    balloon = st.checkbox("Balloon")
    IVL = st.checkbox("IVL")
    ROTA = st.checkbox("ROTA")
    if st.button("📝 Καταχώρηση"):
        data = {"patient_id": patient_id, "balloon": balloon, "IVL": IVL, "ROTA": ROTA}
        response = requests.post(f"{API_URL}/pci/", json=data)
        if response.status_code == 200:
            st.success("✅ PCI προστέθηκε με επιτυχία!")
        else:
            st.error("❌ Σφάλμα στην προσθήκη PCI.")

### 📌 Διαγραφή Ασθενή
elif option == "Διαγραφή Ασθενή":
    st.header("🗑️ Διαγραφή Ασθενή")
    patient_id = st.number_input("ID Ασθενή για διαγραφή", min_value=1, step=1)
    if st.button("⚠️ Διαγραφή"):
        response = requests.delete(f"{API_URL}/patients/{patient_id}")
        if response.status_code == 200:
            st.success("✅ Ο ασθενής διαγράφηκε.")
        else:
            st.error("❌ Δεν βρέθηκε ασθενής ή απέτυχε η διαγραφή.")

### 📌 Προβολή Συνολικών Στοιχείων (Πίνακας)
elif option == "Προβολή Όλων των Ασθενών (Πλήρη Δεδομένα)":
    st.header("📋 Πλήρης Πίνακας Όλων των Ασθενών")
    if st.button("📥 Φόρτωση Δεδομένων"):
        response = requests.get(f"{API_URL}/all_data/")
        if response.status_code == 200:
            data = response.json()
            rows = []
            for entry in data:
                p = entry["patient"]
                h = entry.get("history", {})
                l = entry.get("lesion", {})
                v = entry.get("vessel", {})
                pci = entry.get("pci", {})
                row = {
                    "ID": p.get("patient_id"),
                    "Όνομα": p.get("first_name", ""),
                    "Επώνυμο": p.get("last_name", ""),
                    "Ηλικία": p.get("age", ""),
                    "Ιστορικό": p.get("medical_history", ""),
                    "Φύλο": h.get("gender", "") if h else "",
                    "Υπέρταση": "ΝΑΙ" if h and h.get("hypertension") else "ΟΧΙ",
                    "Κάπνισμα": "ΝΑΙ" if h and h.get("smoking") else "ΟΧΙ",
                    "Διαβήτης": h.get("diabetes", "") if h else "",
                    "Κληρονομικότητα": "ΝΑΙ" if h and h.get("hereditary") else "ΟΧΙ",
                    "Κολπική Μαρμαρυγή": "ΝΑΙ" if h and h.get("atrial_fibrillation") else "ΟΧΙ",
                    "BMI": h.get("BMI", "") if h else "",
                    "LAD": "ΝΑΙ" if l and l.get("LAD") else "ΟΧΙ",
                    "LCX": "ΝΑΙ" if l and l.get("LCX") else "ΟΧΙ",
                    "RCA": "ΝΑΙ" if l and l.get("RCA") else "ΟΧΙ",
                    "Αρ. Αγγείων": v.get("num_vessels", "") if v else "",
                    "Αγγειοπλαστική": "ΝΑΙ" if v and v.get("angioplasty") else "ΟΧΙ",
                    "Απεικόνιση": v.get("imaging", "") if v else "",
                    "Balloon": "ΝΑΙ" if pci and pci.get("balloon") else "ΟΧΙ",
                    "IVL": "ΝΑΙ" if pci and pci.get("IVL") else "ΟΧΙ",
                    "ROTA": "ΝΑΙ" if pci and pci.get("ROTA") else "ΟΧΙ"
                }

                rows.append(row)
            st.dataframe(rows, use_container_width=True)
        else:
            st.error("❌ Πρόβλημα κατά την ανάκτηση των δεδομένων.")


elif option == "Αναζήτηση Ασθενών με Κριτήρια":
    st.header("🔍 Αναζήτηση με Κριτήρια")

    with st.expander("🧍‍♂️ Ιστορικό"):
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Ηλικία", min_value=0, max_value=120, step=1, value=0)
            diabetes = st.selectbox("Διαβήτης", ["", "Type 1", "Type 2"])
            gender = st.selectbox("Φύλο", ["", "Male", "Female"])
        with col2:
            hypertension = st.checkbox("Υπέρταση")
            smoking = st.checkbox("Κάπνισμα")
            atrial_fibrillation = st.checkbox("Κολπική Μαρμαρυγή")

    with st.expander("🫀 Βλάβες Αγγείων"):
        LAD = st.checkbox("LAD")
        LCX = st.checkbox("LCX")
        RCA = st.checkbox("RCA")

    with st.expander("🩺 PCI"):
        balloon = st.checkbox("Balloon")
        IVL = st.checkbox("IVL")
        ROTA = st.checkbox("ROTA")

    with st.expander("🧬 Αγγεία"):
        min_vessels = st.slider("Ελάχιστος αριθμός αγγείων", 0, 10, 0)
        angioplasty = st.checkbox("Αγγειοπλαστική")
        imaging = st.selectbox("Απεικόνιση", ["", "NONE", "OCT", "IVUS"])

    if st.button("🔎 Αναζήτηση"):
        params = {}
        if age > 0: params["age"] = age
        if diabetes: params["diabetes"] = diabetes
        if gender: params["gender"] = gender
        if hypertension: params["hypertension"] = True
        if smoking: params["smoking"] = True
        if atrial_fibrillation: params["atrial_fibrillation"] = True
        if LAD: params["LAD"] = True
        if LCX: params["LCX"] = True
        if RCA: params["RCA"] = True
        if balloon: params["balloon"] = True
        if IVL: params["IVL"] = True
        if ROTA: params["ROTA"] = True
        if angioplasty: params["angioplasty"] = True
        if imaging: params["imaging"] = imaging
        if min_vessels > 0: params["min_vessels"] = min_vessels

        response = requests.get(f"{API_URL}/search_patients/", params=params)
        if response.status_code == 200:
            results = response.json()
            if results:
                st.success(f"✅ Βρέθηκαν {len(results)} αποτελέσματα.")
                st.dataframe(results, use_container_width=True)
            else:
                st.info("❕ Δεν βρέθηκαν αποτελέσματα.")
        else:
            st.error("❌ Σφάλμα κατά την αναζήτηση.")