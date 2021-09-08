from bs4 import BeautifulSoup
import re
import requests


def Nama_Dosen(nama):
    format_data=[]
    list_nama = []

    
    url = 'http://staffsite.gunadarma.ac.id/index2.php'
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, "html.parser")

    div_tabel = soup.find('table', attrs={"width": "80%"})
    tr = div_tabel.find_all("tr")

    for i in range(0, len(tr)):
        mencari = tr[i].find_all("td")
        for teks in mencari:
            
            nama_split = teks.text.split()
            email_homesite = teks.find_all("a")

            list_detil = [nama_split]
            
            for e_h in email_homesite:
                for huruf in e_h:
                    isi = e_h.get("href")
                    if 'email' in huruf:
                        list_detil.append(isi)
                    if 'homesite' in huruf:
                        list_detil.append(isi)
        list_nama.append(list_detil)
        # print(list_nama.index(list_detil))
        

    for rem in range(0, len(list_nama)):
        
        try:
            while rem <= len(list_nama):
               
                if not list_nama[rem][0]:
                    list_nama.remove([[]])
                if list_nama[rem][0] == ['top']:
                    list_nama.remove([['top']])
                if len(list_nama[rem][0]) == 1:
                    list_nama.remove(list_nama[rem])
                if not list_nama[rem][0]:
                    list_nama.remove([[]])
                if list_nama[rem][0] == ['top']:
                    list_nama.remove([['top']])
                if len(list_nama[rem][0]) == 1:
                    list_nama.remove(list_nama[rem])
                if not list_nama[rem][0]:
                    list_nama.remove([[]])
                

                pencarian = list_nama[rem][0]
                
                nama_cari = nama.lower().split()
                n = 0
                for detil in pencarian:
                    nama_pencarian = detil.lower().split(',')
                    for nm in nama_cari:
                        for z in range(0, len(nama_pencarian)):
                           
                            if nm == nama_pencarian[z].replace(',', '') or nm == nama_pencarian[z].replace('.', ''):
                                calon_format_data = []
                                if '[email]' in pencarian :
                                    pencarian.remove('[email]')
                                if '[homesite]' in pencarian:
                                    pencarian.remove('[homesite]')

                                calon_format_data.append(pencarian)
                                # print(pencarian)
                                calon_format_data.append(list_nama[rem][1])                            
                                if len(list_nama[rem]) == 3:
                                    calon_format_data.append(list_nama[rem][2])
                                if calon_format_data not in format_data:
                                    format_data.append(calon_format_data)

                            elif nm != nama_pencarian[z]:
                                continue
                    

                rem = rem + 1
        except AttributeError:
            format_data = "Maaf, website Staffsite sedang tidak dapat diakses. Cobalah tanyakan kembali beberapa saat lagi ya."
        except IndexError:
            break
        
    return format_data

# tes = Nama_Dosen('pak ary bima')

# if len(tes) > 1:
#     for a in range(0, len(tes)-1):
#         for detail_dosen in tes:
#             if type(detail_dosen[0]) == list:
#                 for j in range(0, len(detail_dosen[0])):
#                     print(detail_dosen[0][j], end=' ')
#             print()
#             for i in range(1, len(detail_dosen)):    
#                 print(detail_dosen[i])
#             print()
# else: 
#     if type(tes[0][0]) == list:
#         for j in range(0, len(tes[0][0])):
#             print(tes[0][0][j], end=' ')
#     print()
#     for i in range(1, len(tes[0])):    
#         print(tes[0][i])
#     print()



