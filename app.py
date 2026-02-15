import streamlit as st
import pandas as pd
from datetime import datetime

# Uygulama Başlığı ve Sidebar
st.set_page_config(page_title="Sena CDM Workbench", layout="wide")
st.sidebar.title("🛠️ CDM İş Akışı")
menu = st.sidebar.radio("Modül Seçiniz:", 
    ["1. Study Design (eCRF)", "2. Data Entry & Edit Checks", "3. Query Management", "4. Medical Coding"])

# --- MODÜL 1: STUDY DESIGN ---
if menu == "1. Study Design (eCRF)":
    st.header("📋 eCRF Tasarım Modülü (Hafta 2)")
    st.info("Burada protokolü veri mimarisine çeviriyoruz.")
    
    crf_data = {
        "Field Label": ["Subject ID", "Visit Date", "Systolic BP", "Diastolic BP", "Adverse Event?"],
        "Variable Name": ["SUBJID", "VISDAT", "SYSBP", "DIABP", "AE_YN"],
        "Type": ["Numeric", "Date", "Number", "Number", "Boolean"],
        "Validation": ["Required", "Current/Past", "30-250", "20-150", "Required"]
    }
    st.table(pd.DataFrame(crf_data))
    st.success("Çıktı: CRF Specification v1.0 hazır.")

# --- MODÜL 2: DATA ENTRY & EDIT CHECKS ---
elif menu == "2. Data Entry & Edit Checks":
    st.header("⌨️ Veri Girişi ve Otomatik Kontroller (Hafta 3)")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Veri Giriş Formu")
        sub_id = st.text_input("Subject ID", "1001")
        sys_bp = st.number_input("Systolic BP (mmHg)", value=120)
        dia_bp = st.number_input("Diastolic BP (mmHg)", value=80)
        ae_status = st.selectbox("Adverse Event var mı?", ["Hayır", "Evet"])
        
    with col2:
        st.subheader("Otomatik Edit Checks (DVP)")
        # Gerçek zamanlı kontrol simülasyonu
        if sys_bp > 200 or sys_bp < 70:
            st.error(f"🚩 🚩 [SYSBP_RANGE]: {sys_bp} değeri klinik sınırların dışında! (70-200)")
        if sys_bp <= dia_bp:
            st.error("🚩 [BP_CONSISTENCY]: Sistolik değer Diastolikten küçük veya eşit olamaz.")
        if ae_status == "Evet":
            st.warning("🔔 [AE_RECON]: Lütfen AE formunu doldurmayı unutmayın.")
        else:
            st.success("✅ Veri şu anki kurallara göre temiz.")

# --- MODÜL 3: QUERY MANAGEMENT ---
elif menu == "3. Query Management":
    st.header("❓ Query (Sorgu) Yönetimi (Hafta 4)")
    
    queries = pd.DataFrame([
        {"ID": "Q1", "Field": "SYSBP", "Issue": "Value 12 mmHg is improbable", "Status": "Open", "Aging": "3 Days"},
        {"ID": "Q2", "Field": "VISDAT", "Issue": "Future date entered", "Status": "Answered", "Aging": "1 Day"},
    ])
    
    st.dataframe(queries, use_container_width=True)
    
    st.subheader("Yeni Query Oluştur")
    q_text = st.text_area("Siteye mesajınız:", placeholder="Lütfen kaynak dökümanı kontrol ederek değeri düzeltiniz...")
    if st.button("Query Gönder"):
        st.info("Query sisteme işlendi ve merkeze iletildi.")

# --- MODÜL 4: MEDICAL CODING ---
elif menu == "4. Medical Coding":
    st.header("🧬 Medical Coding (MedDRA) (Hafta 6)")
    
    verbatim = st.text_input("Sahanın girdiği terim (Verbatim):", "Mide yanması ve ağrı")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**MedDRA Hiyerarşisi**")
        st.code("""
        LLT: Mide yanması
        PT: Gastrointestinal ağrı
        SOC: Gastrointestinal hastalıklar
        """)
    with col2:
        if st.button("Kodu Onayla"):
            st.success(f"'{verbatim}' terimi MedDRA 26.1 ile başarıyla kodlandı.")