import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Sena Pro CDM Tool", layout="wide")

# --- APP STATE (Veri Kaybını Önlemek İçin) ---
if 'audit_log' not in st.session_state:
    st.session_state.audit_log = []

# --- SIDEBAR (Menü Burasıdır, Buraya Eklenmezse Görünmez) ---
st.sidebar.title("🏥 Clinical Data Ops")
menu = st.sidebar.radio("İşlem Seçiniz:", [
    "1. Study Dashboard", 
    "2. eCRF Data Entry", 
    "3. Query Management", 
    "4. Medical Coding", 
    "5. External Data Recon", 
    "6. Imaging Review", 
    "7. Imaging View Check" # Yeni eklediğimiz modül
])

# --- MODÜL 1: DASHBOARD ---
if menu == "1. Study Dashboard":
    st.header("📊 Study Oversight Dashboard")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Subjects", "120", "+2 today")
    col2.metric("Open Queries", "14", "-3")
    col3.metric("Database Lock Readiness", "85%", "Phase: Cleaning")
    
    

# --- MODÜL 2: eCRF DATA ENTRY (FDA & GCP COMPLIANT) ---
elif menu == "2. eCRF Data Entry":
    st.header("📋 FDA & GCP Compliant eCRF: Subject Enrollment")
    st.info("GCP Gerekliliği: Veri girişi yapılmadan önce 'Informed Consent' (ICF) alınmış olmalıdır.")

    with st.form("subject_enrollment"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📌 Administrative Data")
            sub_id = st.text_input("Subject ID (Unique)", placeholder="Örn: 101-001")
            # FDA gereği: Veri girişi yapanın kimliği ve tarih-saat otomatik tutulur (Audit Trail)
            icf_date = st.date_input("Informed Consent Verilme Tarihi")
            site_id = st.selectbox("Site ID", ["001 - İstanbul", "002 - Ankara", "003 - Londra"])

        with col2:
            st.subheader("👤 Demographics")
            birth_year = st.number_input("Doğum Yılı", min_value=1940, max_value=2026, value=1990)
            sex = st.radio("Cinsiyet (At Birth)", ["Male", "Female", "Undifferentiated"])
            ethnicity = st.selectbox("Ethnicity (FDA Requirement)", ["Hispanic or Latino", "Not Hispanic or Latino", "Unknown"])
            race = st.multiselect("Race", ["White", "Black or African American", "Asian", "Other"])

        st.divider()
        st.subheader("🩺 Clinical Baseline")
        weight = st.number_input("Weight (kg)", min_value=30.0, max_value=250.0, step=0.1)
        medical_history = st.text_area("Önemli Tıbbi Geçmiş (Medical History)")

        # Audit Trail Nedeni (FDA 21 CFR Part 11 gereği)
        st.warning("⚠️ Önemli: Eğer bu veriyi güncelliyorsanız, aşağıya 'Change Reason' girmek zorunludur.")
        change_reason = st.text_input("Reason for Change / Entry")

        # Form Submit
        submitted = st.form_submit_button("Submit to Database")

        if submitted:
            # GCP Edit Check 1: ICF tarihi bugünden sonra olamaz
            if icf_date > datetime.now().date():
                st.error("🚩 GCP Error: Onay tarihi gelecek bir tarih olamaz!")
            
            # GCP Edit Check 2: Zorunlu alan kontrolü
            elif not sub_id or not change_reason:
                st.error("🚩 FDA Error: Subject ID ve Change Reason boş bırakılamaz (Data Integrity).")
            
            else:
                # Veriyi Audit Log'a yazma
                new_entry = {
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "User": "Sena_CDM_Lead",
                    "Subject": sub_id,
                    "ICF_Date": str(icf_date),
                    "Action": "Data Entry",
                    "Reason": change_reason
                }
                st.session_state.audit_log.append(new_entry)
                st.success(f"✅ Subject {sub_id} başarıyla kaydedildi. Audit trail oluşturuldu.")

# --- MODÜL 3: QUERY ---
elif menu == "3. Query Management":
    st.header("❓ Query Management")
    st.write("Açık sorguları buradan yönetebilirsiniz.")

# --- MODÜL 4: CODING ---
elif menu == "4. Medical Coding":
    st.header("🧬 MedDRA Coding")
    st.text_input("Verbatim Term:", "Baş ağrısı")

# --- MODÜL 5: EXTERNAL RECON ---
elif menu == "5. External Data Recon":
    st.header("🔬 Lab Reconciliation")
    st.file_uploader("Lab Dosyası Yükle")

# --- MODÜL 6: IMAGING REVIEW ---
elif menu == "6. Imaging Review":
    st.header("🩻 Imaging Core Lab Tracking")
    st.write("Görüntü transfer durumları.")

# --- MODÜL 7: IMAGING VIEW CHECK (Senin İstediğin Modül) ---
elif menu == "7. Imaging View Check":
    st.header("🔍 Abdominal Ultrasound: View Completeness Check")
    
    liver_views = ["Longitudinal Left Lobe", "Longitudinal Right Lobe", "Transverse Main Portal Vein", "Subcostal Hepatic Veins", "Liver/Kidney Interface"]
    other_organs = ["Spleen", "Right Kidney", "Left Kidney", "Gallbladder"]

    sub_id = st.selectbox("Subject ID:", ["SUB-001", "SUB-002"])
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🥩 Liver Views")
        # Örnek: SUB-002'de bazıları eksik görünsün
        for view in liver_views:
            status = "✅" if (sub_id == "SUB-001" or "Long" in view) else "❌"
            st.write(f"{status} {view}")
            
    with col2:
        st.subheader("🏥 Other Organs")
        for organ in other_organs:
            status = "✅" if sub_id == "SUB-001" else "❌"
            st.write(f"{status} {organ}")