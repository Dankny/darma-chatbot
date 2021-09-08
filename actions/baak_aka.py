from bs4 import BeautifulSoup
import re
import requests
import html2text

def Baak_Akademik(judul):
    cari = judul.lower().split()

    url = 'https://baak.gunadarma.ac.id/adminAkademik/2#undefined1'
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, "html.parser")

    div_tab = soup.find('div', attrs={"class": "resp-tabs-container text-sm-left tabs-lg-collapsed"})
    post = div_tab.find_all("h4")

    h = html2text.HTML2Text()
    temp = []
    format_data = []
    artikel = div_tab.find_all(attrs={'class':'inset-lg-left-60'})
    
    for i in range(0, len(artikel)):
        teks_artikel = h.handle(str(artikel[i].prettify()))
        temp.append(teks_artikel)

    count = 0 
    index = 0
    
    for sementara in temp:
        judul_teks = sementara[0:32].split()
        
        index = temp.index(sementara)
        teks_artikel = h.handle(str(artikel[index].prettify()))
        for kata in cari:
            for j in range(0, len(judul_teks)):
                if kata == judul_teks[j].lower():
                    # print(sementara)
                    if sementara not in format_data:
                        format_data.append(teks_artikel)
        count += 1
            
    return format_data
    

# tes = Baak_Akademik('cuti kuliah')

# for teks in tes:
#     print(teks)

