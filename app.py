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

# --- MODÜL 5: EXTERNAL DATA RECONCILIATION ---
elif menu == "External Data Recon":
    st.header("🔬 External Lab Data Reconciliation")
    st.write("Bu modül, EDC vizit tarihleri ile Laboratuvardan gelen verileri karşılaştırır.")

    # 1. Simüle Edilmiş EDC Verisi (Sistemde olan)
    edc_data = pd.DataFrame({
        "Subject_ID": ["SUB-001", "SUB-002", "SUB-003", "SUB-004"],
        "Visit_Name": ["Screening", "Screening", "Visit 1", "Visit 1"],
        "EDC_Visit_Date": ["2026-01-10", "2026-01-12", "2026-02-01", "2026-02-05"]
    })
    
    # 2. Dış Veri Yükleme Alanı
    st.subheader("1. Lab Verisini Yükle (CSV/Excel)")
    uploaded_file = st.file_uploader("Laboratuvardan gelen dosyayı buraya sürükleyin", type=["csv", "xlsx"])

    if uploaded_file:
        # Örnek olarak kullanıcının yüklediği dosyayı okuyoruz
        lab_data = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        
        st.write("📂 Yüklenen Lab Verisi (Önizleme):")
        st.dataframe(lab_data.head())

        # 3. Reconciliation Mantığı (Merge/Join)
        st.subheader("2. Karşılaştırma Analizi (Recon)")
        
        # EDC ve Lab verisini Subject_ID üzerinden birleştiriyoruz
        recon_df = pd.merge(edc_data, lab_data, on="Subject_ID", how="outer", indicator=True)
        
        # Hataları Tanımlama
        recon_df['Status'] = "✅ Match"
        recon_df.loc[recon_df['_merge'] == 'left_only', 'Status'] = "❌ Missing in Lab (No Sample?)"
        recon_df.loc[recon_df['_merge'] == 'right_only', 'Status'] = "⚠️ Missing in EDC (Unscheduled Visit?)"

        st.dataframe(recon_df[["Subject_ID", "Visit_Name", "EDC_Visit_Date", "Status"]])

        # 4. Aksiyon Alma
        if st.button("Uyumsuzluklar için Otomatik Query Oluştur"):
            missing_count = len(recon_df[recon_df['Status'] != "✅ Match"])
            st.error(f"⚠️ {missing_count} adet uyumsuzluk bulundu. CDM Query Log'una işlendi.")
    else:
        st.info("Analiz yapmak için lütfen bir Lab sonuç dosyası yükleyin.")
        # Test etmen için örnek bir yapı gösterelim
        st.write("Örnek Lab Dosyası Formatı (CSV):")
        st.code("Subject_ID,Lab_Result,Lab_Date\nSUB-001,4.5,2026-01-10\nSUB-003,5.1,2026-02-01")
        
# --- MODÜL 6: IMAGING & BIOMEDICAL DATA ---
elif menu == "Imaging Review":
    st.header("🩻 Ultrasound & Imaging Core Lab Tracking")
    st.write("Bu panel, cihazlardan gelen görüntülerin (DICOM) transfer ve kalite kontrol (QC) durumunu izler.")

    # Simüle edilmiş Görüntüleme Verisi
    imaging_logs = pd.DataFrame({
        "Subject_ID": ["SUB-001", "SUB-002", "SUB-003", "SUB-004"],
        "Visit": ["Baseline", "Baseline", "Day 30", "Baseline"],
        "Modality": ["Ultrasound (Liver)", "Ultrasound (Liver)", "Cardiac Echo", "Ultrasound (Liver)"],
        "Transfer_Status": ["Uploaded", "Uploaded", "Pending", "Uploaded"],
        "Core_Lab_QC": ["Pass", "Fail (Blurry)", "N/A", "Pass"],
        "Action_Required": ["None", "Re-scan Needed", "Follow-up", "None"]
    })
    

# --- MODÜL 7: IMAGING VIEW CHECK (ABDOMINAL PROTOCOL) ---
elif menu == "Imaging View Check":
    st.header("🔍 Abdominal Ultrasound: View Completeness Check")
    st.info("Protokol Gereksinimi: Karaciğer için 5 farklı açı (Longitudinal, Transverse, Subcostal vb.) zorunludur.")

    # Protokol Tanımları (Checklist)
    liver_views = ["Longitudinal Left Lobe", "Longitudinal Right Lobe", "Transverse Main Portal Vein", "Subcostal Hepatic Veins", "Liver/Kidney Interface"]
    other_organs = ["Spleen", "Right Kidney", "Left Kidney", "Gallbladder"]

    # Simüle edilmiş çekim verileri
    if 'imaging_checklist' not in st.session_state:
        st.session_state.imaging_checklist = {
            "SUB-001": {"Liver": liver_views, "Others": other_organs}, # Tam çekim
            "SUB-002": {"Liver": ["Longitudinal Left Lobe", "Subcostal Hepatic Veins"], "Others": ["Right Kidney"]}, # Eksik çekim
            "SUB-003": {"Liver": liver_views, "Others": []} # Diğer organlar eksik
        }

    selected_sub_imaging = st.selectbox("Subject ID Seçin:", list(st.session_state.imaging_checklist.keys()))
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🥩 Liver (Karaciğer) Views")
        captured_liver = st.session_state.imaging_checklist[selected_sub_imaging]["Liver"]
        for view in liver_views:
            if view in captured_liver:
                st.write(f"✅ {view}")
            else:
                st.write(f"❌ {view} - **EKSİK**")

    with col2:
        st.subheader("🏥 Other Abdominal Organs")
        captured_others = st.session_state.imaging_checklist[selected_sub_imaging]["Others"]
        for organ in other_organs:
            if organ in captured_others:
                st.write(f"✅ {organ}")
            else:
                st.write(f"❌ {organ} - **EKSİK**")

    # Otomatik Query Tetikleyici
    st.divider()
    missing_liver = [v for v in liver_views if v not in captured_liver]
    missing_others = [o for o in other_organs if o not in captured_others]

    if missing_liver or missing_others:
        st.error(f"⚠️ Kritik Eksiklik Tespit Edildi!")
        if missing_liver:
            st.write(f"**Eksik Karaciğer Açıları:** {', '.join(missing_liver)}")
        
        if st.button("Eksik Görüntü Protokol Query'si Oluştur"):
            query_msg = f"Vizit kapsamında {', '.join(missing_liver + missing_others)} görüntüleri Core Lab sistemine ulaşmamıştır. Lütfen çekimi tekrarlayın veya mevcutsa yükleyin."
            st.warning(f"Sisteme İşlenen Query: {query_msg}")
    else:
        st.success("🎉 Tebrikler! Tüm protokol görüntüleri tam ve eksiksiz.")

    # Görselleştirme
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Görüntüleme Veri Akışı")
        st.dataframe(imaging_logs, use_container_width=True)

    with col2:
        st.subheader("QC İstatistikleri")
        qc_counts = imaging_logs["Core_Lab_QC"].value_counts()
        st.bar_chart(qc_counts)

    # CDM Müdahalesi (Query Tetikleme)
    st.divider()
    st.subheader("⚠️ Teknik Query Oluştur")
    selected_sub = st.selectbox("QC Hatası Alan Subject Seç:", imaging_logs[imaging_logs["Core_Lab_QC"] == "Fail (Blurry)"]["Subject_ID"])
    
    if selected_sub:
        st.warning(f"Dikkat: {selected_sub} için görüntü kalitesi düşük. Yeniden tarama (re-scan) talep edilmelidir.")
        if st.button(f"{selected_sub} için Siteye Bildir"):
            st.success(f"Siteye teknik talimat gönderildi: 'Lütfen probe (L6-12rs) ayarlarını kontrol ederek çekimi tekrarlayın.'")
        