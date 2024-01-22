#pip install streamlit

#%%writefile deneme.py

import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd


#streamlit.config.theme.base = "dark"
st.title("Hocalar Hisse Hesaplıyor  :chart:")
st.subheader("Road to Kıbrıs :airplane_departure: :sunglasses:")
#st.set_page_config(
# page_title="Hisse Hedef Fiyat Hesaplayıcı",
#  page_icon="https://example.com/icon.png",
#  layout="centered",
#)



# Kullanıcıdan hisse senedi adı almak için input fonksiyonu kullanın
#hisse_adi = input("Hisse Adı : ").upper()
hisse_input = st.text_input("Hisse Adı (Sadece Borsadaki Kısaltma Adını Girin):").upper()
hisse_adi = hisse_input

# hisse_adi değişkenini url1 değişkeninde hisse parametresine atayın
url1="https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/sirket-karti.aspx?hisse="+hisse_adi

# web sitesinden yıl ve dönem bilgilerini çekmek için BeautifulSoup kullanın
r1=requests.get(url1)
s1=BeautifulSoup(r1.text, "html.parser")
secim=s1.find("select", id="ddlMaliTabloFirst")
secim2=s1.find("select", id="ddlMaliTabloGroup")

#print(secim2)

# yıl ve dönem bilgilerini listelere atayın
grup=[]
tarihler=[]
yıllar=[]
donemler=[]

# try to find the elements with BeautifulSoup
try:
  cocuklar=secim.findChildren("option")
  grup=secim2.find("option")["value"]


  for i in cocuklar:
    tarihler.append(i.string.rsplit("/"))

  for j in tarihler:
    yıllar.append(j[0])
    donemler.append(j[1])


  if len(tarihler)>=4:
    # parametreler değişkenini oluşturun
    parametreler=(
        ("companyCode",hisse_adi),
        ("exchange","TRY"),
        ("financialGroup",grup),
        ("year1",yıllar[0]),
        ("period1",donemler[0]),
        ("year2",yıllar[1]),
        ("period2",donemler[1]),
        ("year3",yıllar[2]),
        ("period3",donemler[2]),
        ("year4",yıllar[3]),
        ("period4",donemler[3])
    )
    #print(tarihler)
    # web servisine istek gönderin ve veriyi alın
    url2="https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo"
    r2= requests.get(url2,params=parametreler).json()["value"]

    # veriyi bir veri çerçevesine dönüştürün
    veri=pd.DataFrame.from_dict(r2)

    # gereksiz sütunları kaldırın
    veri.drop(columns=["itemCode","itemDescEng"],inplace=True)
    # Select the first row by its index
    Ozkaynaklar =  veri[veri['itemDescTr'] == 'Özkaynaklar']
    ozkaynaklar1 = Ozkaynaklar.iloc[0,1]
    OdenmisSermaye = veri[veri['itemDescTr'] == '  Ödenmiş Sermaye']
    OdenmisSermaye = OdenmisSermaye.iloc[0,1]
    NetDonemKarı = veri[veri['itemDescTr'] == 'DÖNEM KARI (ZARARI)']
    NetDonemKarı = NetDonemKarı.iloc[0,1]

    #print("Özkaynaklar:", ozkaynaklar1)
    #print("Ödenmiş Sermaye:", OdenmisSermaye)
    ###print(f"Özkaynaklar: {float(ozkaynaklar1):,.2f}") # comma and dot separators
    ###print(f"Ödenmiş Sermaye: {float(OdenmisSermaye):,.2f}")

# Print the desired data
    #print(ozkaynaklar)
    #print(OdenmisSermaye)
    # veriyi ekrana yazdırın
    #print(veri)

except AttributeError:
  # print a message
  print("An AttributeError occurred")
  # skip the iteration
  #continue

### KODUN 2. KISMI BURADAN BAŞLIYOR

# URL for the initial page
url = "https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/Temel-Degerler-Ve-Oranlar.aspx?"

# Fetch the initial page content
response = requests.get(url)
temeldegerler = BeautifulSoup(response.text, "html.parser")

# Find the tables containing the stock data
table = temeldegerler.find("tbody", id="temelTBody_Ozet")
f_oranlar = temeldegerler.find("tbody", id="temelTBody_Finansal")

sektorkodu = temeldegerler.find("select", id="ddlSektor")

# Create dictionaries to store stock information
hisse_sektor = {}
hisse_oran = {}
sektor_numara = {}

# Iterate over the first table to extract stock names and sectors
for row in table.find_all("tr"):
    cells = row.find_all("td")
    hisse = cells[0].find("a").text.upper()
    sektor = cells[2].text
    hisse_sektor[hisse] = sektor
    ###sektor_output = hisse_sektor[hisse_input]

# Iterate over the options in the select element
for option in sektorkodu.find_all("option"):
    # Get the sector row number
    sektor_numarasi = option["value"]
    # Get the sector name
    sektor_ismi  = option.text
    # Add the pair to the dictionary
    sektor_numara[sektor_ismi] = sektor_numarasi

# Iterate over the second table to extract financial ratios
for r in f_oranlar.find_all("tr"):
    hucre = r.find_all("td")
    hisse_adi_1 = hucre[0].find("a").text.upper()
    kapanıs = hucre[1].text
    #c3 = float(kapanıs)
    f_k = hucre[2].text
    #c10 = float(fk_value)
    pd_dd = hucre[5].text
    #c11 = float(pd_value)
    hisse_oran[hisse_adi_1] = {"kapanıs": kapanıs, "f_k": f_k, "pd_dd": pd_dd}

# Get the stock name from the user
stock_name = hisse_adi #input("Hisse Adı Giriniz: ").upper()

if stock_name:
    # Check if the input is in the dictionary
    if stock_name in hisse_sektor:
        # Get the sector name from the dictionary
        sektor_output = hisse_sektor[stock_name]
        # Display the sector name
        st.write("**SEKTÖR ALANI:**",  sektor_output)
        #print("Sektör Alanı:", sektor_output)
        # Get the sector row number from the dictionary
        sektor_numarasi = sektor_numara[sektor_output]
        # Add the sector row number to the url
        url = "https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/Temel-Degerler-Ve-Oranlar.aspx?sektor="+sektor_numarasi
        # Make a new request with the updated url
        response = requests.get(url)
        temeldegerler = BeautifulSoup(response.text, "html.parser")

# Check if the stock exists in the dictionary
if stock_name in hisse_oran:
    try:
        # Access the stock data and extract the F/K value
        kapanıs = hisse_oran[stock_name]["kapanıs"].replace(",", ".")
        fk_value = hisse_oran[stock_name]["f_k"].replace(",", ".")  # Format with dots as decimal separators
        pd_value = hisse_oran[stock_name]["pd_dd"].replace(",", ".")
        st.write(f"**HİSSE FİYATI:**  {kapanıs}", box = True)
        st.write(f"**HİSSE F/K ORANI:**  {fk_value}", box = True)
        st.write(f"**HİSSE PD/DD ORANI:**  {pd_value}", box = True)
                #print(f"{stock_name} Hisse Fiyatı: {kapanıs}")
        #print(f"{stock_name} F/K Oranı:  {fk_value}")
        #print(f"{stock_name} PD/DD Oranı:  {pd_value}")
        st.write(f"**ÖZKAYNAKLAR:**  {float(ozkaynaklar1):,.2f}", box = True)
        st.write(f"**ÖDENMİŞ SERMAYE:**  {float(OdenmisSermaye):,.2f}", box = True)
        st.write(f"**NET DÖNEM KARI:**  {float(NetDonemKarı):,.2f}", box = True)
    except KeyError:
        #print("Hisse bulunamadı.") # Stock not found in the dictionary
        st.write("Hisse bulunamadı.")
else:
    #print("Bir sorun var!")  # Stock not found in any of the dictionaries
    st.write("İşlem yapılıyor!")

st.write(" Sektör Ortalamaları için Tıklayın: [link](https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/Temel-Degerler-Ve-Oranlar.aspx?#page-5)")

#import streamlit_tags as tags

#st.write("Hisse Hedef Fiyat Hesaplayıcı")

# Hisse Fiyatı
#c3 = st.number_input("Hisse Fiyatı:" )
c3 = float(kapanıs)
#if stock_name in hisse_oran:
  #try:
    # Access the stock data and extract the F/K value
    #kapanıs = hisse_oran[stock_name]["kapanıs"]
    #c3 = float(kapanıs)
 # except KeyError:
    #print("Hisse bulunamadı.") # Stock not found in the dictionary
    #st.write("Hisse bulunamadı.")
#else:
  #print("Bir sorun var!") # Stock not found in any of the dictionaries
 # st.write("İşlem yapılıyor!")

# Hisse F/K Oranı
#if stock_name in hisse_oran:
 # try:
    # Access the stock data and extract the F/K value
   # fk_value = hisse_oran[stock_name]["f_k"].replace(",", ".")  
  #  c10 = float(fk_value)
#  except KeyError:
    #print("Hisse bulunamadı.") # Stock not found in the dictionary
   # st.write("Hisse bulunamadı.")
#else:
  #print("Bir sorun var!") # Stock not found in any of the dictionaries
 # st.write()
#c10 = float(st.number_input("Hisse F/K Oranı:"))
c10 = float(fk_value)
if c10 <= 0:
  st.write("F/K Değeri Bulunmamaktadır!")

# HİSSE PD/DD ORANI
#if stock_name in hisse_oran:
 # try:
    # Access the stock data and extract the F/K value
   # pd_value = hisse_oran[stock_name]["pd_dd"].replace(",", ".")
  #  c11 = float(pd_value)
#  except KeyError:
    #print("Hisse bulunamadı.") # Stock not found in the dictionary
 #   st.write("Hisse bulunamadı.")
#else:
  #print("Bir sorun var!") # Stock not found in any of the dictionaries
#  st.write()
#c11 = st.number_input("Hisse PD/DD Oranı: ")
c11 = float(pd_value)

# BİST100 /SEKTÖR GÜNCEL F/K ORANI
c12 = float(st.number_input("BİST100 / Sektör Güncel F/K Oranı: "))

# BIST100 / Sektör Güncel P/D Oranı
c13 = float(st.number_input("BİST100 / Sektör Güncel PD/DD Oranı:"))

# Ödenmiş Sermaye
#c4 = st.number_input("Ödenmiş Sermaye: ")
c4 = float(OdenmisSermaye)
#c4 = float({(OdenmisSermaye):,.2f})
st.write("Ödenmiş Sermaye:" c4)

# Yıllık Net Kar
#c7 = st.number_input("Yıllık Net Kar: ")
C7 = float(NetDonemKarı)

# Özsermaye
#c8 = st.number_input("Özsermaye : ")
c8 = float(ozkaynaklar1)

# Güncel Piyasa Değeri
#c9 = st.number_input("Güncel Piyasa Değeri: ")


st.write("**HİSSE HEDEF FİYAT HESAPLAYICI**")

operation = st.selectbox("İşlem Seçimi:", ["F/K Hedef Fiyat", "P/D Hedef Fiyat", "ÖDENMİŞ SERMAYEYE GÖRE HEDEF FİYAT", "ÖZSERMAYE KARLILIĞINA GÖRE HEDEF FİYAT"])

# Calculate the target price based on the selected operation
if operation == "F/K Hedef Fiyat":
  if c10 != 0:
    fk_hedef_fiyat = c3 / c10 * c12
  else:
    fk_hedef_fiyat = 0

elif operation == "P/D Hedef Fiyat":
  if c11 != 0:
    pd_hedef_fiyat = c3 / c11 * c13
  else:
    pd_hedef_fiyat = 0

elif operation == "ÖDENMİŞ SERMAYEYE GÖRE HEDEF FİYAT":
  if c4 != 0:
    odenmis_hedef_fiyat = (c7 / c4) * c10
  else:
    odenmis_hedef_fiyat = 0

# Print the result of the selection
if operation == "F/K Hedef Fiyat":
  st.write(f"**F/K HEDEF FİYAT:** {fk_hedef_fiyat:,.2f}")

elif operation == "P/D Hedef Fiyat":
  st.write(f"**P/D HEDEF FİYAT:** {pd_hedef_fiyat:,.2f}")

elif operation == "ÖDENMİŞ SERMAYEYE GÖRE HEDEF FİYAT":
  st.write(f"ÖDENMİŞ SERMAYEYE GÖRE HEDEF FİYAT: {odenmis_hedef_fiyat:,.2f}")

elif operation == "ÖZSERMAYE KARLILIĞINA GÖRE HEDEF FİYAT":
  if c10 != 0:
    ozsermaye_hf = (c7/c8)*10/c11*c3
    st.write(f"ÖZSERMAYE KARLILIĞINA GÖRE HEDEF FİYAT: {ozsermaye_hf:,.2f}")

#if __name__ == "__main__":
#  st.run()


#!streamlit run deneme.py & npx localtunnel --port 8501
