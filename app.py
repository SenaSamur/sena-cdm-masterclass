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
    
    

# --- MODÜL 2: eCRF ---
elif menu == "2. eCRF Data Entry":
    st.header("📝 eCRF Entry & Data Integrity")
    with st.form("vital_signs"):
        sub_id = st.text_input("Subject ID", "SUB-001")
        sys_bp = st.number_input("Systolic BP", value=120)
        reason = st.text_input("Değişiklik Nedeni", "")
        submitted = st.form_submit_button("Veriyi Kaydet")
        if submitted:
            st.session_state.audit_log.append({"Timestamp": datetime.now(), "Sub": sub_id, "Val": sys_bp, "Reason": reason})
            st.success("Kaydedildi!")

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