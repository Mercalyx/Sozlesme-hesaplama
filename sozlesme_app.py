import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Sözleşme Hesaplama Robotu", page_icon="🧾")

st.title("🧾 Sözleşme Tutarı Hesaplama Robotu")
st.markdown("---")

# Şirket Bilgileri
st.header("👤 Şirket / Acenta Bilgileri")
misafir_adi = st.text_input("Şirket veya Acenta Adı", "")
Tursab = st.radio("TURSAB Üyesi mi?", ["Evet", "Hayır"])

st.markdown("---")

# Süre Bilgileri
st.header("🗓 Süre Bilgileri")
etkinlik_gun_sayisi = st.number_input("Etkinlik Süresi (Gün)", min_value=1, value=1)
konaklama_gun_sayisi = st.number_input("Konaklama Süresi (Gece)", min_value=1, value=1)

st.markdown("---")

# Para Birimi Seçimi
st.header("💱 Para Birimi Seçimi")
para_birimleri = {"EUR": "€", "USD": "$", "TL": "₺"}
secili_para_birimi = st.selectbox("Para Birimi Seçin", list(para_birimleri.keys()))
sembol = para_birimleri[secili_para_birimi]

st.markdown("---")

# Oda Bilgileri
st.header("🛏 Konaklama Bilgileri")
oda_bilgileri = []
for gun in range(konaklama_gun_sayisi):
    st.subheader(f"{gun+1}. Gece Oda Bilgisi")
    tek = st.number_input(f"Tek Kişilik Oda Sayısı (Gece {gun+1})", min_value=0, key=f"tek{gun}")
    cift = st.number_input(f"Çift Kişilik Oda Sayısı (Gece {gun+1})", min_value=0, key=f"cift{gun}")
    tek_f = st.number_input(f"Tek Kişilik Oda Fiyatı (Gece {gun+1})", min_value=0.0, key=f"tekf{gun}")
    cift_f = st.number_input(f"Çift Kişilik Oda Fiyatı (Gece {gun+1})", min_value=0.0, key=f"ciftf{gun}")

    oda_bilgileri.append({"tek": tek, "cift": cift, "tek_f": tek_f, "cift_f": cift_f})

st.markdown("---")

# Etkinlik Bilgileri - Dinamik Ekleme
st.header("🎤 Etkinlik Bilgileri")

if "etkinlikler" not in st.session_state:
    st.session_state.etkinlikler = {gun: [] for gun in range(etkinlik_gun_sayisi)}

etkinlik_turleri = ["Toplantı", "Gala", "Kokteyl", "Öğle Yemeği", "Akşam Yemeği", "Breakout", "Kurulum"]

for gun in range(etkinlik_gun_sayisi):
    st.subheader(f"{gun+1}. Gün Etkinlikleri")

    for idx, etkinlik in enumerate(st.session_state.etkinlikler[gun]):
        st.write(f"Etkinlik {idx+1}: {etkinlik['tur']} - {etkinlik['fiyat']} {sembol} - {etkinlik['kisi']} kişi")

    if st.button(f"➕ {gun+1}. Gün Etkinlik Ekle", key=f"ekle{gun}"):
        yeni_etkinlik = {}
        yeni_etkinlik["tur"] = st.selectbox(f"Etkinlik Türü (Gün {gun+1})", etkinlik_turleri, key=f"t{gun}")
        yeni_etkinlik["fiyat"] = st.number_input(f"Etkinlik Fiyatı (Kişi Başı) (Gün {gun+1})", min_value=0.0, key=f"f{gun}")
        yeni_etkinlik["kisi"] = st.number_input(f"Katılımcı Sayısı (Gün {gun+1})", min_value=0, key=f"k{gun}")

        st.session_state.etkinlikler[gun].append(yeni_etkinlik)

st.markdown("---")

# Hesaplama Modülü
st.header("🧮 Hesaplama")

vergisiz_konaklama = sum([gun_bilgi["tek"] * gun_bilgi["tek_f"] + gun_bilgi["cift"] * gun_bilgi["cift_f"] for gun_bilgi in oda_bilgileri])
vergili_konaklama = vergisiz_konaklama * 1.12
vergi_konaklama = vergisiz_konaklama * 0.12

vergisiz_etkinlik = 0
vergi_etkinlik = 0
vergili_etkinlik = 0
for gun_etkinlikler in st.session_state.etkinlikler.values():
    for etkinlik in gun_etkinlikler:
        e_tutar = etkinlik["fiyat"] * etkinlik["kisi"]
        vergi = e_tutar * 0.20
        vergisiz_etkinlik += e_tutar
        vergi_etkinlik += vergi
        vergili_etkinlik += e_tutar + vergi

damga_vergisi = 0
if Tursab == "Evet":
    damga_vergisi = 3783.20 / 82 + vergisiz_etkinlik * 0.00948 / 2
else:
    damga_vergisi = (vergisiz_konaklama + vergisiz_etkinlik) * 0.00948 / 2

toplam_tutar = vergili_konaklama + vergili_etkinlik + damga_vergisi
ilk_odeme = toplam_tutar * 0.30
son_odeme = toplam_tutar * 0.70

# Çıktı
st.success("✅ Hesaplama Tamamlandı!")

st.header("📋 Sözleşme Özeti")
st.info(f"Şirket/Acenta: {misafir_adi}")

st.write(f"Konaklama Bedeli (KDV Hariç): {vergisiz_konaklama:,.2f} {sembol}")
st.write(f"Konaklama Bedeli (KDV Dahil): {vergili_konaklama:,.2f} {sembol}")

st.write(f"Etkinlik Bedeli (KDV Hariç): {vergisiz_etkinlik:,.2f} {sembol}")
st.write(f"Etkinlik Bedeli (KDV Dahil): {vergili_etkinlik:,.2f} {sembol}")

st.write(f"Toplam KDV: {(vergi_konaklama + vergi_etkinlik):,.2f} {sembol}")
st.write(f"Damga Vergisi: {damga_vergisi:,.2f} {sembol}")
st.write(f"Genel Toplam: {toplam_tutar:,.2f} {sembol}")

st.subheader(f"🔵 İlk Ödeme (30%): {ilk_odeme:,.2f} {sembol}")
st.subheader(f"🔵 Kalan Ödeme (70%): {son_odeme:,.2f} {sembol}")

st.markdown("---")

# Excel Export
st.header("📄 Teklif Excel Çıktısı")
data = {
    "Şirket/Acenta": [misafir_adi],
    "Konaklama (KDV Hariç)": [vergisiz_konaklama],
    "Konaklama (KDV Dahil)": [vergili_konaklama],
    "Etkinlik (KDV Hariç)": [vergisiz_etkinlik],
    "Etkinlik (KDV Dahil)": [vergili_etkinlik],
    "Toplam KDV": [vergi_konaklama + vergi_etkinlik],
    "Damga Vergisi": [damga_vergisi],
    "Genel Toplam": [toplam_tutar],
    "İlk Ödeme (30%)": [ilk_odeme],
    "Kalan Ödeme (70%)": [son_odeme]
}

df = pd.DataFrame(data)

@st.cache_data
def convert_df_to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sözleşme Özeti')
    processed_data = output.getvalue()
    return processed_data

excel_data = convert_df_to_excel(df)

st.download_button(
    label="📥 Excel Olarak İndir",
    data=excel_data,
    file_name='sozlesme_ozeti.xlsx',
    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
)

st.success("✅ Teklif Excel dosyasını indirebilirsiniz!")
