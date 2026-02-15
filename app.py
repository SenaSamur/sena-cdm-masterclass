import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Sena Pro CDM Tool", layout="wide")

# --- APP STATE (Veri Depolama Simülasyonu) ---
if 'audit_log' not in st.session_state:
    st.session_state.audit_log = []

# Sidebar
st.sidebar.title("🏥 Clinical Data Ops")
menu = st.sidebar.selectbox("İşlem Seçiniz:", 
    ["Study Dashboard", "eCRF Data Entry", "SAE Reconciliation", "Audit Trail Explorer"])

# --- MODÜL 1: DASHBOARD ---
if menu == "Study Dashboard":
    st.header("📊 Study Oversight Dashboard")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Subjects", "120", "+2 today")
    col2.metric("Open Queries", "14", "-3")
    col3.metric("Database Lock Readiness", "85%", "Phase: Cleaning")
    
    

# --- MODÜL 2: eCRF & AUDIT TRAIL ---
elif menu == "eCRF Data Entry":
    st.header("📝 eCRF Entry & Data Integrity")
    st.info("Not: Her değişiklik 'Audit Trail' altına kaydedilir.")
    
    with st.form("vital_signs"):
        sub_id = st.text_input("Subject ID", "SUB-001")
        sys_bp = st.number_input("Systolic BP", value=120)
        reason = st.text_input("Değişiklik Nedeni (Eğer veri güncelleniyorsa)", "")
        
        submitted = st.form_submit_button("Veriyi Kaydet")
        
        if submitted:
            # Gerçek Dünya Edit Check: Sistolik ve Diastolik mantığı
            if sys_bp > 200:
                st.error("🚩 Otomatik Query: Değer fizyolojik sınır dışı. Lütfen kontrol edin.")
            
            # Audit Trail Kaydı
            log_entry = {
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "User": "Sena_CDM_Lead",
                "Subject": sub_id,
                "Field": "SYSBP",
                "New Value": sys_bp,
                "Reason": reason if reason else "Initial Entry"
            }
            st.session_state.audit_log.append(log_entry)
            st.success("Veri başarıyla kaydedildi ve denetim izi oluşturuldu.")

# --- MODÜL 3: SAE RECONCILIATION (Kritik CDM Görevi) ---
elif menu == "SAE Reconciliation":
    st.header("🔄 AE / SAE Reconciliation")
    st.write("Aşağıdaki tabloda Klinik Veritabanı (EDC) ile Güvenlik Veritabanı (Safety DB) arasındaki uyumsuzluklar listelenmiştir.")
    
    recon_data = pd.DataFrame({
        "Subject ID": ["SUB-001", "SUB-005", "SUB-012"],
        "EDC Term": ["Baş ağrısı", "Miyokard Enfarktüsü", "Bulantı"],
        "Safety DB Term": ["Baş ağrısı", "N/A (Eksik)", "Gastrit"],
        "Status": ["✅ Match", "❌ Missing in Safety", "⚠️ Mismatch"]
    })
    
    st.table(recon_data)
    
    
    
    if st.button("Uyumsuzluklar için Query Başlat"):
        st.warning("Uyumsuzluk tespit edilen 2 vaka için sistem otomatik sorgu oluşturdu.")

# --- MODÜL 4: AUDIT TRAIL EXPLORER ---
elif menu == "Audit Trail Explorer":
    st.header("🔍 Audit Trail (21 CFR Part 11)")
    if st.session_state.audit_log:
        df_log = pd.DataFrame(st.session_state.audit_log)
        st.dataframe(df_log, use_container_width=True)
        st.download_button("Audit Trail'i Export Et (CSV)", df_log.to_csv(), "audit_trail.csv")
    else:
        st.write("Henüz bir işlem kaydı yok.")