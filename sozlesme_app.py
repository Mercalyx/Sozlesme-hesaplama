import streamlit as st

st.title("Sözleşme Tutarı Hesaplama Aracı")

# Giriş Bilgileri
misafir_adi = st.text_input("Misafir Adı", "DORAK")
Tursab = st.radio("TÜRSAB Üyesi mi?", ["Evet", "Hayır"])  # "Y" yerine işaretli giriş
oda_sayisi = st.number_input("Oda Sayısı", min_value=0, value=0)
gece_sayisi = st.number_input("Gece Sayısı", min_value=0, value=0)
gecelik_fiyat = st.number_input("Gecelik Fiyat (EUR)", min_value=0.0, value=0.0)
DDR = st.number_input("Toplantı Paketi Fiyatı (DDR)", min_value=0.0, value=0.0)
Katilimci_sayisi = st.number_input("Katılımcı Sayısı", min_value=0, value=0)
gun_sayisi = st.number_input("Etkinlik Günü Sayısı", min_value=0, value=0)

# Hesaplamalar
Vergisiz_Konaklama_bedeli = oda_sayisi * gece_sayisi * gecelik_fiyat
Vergisiz_Etkinlik_bedeli = DDR * Katilimci_sayisi * gun_sayisi
Vergisiz_ara_toplam = Vergisiz_Konaklama_bedeli + Vergisiz_Etkinlik_bedeli
vergi = (vergisiz_konaklama_bedeli * 0.12) + (vergisiz_etkinlik_bedeli * 0.20)
Vergili_Konaklama_bedeli = oda_sayisi * gece_sayisi * gecelik_fiyat * 1.12
Vergili_Etkinlik_bedeli = DDR * Katilimci_sayisi * gun_sayisi * 1.20
Vergili_ara_toplam = Vergili_Konaklama_bedeli + Vergili_Etkinlik_bedeli
Komisyon_tutari = (gecelik_fiyat - 15) * 0.10 * oda_sayisi * gece_sayisi
Ara_Toplam = Vergisiz_Konaklama_bedeli + Vergisiz_Etkinlik_bedeli

damga_vergisi = 0
if Tursab == "Evet":
    damga_vergisi = 3783.20 / 82 + Vergisiz_Etkinlik_bedeli * 0.00948 / 2

if Tursab == "Hayır":
    damga_vergisi = (Vergisiz_Konaklama_bedeli + Vergisiz_Etkinlik_bedeli) * 0.00948 / 2

toplam = ara_toplam + vergi + damga_vergisi
ilk_odeme = toplam * 0.30
son_odeme = toplam * 0.70

# Çıktı
st.markdown("### 💳 Sözleşme Özeti")
st.write(f"**Şirket/Acenta:** {misafir_adi}")
st.write(f"**Oda Sayısı:** {oda_sayisi}")
st.write(f"**Gece Sayısı:** {gece_sayisi}")
st.write(f"**Gecelik Fiyat:** {gecelik_fiyat:,.2f} EUR")
st.write(f"**Konaklama Bedeli KDV Hariç:** {Vergisiz_Konaklama_bedeli:,.2f} EUR")
st.write(f"**Etkinlik Bedeli KDV Hariç:** {Vergisiz_Etkinlik_bedeli:,.2f} EUR")
st.write(f"**Konaklama Bedeli KDV Dahil:** {Vergili_Konaklama_bedeli:,.2f} EUR")
st.write(f"**Etkinlik Bedeli KDV Dahil:** {Vergili_Etkinlik_bedeli:,.2f} EUR")
st.write(f"**Vergi (%{vergi_orani * 100:.0f}):** {vergi:,.2f} EUR")
st.write(f"**Vergi (Konaklama %12 + Etkinlik %20):** {vergi:,.2f} EUR")
st.write(f"**Damga Vergisi:** {damga_vergisi:,.2f} EUR")
st.write(f"**Ara Toplam:** {ara_toplam:,.2f} EUR")
st.write(f"**Komisyon Tutarı:** {Komisyon_tutari:,.2f} EUR")
st.write(f"### ✅ İlk Ödeme: {ilk_odeme:,.2f} EUR")
st.write(f"### ✅ Son Ödeme: {son_odeme:,.2f} EUR")
st.success("Teşekkür Ederiz!")
