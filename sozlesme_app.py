import streamlit as st

st.title("Sözleşme Tutarı Hesaplama Aracı")

# Kullanıcıdan temel veriler alma
misafir_adi = st.text_input("Misafir Adı", "")
Tursab = st.radio("TÜRSAB Üyesi mi?", ["Evet", "Hayır"])

gun_sayisi = st.number_input("Etkinlik Süresi (Gün)", min_value=1, value=1)

oda_farkli_mi = st.checkbox("Her gün için farklı oda bilgisi girilsin mi?")
oda_fiyat_degisim = st.radio("Her gün oda fiyatları değişiyor mu?", ["Hayır", "Evet"]) if oda_farkli_mi else "Hayır"

etkinlik_farkli_mi = st.checkbox("Her gün için farklı etkinlik bilgisi girilsin mi?")
etkinlik_fiyat_degisim = st.radio("Her gün etkinlik fiyatları değişiyor mu?", ["Hayır", "Evet"]) if etkinlik_farkli_mi else "Hayır"

st.markdown("---")

# Başlangıç Fiyatları (Eğer değişmeyecekse)
st.header("Başlangıç Oda ve Etkinlik Fiyatları")

# Oda fiyatları
tek_kisilik_standart_fiyat = st.number_input("Tek Kişilik Oda Standart Fiyatı (gecelik)", min_value=0.0, value=0.0)
cift_kisilik_standart_fiyat = st.number_input("Çift Kişilik Oda Standart Fiyatı (gecelik)", min_value=0.0, value=0.0)

# Etkinlik fiyatları (her tür için)
etkinlik_turleri = ["Toplantı", "Gala", "Kokteyl", "Workshop"]
standart_etkinlik_fiyatlari = {}
for tur in etkinlik_turleri:
    fiyat = st.number_input(f"{tur} Standart Fiyatı (Kişi Başı)", min_value=0.0, value=0.0, key=f"standart_{tur}")
    standart_etkinlik_fiyatlari[tur] = fiyat

st.markdown("---")

# Oda Bilgileri
st.header("🛏 Oda Bilgileri")
oda_bilgileri = []
for gun in range(gun_sayisi):
    st.subheader(f"{gun+1}. Gün Oda Bilgisi")
    tek = st.number_input(f"Tek Kişilik Oda Sayısı (Gün {gun+1})", min_value=0, key=f"tek{gun}")
    cift = st.number_input(f"Çift Kişilik Oda Sayısı (Gün {gun+1})", min_value=0, key=f"cift{gun}")

    if oda_farkli_mi and oda_fiyat_degisim == "Evet":
        tek_f = st.number_input(f"Tek Kişilik Oda Fiyatı (Gün {gun+1})", min_value=0.0, key=f"tekf{gun}")
        cift_f = st.number_input(f"Çift Kişilik Oda Fiyatı (Gün {gun+1})", min_value=0.0, key=f"ciftf{gun}")
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
    g_etkinlikler = []
    g_sayisi = st.number_input(f"{gun+1}. gün kaç farklı etkinlik olacak?", min_value=1, value=1, step=1, key=f"eg{gun}")
    for j in range(g_sayisi):
        tur = st.selectbox(f"Etkinlik Türü {j+1} (Gün {gun+1})", options=etkinlik_turleri, key=f"t{gun}{j}")

        if etkinlik_farkli_mi and etkinlik_fiyat_degisim == "Evet":
            fiyat = st.number_input(f"{tur} Fiyatı (Gün {gun+1})", min_value=0.0, key=f"f{gun}{j}")
        else:
            fiyat = standart_etkinlik_fiyatlari[tur]

        kisi = st.number_input(f"{tur} Katılımcı Sayısı (Gün {gun+1})", min_value=0, key=f"k{gun}{j}")
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
        vergi = e_tutar * 0.20  # Şu an tüm etkinlikler için %20 vergi, istersen ileride tür bazlı değiştiririz
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
st.subheader("💳 Sözleşme Özeti")
st.write(f"*Şirket/Acenta:* {misafir_adi}")
st.write(f"*Konaklama Bedeli (KDV Hariç):* {vergisiz_konaklama:,.2f} EUR")
st.write(f"*Etkinlik Bedeli (KDV Hariç):* {vergisiz_etkinlik:,.2f} EUR")
st.write(f"*Toplam KDV:* {(vergi_konaklama + vergi_etkinlik):,.2f} EUR")
st.write(f"*Damga Vergisi:* {damga_vergisi:,.2f} EUR")
st.write(f"*Genel Toplam:* {toplam_tutar:,.2f} EUR")
st.write(f"### ✅ İlk Ödeme (30%): {ilk_odeme:,.2f} EUR")
st.write(f"### ✅ Kalan Ödeme (70%): {son_odeme:,.2f} EUR")

st.success("Teşekkür Ederiz!")
