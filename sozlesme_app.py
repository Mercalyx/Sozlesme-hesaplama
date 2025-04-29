import streamlit as st

st.title("Sözleşme Tutarı Hesaplama Aracı")

misafir_adi = st.text_input("Misafir Adı", "")
Tursab = st.radio("TÜRSAB Üyesi mi?", ["Evet", "Hayır"])
gun_sayisi = st.number_input("Toplam Gün Sayısı", min_value=1, max_value=10, value=3)
ozel_gunler = st.checkbox("Her gün farklı oda ve etkinlik bilgileri olacak mı?")

oda_verileri = []
etkinlik_verileri = []

for i in range(gun_sayisi):
    st.markdown(f"### \U0001F4C5 Gün {i+1}")

    if ozel_gunler:
        tek_kisi = st.number_input(f"{i+1}. Gün Tek Kişilik Oda Sayısı", key=f"tk_{i}")
        tek_fiyat = st.number_input(f"{i+1}. Gün Tek Kişilik Fiyat", key=f"tf_{i}")
        cift_kisi = st.number_input(f"{i+1}. Gün Çift Kişilik Oda Sayısı", key=f"ck_{i}")
        cift_fiyat = st.number_input(f"{i+1}. Gün Çift Kişilik Fiyat", key=f"cf_{i}")
        oda_verileri.append({"tek": tek_kisi, "tek_f": tek_fiyat, "cift": cift_kisi, "cift_f": cift_fiyat})

        katilimci = st.number_input(f"{i+1}. Gün Katılımcı Sayısı", key=f"k_{i}")
        etkinlik_turu = st.selectbox(f"{i+1}. Gün Etkinlik Türü", ["Toplantı", "Gala", "Öğle Yemeği"], key=f"e_{i}")
        etkinlik_fiyat = st.number_input(f"{i+1}. Gün {etkinlik_turu} Fiyatı", key=f"ef_{i}")
        etkinlik_verileri.append({"katilimci": katilimci, "tur": etkinlik_turu, "fiyat": etkinlik_fiyat})
    else:
        if i == 0:
            tek_kisi = st.number_input("Tek Kişilik Oda Sayısı", key="tk")
            tek_fiyat = st.number_input("Tek Kişilik Fiyat", key="tf")
            cift_kisi = st.number_input("Çift Kişilik Oda Sayısı", key="ck")
            cift_fiyat = st.number_input("Çift Kişilik Fiyat", key="cf")
            katilimci = st.number_input("Katılımcı Sayısı", key="kat")
            etkinlik_turu = st.selectbox("Etkinlik Türü", ["Toplantı", "Gala", "Öğle Yemeği"], key="tur")
            etkinlik_fiyat = st.number_input(f"{etkinlik_turu} Fiyatı", key="fiyat")

        oda_verileri.append({"tek": tek_kisi, "tek_f": tek_fiyat, "cift": cift_kisi, "cift_f": cift_fiyat})
        etkinlik_verileri.append({"katilimci": katilimci, "tur": etkinlik_turu, "fiyat": etkinlik_fiyat})

if st.button("Hesapla"):
    toplam_oda = 0
    toplam_etkinlik = 0

    for i in range(gun_sayisi):
        gun_oda = oda_verileri[i]["tek"] * oda_verileri[i]["tek_f"] + \
                  oda_verileri[i]["cift"] * oda_verileri[i]["cift_f"]
        gun_etkinlik = etkinlik_verileri[i]["katilimci"] * etkinlik_verileri[i]["fiyat"]
        toplam_oda += gun_oda
        toplam_etkinlik += gun_etkinlik

    vergi = toplam_oda * 0.12 + toplam_etkinlik * 0.20
    vergili_toplam = toplam_oda * 1.12 + toplam_etkinlik * 1.20

    if Tursab == "Evet":
        damga_vergisi = 3783.20 / 82 + toplam_etkinlik * 0.00948 / 2
    else:
        damga_vergisi = (toplam_oda + toplam_etkinlik) * 0.00948 / 2

    toplam = vergili_toplam + damga_vergisi
    ilk_odeme = toplam * 0.30
    son_odeme = toplam * 0.70

    st.markdown("### \U0001F4B3 Sözleşme Özeti")
    st.write(f"**Şirket/Acenta:** {misafir_adi}")
    st.write(f"**KDV Hariç Oda Bedeli:** {toplam_oda:,.2f} EUR")
    st.write(f"**KDV Hariç Etkinlik Bedeli:** {toplam_etkinlik:,.2f} EUR")
    st.write(f"**Toplam KDV:** {vergi:,.2f} EUR")
    st.write(f"**Damga Vergisi:** {damga_vergisi:,.2f} EUR")
    st.write(f"**KDV Dahil Ara Toplam:** {vergili_toplam:,.2f} EUR")
    st.write(f"**Genel Toplam:** {toplam:,.2f} EUR")
    st.write(f"### ✅ İlk Ödeme: {ilk_odeme:,.2f} EUR")
    st.write(f"### ✅ Son Ödeme: {son_odeme:,.2f} EUR")
    st.success("Teşekkür Ederiz!")
