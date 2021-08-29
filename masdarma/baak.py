from bs4 import BeautifulSoup
import re
import requests
import html2text


def Berita_BAAK(topik):
    format_data = []
    text_judul_fix = []
    link_fix = []
    tanggal_fix = []
    cari = topik.lower().split()

    for i in range(0, 6):
        text_judul = []
        link = []
        tanggal = []
        
        url='https://baak.gunadarma.ac.id/berita?sort=votes&page=' + str(i)

        html_content = requests.get(url).text
        soup = BeautifulSoup(html_content, "html.parser")

        div_judul = soup.find('div', attrs={"class": "range text-sm-left range-xs-center"})
        judul = div_judul.find_all("h6")
        tgl = div_judul.find_all("span")
        # print(tgl)
        
        for i in range(0, len(judul)):
            for teks in judul[i].find_all("a"):
                text_judul.append(teks.text)
                link.append(teks.get("href"))
                
                for teks_tgl in tgl:
                    if teks_tgl.text != "" :
                        tanggal.append(teks_tgl.text)
            # print(teks.text)
            # print(teks.get("href"))
            # print(teks_tgl.text)
            
        # print(link)
        # print(tanggal)
        # print(text_judul)
        # print(link)
        # print(tanggal)

        for title in text_judul:
            index = text_judul.index(title)
            jdl = title.lower().split()

            for kata in cari:
                for z in range(0, len(jdl)):
                    if kata == jdl[z] :
                        if text_judul[index] not in text_judul_fix:
                            # print(text_judul[index])
                            # print(text_judul_fix)
                            text_judul_fix.append(text_judul[index])
                            link_fix.append(link[index])
                            tanggal_fix.append(tanggal[index])

                            # print('Judul : ', text_judul[index])
                            # print('Link : ', link[index])
                            # print('Tanggal : ', tanggal[index])
                            # print('')
                            
                            format_data = [text_judul_fix, link_fix, tanggal_fix]
        
    return format_data

# topik ='prosedur team teaching'
# hasil = Berita_BAAK(topik)
# print(hasil)
# for j in range(0, len(hasil[0])):
#     print(f'Judul : {hasil[0][j]} \
#             \nLink : {hasil[1][j]} \
#             \nTanggal : {hasil[2][j]} \n')



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
           
    return format_data
    

# tes = Baak_Akademik('cuti kuliah')

# for teks in tes:
#     print(teks)


