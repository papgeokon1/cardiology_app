
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import streamlit as st

# === DATABASE SETUP ===
DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# === MODELS ===
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

# === CREATE TABLES ===
Base.metadata.create_all(bind=engine)

# === STREAMLIT APP START ===
st.title("🫀 Cardiology App (SQLite Version)")

db = SessionLocal()
st.success("✅ Η βάση δεδομένων είναι έτοιμη.")

st.write("Μπορείς να ξεκινήσεις να ενσωματώνεις τις ενότητες του frontend εδώ...")



# === Επιλογή λειτουργίας ===
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

# === Προσθήκη Ασθενή ===
if option == "Προσθήκη Ασθενή":
    st.subheader("➕ Προσθήκη Νέου Ασθενή")
    first_name = st.text_input("Όνομα")
    last_name = st.text_input("Επώνυμο")
    age = st.number_input("Ηλικία", min_value=1, max_value=120, step=1)
    medical_history = st.text_area("Ιατρικό Ιστορικό")
    if st.button("📝 Καταχώρηση"):
        if first_name and last_name:
            new_patient = Patient(
                first_name=first_name,
                last_name=last_name,
                age=age,
                medical_history=medical_history
            )
            db.add(new_patient)
            db.commit()
            st.success("✅ Ο ασθενής προστέθηκε με επιτυχία!")
        else:
            st.warning("⚠️ Συμπληρώστε όλα τα πεδία.")

# === Λίστα Ασθενών ===
elif option == "Λίστα Ασθενών":
    st.subheader("📋 Λίστα Ασθενών")
    patients = db.query(Patient).all()
    if patients:
        for p in patients:
            st.write(f"🆔 {p.patient_id} - {p.first_name} {p.last_name}, {p.age} ετών")
    else:
        st.info("❕ Δεν υπάρχουν καταχωρημένοι ασθενείς.")



# === Προσθήκη Ιατρικού Ιστορικού ===
elif option == "Προσθήκη Ιατρικού Ιστορικού":
    st.subheader("➕ Προσθήκη Ιατρικού Ιστορικού")
    patient_id = st.number_input("ID Ασθενή", min_value=1, step=1)
    gender = st.selectbox("Φύλο", ["Male", "Female"])
    hypertension = st.checkbox("Υπέρταση")
    smoking = st.checkbox("Κάπνισμα")
    diabetes = st.selectbox("Διαβήτης", ["None", "Type 1", "Type 2"])
    hereditary = st.checkbox("Κληρονομικό Ιστορικό")
    BMI = st.number_input("BMI", min_value=10.0, max_value=50.0, step=0.1)
    atrial_fibrillation = st.checkbox("Κολπική Μαρμαρυγή")
    if st.button("📝 Καταχώρηση Ιστορικού"):
        if db.query(Patient).filter_by(patient_id=patient_id).first():
            hist = MedicalHistory(
                patient_id=patient_id,
                gender=gender,
                hypertension=hypertension,
                smoking=smoking,
                diabetes=diabetes,
                hereditary=hereditary,
                BMI=BMI,
                atrial_fibrillation=atrial_fibrillation
            )
            db.add(hist)
            db.commit()
            st.success("✅ Το ιστορικό προστέθηκε.")
        else:
            st.error("❌ Ο ασθενής δεν βρέθηκε.")


elif option == "Λίστα Ιατρικών Ιστορικών":
    st.header("📜 Λίστα Ιατρικών Ιστορικών")
    patient_id = st.number_input("ID Ασθενή για Αναζήτηση", min_value=1, step=1)
    if st.button("🔍 Αναζήτηση"):
        history = db.query(MedicalHistory).filter_by(patient_id=patient_id).first()
        if history:
            st.json({
                "Φύλο": history.gender,
                "Υπέρταση": history.hypertension,
                "Κάπνισμα": history.smoking,
                "Διαβήτης": history.diabetes,
                "Κληρονομικότητα": history.hereditary,
                "BMI": history.BMI,
                "Κολπική Μαρμαρυγή": history.atrial_fibrillation
            })
        else:
            st.warning("❕ Δεν βρέθηκε ιατρικό ιστορικό.")


# === Προσθήκη Βλαβών Αγγείων ===
elif option == "Προσθήκη Βλαβών Αγγείων":
    st.subheader("➕ Προσθήκη Βλαβών Αγγείων")
    patient_id = st.number_input("ID Ασθενή", min_value=1, step=1)
    LAD = st.checkbox("LAD")
    LCX = st.checkbox("LCX")
    RCA = st.checkbox("RCA")
    if st.button("📝 Καταχώρηση Βλαβών"):
        if db.query(Patient).filter_by(patient_id=patient_id).first():
            lesion = Lesion(patient_id=patient_id, LAD=LAD, LCX=LCX, RCA=RCA)
            db.add(lesion)
            db.commit()
            st.success("✅ Οι βλάβες προστέθηκαν.")
        else:
            st.error("❌ Ο ασθενής δεν βρέθηκε.")

elif option == "Προβολή Βλαβών":
    st.header("📋 Προβολή Βλαβών")
    patient_id = st.number_input("ID Ασθενή για Αναζήτηση", min_value=1, step=1)
    if st.button("🔍 Αναζήτηση"):
        lesion = db.query(Lesion).filter_by(patient_id=patient_id).first()
        if lesion:
            st.json({
                "LAD": lesion.LAD,
                "LCX": lesion.LCX,
                "RCA": lesion.RCA
            })
        else:
            st.warning("❕ Δεν βρέθηκαν καταχωρημένες βλάβες.")


# === Προσθήκη Αγγείων ===
elif option == "Προσθήκη Αγγείων":
    st.subheader("➕ Προσθήκη Αγγείων")
    patient_id = st.number_input("ID Ασθενή", min_value=1, step=1)
    num_vessels = st.number_input("Αριθμός Αγγείων", min_value=0, max_value=10, step=1)
    angioplasty = st.checkbox("Αγγειοπλαστική")
    imaging = st.selectbox("Απεικόνιση", ["NONE", "OCT", "IVUS"])
    if st.button("📝 Καταχώρηση Αγγείων"):
        if db.query(Patient).filter_by(patient_id=patient_id).first():
            vessel = Vessel(patient_id=patient_id, num_vessels=num_vessels, angioplasty=angioplasty, imaging=imaging)
            db.add(vessel)
            db.commit()
            st.success("✅ Τα αγγεία προστέθηκαν.")
        else:
            st.error("❌ Ο ασθενής δεν βρέθηκε.")

elif option == "Προβολή Αγγείων":
    st.header("📋 Προβολή Αγγείων")
    patient_id = st.number_input("ID Ασθενή για Αναζήτηση", min_value=1, step=1)
    if st.button("🔍 Αναζήτηση"):
        vessel = db.query(Vessel).filter_by(patient_id=patient_id).first()
        if vessel:
            st.json({
                "Αριθμός Αγγείων": vessel.num_vessels,
                "Αγγειοπλαστική": "ΝΑΙ" if vessel.angioplasty else "ΟΧΙ",
                "Απεικόνιση": vessel.imaging
            })
        else:
            st.warning("❕ Δεν βρέθηκαν δεδομένα αγγείων.")


# === Προσθήκη PCI ===
elif option == "Προσθήκη PCI":
    st.subheader("➕ Προσθήκη PCI")
    patient_id = st.number_input("ID Ασθενή", min_value=1, step=1)
    balloon = st.checkbox("Balloon")
    IVL = st.checkbox("IVL")
    ROTA = st.checkbox("ROTA")
    if st.button("📝 Καταχώρηση PCI"):
        if db.query(Patient).filter_by(patient_id=patient_id).first():
            pci = PCI(patient_id=patient_id, balloon=balloon, IVL=IVL, ROTA=ROTA)
            db.add(pci)
            db.commit()
            st.success("✅ PCI προστέθηκε.")
        else:
            st.error("❌ Ο ασθενής δεν βρέθηκε.")

elif option == "Προβολή PCI":
    st.header("📋 Προβολή PCI")
    patient_id = st.number_input("ID Ασθενή για Αναζήτηση", min_value=1, step=1)
    if st.button("🔍 Αναζήτηση"):
        pci = db.query(PCI).filter_by(patient_id=patient_id).first()
        if pci:
            st.json({
                "Balloon": pci.balloon,
                "IVL": pci.IVL,
                "ROTA": pci.ROTA
            })
        else:
            st.warning("❕ Δεν βρέθηκαν δεδομένα PCI.")


# === Διαγραφή Ασθενή ===
elif option == "Διαγραφή Ασθενή":
    st.subheader("🗑️ Διαγραφή Ασθενή")
    patient_id = st.number_input("ID Ασθενή για διαγραφή", min_value=1, step=1)
    if st.button("⚠️ Διαγραφή"):
        patient = db.query(Patient).filter_by(patient_id=patient_id).first()
        if patient:
            db.delete(patient)
            db.commit()
            st.success("✅ Ο ασθενής διαγράφηκε.")
        else:
            st.error("❌ Δεν βρέθηκε ασθενής.")


elif option == "Προβολή Όλων των Ασθενών (Πλήρη Δεδομένα)":
    st.header("📋 Πλήρης Πίνακας Όλων των Ασθενών")
    if st.button("📥 Φόρτωση Δεδομένων"):
        rows = []
        patients = db.query(Patient).all()
        for p in patients:
            h = db.query(MedicalHistory).filter_by(patient_id=p.patient_id).first()
            l = db.query(Lesion).filter_by(patient_id=p.patient_id).first()
            v = db.query(Vessel).filter_by(patient_id=p.patient_id).first()
            pci = db.query(PCI).filter_by(patient_id=p.patient_id).first()
            row = {
                "ID": p.patient_id,
                "Όνομα": p.first_name,
                "Επώνυμο": p.last_name,
                "Ηλικία": p.age,
                "Ιστορικό": p.medical_history,
                "Φύλο": h.gender if h else "",
                "Υπέρταση": "ΝΑΙ" if h and h.hypertension else "ΟΧΙ",
                "Κάπνισμα": "ΝΑΙ" if h and h.smoking else "ΟΧΙ",
                "Διαβήτης": h.diabetes if h else "",
                "Κληρονομικότητα": "ΝΑΙ" if h and h.hereditary else "ΟΧΙ",
                "Κολπική Μαρμαρυγή": "ΝΑΙ" if h and h.atrial_fibrillation else "ΟΧΙ",
                "BMI": h.BMI if h else "",
                "LAD": "ΝΑΙ" if l and l.LAD else "ΟΧΙ",
                "LCX": "ΝΑΙ" if l and l.LCX else "ΟΧΙ",
                "RCA": "ΝΑΙ" if l and l.RCA else "ΟΧΙ",
                "Αρ. Αγγείων": v.num_vessels if v else "",
                "Αγγειοπλαστική": "ΝΑΙ" if v and v.angioplasty else "ΟΧΙ",
                "Απεικόνιση": v.imaging if v else "",
                "Balloon": "ΝΑΙ" if pci and pci.balloon else "ΟΧΙ",
                "IVL": "ΝΑΙ" if pci and pci.IVL else "ΟΧΙ",
                "ROTA": "ΝΑΙ" if pci and pci.ROTA else "ΟΧΙ"
            }
            rows.append(row)
        st.dataframe(rows, use_container_width=True)

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
        results = []
        all_patients = db.query(Patient).all()

        for p in all_patients:
            h = db.query(MedicalHistory).filter_by(patient_id=p.patient_id).first()
            l = db.query(Lesion).filter_by(patient_id=p.patient_id).first()
            v = db.query(Vessel).filter_by(patient_id=p.patient_id).first()
            pci = db.query(PCI).filter_by(patient_id=p.patient_id).first()

            match = True
            if age > 0 and p.age != age:
                match = False
            if gender and (not h or h.gender != gender):
                match = False
            if diabetes and (not h or h.diabetes != diabetes):
                match = False
            if hypertension and (not h or not h.hypertension):
                match = False
            if smoking and (not h or not h.smoking):
                match = False
            if atrial_fibrillation and (not h or not h.atrial_fibrillation):
                match = False
            if LAD and (not l or not l.LAD):
                match = False
            if LCX and (not l or not l.LCX):
                match = False
            if RCA and (not l or not l.RCA):
                match = False
            if balloon and (not pci or not pci.balloon):
                match = False
            if IVL and (not pci or not pci.IVL):
                match = False
            if ROTA and (not pci or not pci.ROTA):
                match = False
            if angioplasty and (not v or not v.angioplasty):
                match = False
            if imaging and (not v or v.imaging != imaging):
                match = False
            if min_vessels > 0 and (not v or v.num_vessels < min_vessels):
                match = False

            if match:
                results.append({
                    "ID": p.patient_id,
                    "Όνομα": p.first_name,
                    "Επώνυμο": p.last_name,
                    "Ηλικία": p.age,
                    "Φύλο": h.gender if h else "",
                    "Διαβήτης": h.diabetes if h else "",
                    "Αρ. Αγγείων": v.num_vessels if v else "",
                    "Balloon": "ΝΑΙ" if pci and pci.balloon else "ΟΧΙ"
                })

        if results:
            st.success(f"✅ Βρέθηκαν {len(results)} αποτελέσματα.")
            st.dataframe(results, use_container_width=True)
        else:
            st.warning("❕ Δεν βρέθηκαν αποτελέσματα.")
