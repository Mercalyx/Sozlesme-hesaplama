import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sözleşme Hesaplama Robotu", page_icon="🧾")

st.title("🧾 Sözleşme Tutarı Hesaplama Robotu")
st.markdown("---")

# Şirket/Acenta bilgileri
st.header("👤 Şirket / Acenta Bilgileri")
misafir_adi = st.text_input("Şirket veya Acenta Adı", "")
Tursab = st.radio("TURSAB Üyesi mi?", ["Evet", "Hayır"])

st.markdown("---")

# Para Birimi Seçimi
st.header("💱 Para Birimi Seçimi")
para_birimleri = {"EUR": "€", "USD": "$", "TL": "₺"}
secili_para_birimi = st.selectbox("Para Birimi Seçin", list(para_birimleri.keys()))
sembol = para_birimleri[secili_para_birimi]

st.markdown("---")

# Süre Bilgileri
st.header("🗓 Süre Bilgileri")
etkinlik_gun_sayisi = st.number_input("Etkinlik Süresi (Gün)", min_value=1, value=1)
konaklama_gun_sayisi = st.number_input("Konaklama Süresi (Gece)", min_value=1, value=1)

st.markdown("---")

# Farklılık seçenekleri
st.header("⚙ Bilgi Giriş Ayarları")
etkinlik_farkli_mi = st.checkbox("Her gün için farklı etkinlik bilgisi girilsin mi?", value=True)
oda_farkli_mi = st.checkbox("Her gün için farklı oda bilgisi girilsin mi?", value=True)

etkinlik_fiyat_degisim = st.radio("Her gün etkinlik fiyatı değişiyor mu?", ["Hayır", "Evet"]) if etkinlik_farkli_mi else "Hayır"
oda_fiyat_degisim = st.radio("Her gün oda fiyatı değişiyor mu?", ["Hayır", "Evet"]) if oda_farkli_mi else "Hayır"

st.markdown("---")

# Başlangıç Fiyatları
st.header("💶 Başlangıç Oda ve Etkinlik Fiyatları")
tek_kisilik_standart_fiyat = st.number_input("Tek Kişilik Oda Standart Fiyatı (gecelik)", min_value=0.0, value=0.0)
cift_kisilik_standart_fiyat = st.number_input("Çift Kişilik Oda Standart Fiyatı (gecelik)", min_value=0.0, value=0.0)

etkinlik_turleri = ["Toplantı", "Gala", "Kokteyl", "Öğle Yemeği", "Akşam Yemeği", "Breakout", "Kurulum"]
standart_etkinlik_fiyatlari = {}
for tur in etkinlik_turleri:
    fiyat = st.number_input(f"{tur} Standart Fiyatı (Kişi Başı)", min_value=0.0, value=0.0, key=f"standart_{tur}")
    standart_etkinlik_fiyatlari[tur] = fiyat

st.markdown("---")

# Oda Bilgileri
st.header("🛏 Konaklama Bilgileri")
oda_bilgileri = []
for gun in range(konaklama_gun_sayisi):
    st.subheader(f"{gun+1}. Gece Oda Bilgisi")
    tek = st.number_input(f"Tek Kişilik Oda Sayısı (Gece {gun+1})", min_value=0, key=f"tek{gun}")
    cift = st.number_input(f"Çift Kişilik Oda Sayısı (Gece {gun+1})", min_value=0, key=f"cift{gun}")

    if oda_farkli_mi and oda_fiyat_degisim == "Evet":
        tek_f = st.number_input(f"Tek Kişilik Oda Fiyatı (Gece {gun+1})", min_value=0.0, key=f"tekf{gun}")
        cift_f = st.number_input(f"Çift Kişilik Oda Fiyatı (Gece {gun+1})", min_value=0.0, key=f"ciftf{gun}")
    else:
        tek_f = tek_kisilik_standart_fiyat
        cift_f = cift_kisilik_standart_fiyat

    oda_bilgileri.append({"tek": tek, "cift": cift, "tek_f": tek_f, "cift_f": cift_f})

st.markdown("---")

# Etkinlik Bilgileri
st.header("🎤 Etkinlik Bilgileri")
etkinlikler = []

for gun in range(gun_sayisi):
    st.subheader(f"{gun+1}. Gün Etkinlikleri")

    # Sayacı başlat
    if f"etkinlik_sayaci_{gun}" not in st.session_state:
        st.session_state[f"etkinlik_sayaci_{gun}"] = 1

    if st.button(f"{gun+1}. Gün İçin Etkinlik Ekle", key=f"etkinlik_ekle_{gun}"):
        st.session_state[f"etkinlik_sayaci_{gun}"] += 1

    g_etkinlikler = []
    for j in range(st.session_state[f"etkinlik_sayaci_{gun}"]):
        tur = st.selectbox(f"Etkinlik Türü {j+1} (Gün {gun+1})", options=etkinlik_turleri, key=f"t{gun}_{j}")

        if etkinlik_farkli_mi and etkinlik_fiyat_degisim == "Evet":
            fiyat = st.number_input(f"{tur} Fiyatı (Gün {gun+1})", min_value=0.0, key=f"f{gun}_{j}")
        else:
            fiyat = standart_etkinlik_fiyatlari[tur]

        kisi = st.number_input(f"{tur} Katılımcı Sayısı (Gün {gun+1})", min_value=0, key=f"k{gun}_{j}")
        g_etkinlikler.append({"tur": tur, "fiyat": fiyat, "kisi": kisi})

    etkinlikler.append(g_etkinlikler)

st.markdown("---")

# Hesaplama Modülü
st.header("🧮 Hesaplama")

vergisiz_konaklama = sum([gun_bilgi["tek"] * gun_bilgi["tek_f"] + gun_bilgi["cift"] * gun_bilgi["cift_f"] for gun_bilgi in oda_bilgileri])
vergili_konaklama = vergisiz_konaklama * 1.12
vergi_konaklama = vergisiz_konaklama * 0.12

vergisiz_etkinlik = 0
vergi_etkinlik = 0
vergili_etkinlik = 0
for gun in etkinlikler:
    for etkinlik in gun:
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
st.write(f"Konaklama Bedeli (KDV Hariç): {vergisiz_konaklama:,.2f} EUR")
st.write(f"Etkinlik Bedeli (KDV Hariç): {vergisiz_etkinlik:,.2f} EUR")
st.write(f"Toplam KDV: {(vergi_konaklama + vergi_etkinlik):,.2f} EUR")
st.write(f"Damga Vergisi: {damga_vergisi:,.2f} EUR")
st.write(f"Genel Toplam: {toplam_tutar:,.2f} EUR")
st.subheader(f"🔵 İlk Ödeme (30%): {ilk_odeme:,.2f} EUR")
st.subheader(f"🔵 Kalan Ödeme (70%): {son_odeme:,.2f} EUR")

st.markdown("---")

# Excel Export
st.header("📄 Teklif Excel Çıktısı")
data = {
    "Şirket/Acenta": [misafir_adi],
    "Konaklama (KDV Hariç)": [vergisiz_konaklama],
    "Etkinlik (KDV Hariç)": [vergisiz_etkinlik],
    "Toplam KDV": [vergi_konaklama + vergi_etkinlik],
    "Damga Vergisi": [damga_vergisi],
    "Genel Toplam": [toplam_tutar],
    "İlk Ödeme (30%)": [ilk_odeme],
    "Kalan Ödeme (70%)": [son_odeme]
}

df = pd.DataFrame(data)

import io

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
