import streamlit as st

st.title("Fatura Hesaplama Aracı")

# Giriş Bilgileri
misafir_adi = st.text_input("Misafir Adı", "DORAK")
Tursab = st.radio("TÜRSAB Üyesi mi?", ["Evet", "Hayır"])  # "Y" yerine işaretli giriş
oda_sayisi = st.number_input("Oda Sayısı", min_value=1, value=45)
gece_sayisi = st.number_input("Gece Sayısı", min_value=1, value=2)
gecelik_fiyat = st.number_input("Gecelik Fiyat (EUR)", min_value=0.0, value=220.0)
vergi_orani = st.number_input("Vergi Oranı", min_value=0.0, max_value=1.0, value=0.12)
DDR = st.number_input("Günlük Etkinlik Fiyatı (DDR)", min_value=0.0, value=75.0)
HDDR = st.number_input("Günlük Etkinlik Fiyatı (HDDR)", min_value=0.0, value=70.0)
Katilimci_sayisi = st.number_input("Katılımcı Sayısı", min_value=1, value=50)
gun_sayisi = st.number_input("Etkinlik Günü Sayısı", min_value=1, value=3)

# Hesaplamalar
Konaklama_bedeli = oda_sayisi * gece_sayisi * gecelik_fiyat
Etkinlik_bedeli = DDR * Katilimci_sayisi * gun_sayisi
ara_toplam = Konaklama_bedeli + Etkinlik_bedeli
vergi = ara_toplam * vergi_orani
Komisyon_tutari = (gecelik_fiyat - 15) * 0.10 * oda_sayisi * gece_sayisi

damga_vergisi = 0
if Tursab == "Evet":
    damga_vergisi = 3783.20 / 82 + Etkinlik_bedeli * 0.00948 / 2

toplam = ara_toplam + vergi + damga_vergisi

# Çıktı
st.markdown("### 💳 Fatura Özeti")
st.write(f"**Müşteri:** {misafir_adi}")
st.write(f"**Oda Sayısı:** {oda_sayisi}")
st.write(f"**Gece Sayısı:** {gece_sayisi}")
st.write(f"**Gecelik Fiyat:** {gecelik_fiyat:,.2f} EUR")
st.write(f"**Konaklama Bedeli:** {Konaklama_bedeli:,.2f} EUR")
st.write(f"**Etkinlik Bedeli:** {Etkinlik_bedeli:,.2f} EUR")
st.write(f"**Ara Toplam:** {ara_toplam:,.2f} EUR")
st.write(f"**Vergi (%{vergi_orani * 100:.0f}):** {vergi:,.2f} EUR")
st.write(f"**Damga Vergisi:** {damga_vergisi:,.2f} EUR")
st.write(f"**Komisyon Tutarı:** {Komisyon_tutari:,.2f} EUR")
st.write(f"### ✅ Toplam Ödeme: {toplam:,.2f} EUR")
st.success("Teşekkür Ederiz!")
