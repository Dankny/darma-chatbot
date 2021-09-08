# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
# from kemahasiswaan import Kemahasiswaan
# from baak import Berita_BAAK, Baak_Akademik
# from staffsite import Nama_Dosen
# from studentsite import berita_ss

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import html2text
import sys

#######################################################################################
import requests


def Kemahasiswaan(topik):
    try:
        api_address='https://kemahasiswaan.gunadarma.ac.id/wp-json/wp/v2/categories'
        hasil = []
        l_post = []
        l_kategori = []
        json_data = requests.get(api_address).json()

        for x in range(0, len(json_data)):
            api_address_post = json_data[x]['_links']['wp:post_type'][0]['href']
            json_data_post = requests.get(api_address_post).json()
            for y in range(0, len(json_data_post)):
                topik_pencarian = json_data_post[y]['title']['rendered']
                cari = topik_pencarian.lower()
                pencarian = topik.split()
                for kata in pencarian:
                    if kata.lower() in cari :

                        post = json_data_post[y]
                        kategori = json_data[y]
                        l_kategori.append(kategori)
                        l_post.append(post)
                
        format_add = [l_post, l_kategori]
        return format_add

    except UnboundLocalError:
        format_add = None
        


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

                            
                            format_data = [text_judul_fix, link_fix, tanggal_fix]
        
    return format_data



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
    

# judul = "tes aptitude"
def berita_ss(judul):
    cari = judul.lower().split()
    format_data = []

    url = 'https://studentsite.gunadarma.ac.id/index.php/site/news'
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, "html.parser")

    div_container = soup.find('div', attrs={"id":"content"})
    posts = div_container.find_all('div', attrs={"class":"content-box"})
    

    for post in posts:

        post_b = post.find_all("b")
        post_link = post.find_all('div', attrs={"align":"left"})
        post_tanggal = post.find_all('div', attrs={"class":"font-gray"})
        
        for post_b_ in post_b:
            post_b_text = post_b_.text.split()

            for kata in cari:
                for i in range(0, len(post_b_text)):
                    if kata == post_b_text[i].lower():
                        if post_b_.text not in format_data:
                            if int(post_tanggal[0].text[28:33]) >= 2020 :
                            
                                format_data.append(post_b_.text)
                                format_data.append('https://studentsite.gunadarma.ac.id'+ post_link[0].find_all('a')[0].get('href'))
                                format_data.append(post_tanggal[0].text)
                   
        
    if format_data == []:
        format_data.append('Berita tidak ditemukan.')
    return format_data



#######################################################################################



class ActionKemahasiswaan(Action):

    def name(self) -> Text:
        return "action_topik_kemahasiswaan"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("Berikut ini artikel yang bersumber \
            dari situs web [Kemahasiswaan Gunadarma](https://kemahasiswaan.gunadarma.ac.id) : ")
        topik = tracker.latest_message['text']
        post = Kemahasiswaan(topik)
        h = html2text.HTML2Text()
        try:
            for x in range(0,len(post[0])):
                judul = post[0][x]['title']['rendered']
                link = post[0][x]['link']
                tanggal = post[0][x]['date'].split('T')[0]
                konten = post[0][x]['content']['rendered']

                h.ignore_links = True
                soup = BeautifulSoup(konten, "html.parser")
                isi = h.handle(str(soup))

                dispatcher.utter_message(f"[{judul}]({link}) \
                                    \nTanggal  : {tanggal} ")
        except: 
            dispatcher.utter_message(f"Hmm, maaf ya sepertinya Darma tidak bisa akses situsnya. Coba beberapa saat lagi ya. ")
        return []


class ActionBeritaBaak(Action):

    def name(self) -> Text:
        return "action_berita_baak"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message("Berikut ini artikel berita yang bersumber \
            dari situs web [BAAK Gunadarma - Berita](https://baak.gunadarma.ac.id/berita) : ")
        topik = tracker.latest_message['text']
        post = Berita_BAAK(topik)

        try:
            for j in range(0, len(post[0])):
                judul = post[0][j]
                link = post[1][j]
                tanggal = post[2][j]

                dispatcher.utter_message(f"[{judul}]({link}) \
                                        \nTanggal  : {tanggal} ")
        except IndexError:
            dispatcher.utter_message(f"Hmm, maaf ya sepertinya Darma tidak bisa akses situsnya. Coba beberapa saat lagi ya. ")
        except :
            dispatcher.utter_message(f"Informasinya tidak ditemukan. Coba kata kunci lain ya! ")
        return []


class ActionBaakAkademik(Action):

    def name(self) -> Text:
        return "action_baak_akademik"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message("Berikut ini artikel yang bersumber \
            dari situs web [BAAK Gunadarma - Akademik](https://baak.gunadarma.ac.id/adminAkademik/1#undefined1) : ")
        topik = tracker.latest_message['text']
        post = Baak_Akademik(topik)

        try:
            for artikel in post:
                dispatcher.utter_message(f"{artikel}")
        except: 
            dispatcher.utter_message(f"Hmm, maaf ya sepertinya Darma tidak bisa akses situsnya. Coba beberapa saat lagi ya. ")
        return []

class ActionStaffsite(Action):

    def name(self) -> Text:
        return "action_staffsite"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message("Berikut ini hasil pencarian nama dosen \
            dari situs web [Staffsite](http://staffsite.gunadarma.ac.id/) : ")
        nama_input = tracker.latest_message['text']
        cari = Nama_Dosen(nama_input)

        # print(cari)
        detail = []
        l_nama = []
        try:
            if len(cari) > 1:
                
                for detail_dosen in cari:
                    nama = ''
                    hasil = [] 
                    if type(detail_dosen[0]) == list:
                        for j in range(0, len(detail_dosen[0])):
                            nama_list = detail_dosen[0][j]
                            nama = nama + nama_list + " "
                        l_nama.append(nama)
                    for i in range(1, len(detail_dosen)):  
                        hasil = hasil + [detail_dosen[i]]  
                    detail.append(hasil)
                        
            else:  
                nama = ''
                hasil = []
                if type(cari[0][0]) == list:
                    for j in range(0, len(cari[0][0])):
                        # nama_list = [ kata[0][j] for kata in cari if type(kata) == list]
                        nama_list = cari[0][0][j]
                        nama = nama + nama_list + " "
                    l_nama.append(nama)
                for i in range(1, len(cari[0])):    
                    hasil = hasil + [cari[0][i]]
                detail.append(hasil)
            
            if len(l_nama) > 1:
                count_nama = 0
                count_detail = 1

                for count in range(0, len(l_nama)):
                    nama = l_nama[count]
                    
                    if len(detail[count]) == 2:
                        email = detail[count][0]
                        homesite = detail[count][1]
                        dispatcher.utter_message(f"{nama} \
                                                \nEmail : {email} \
                                                \nHomesite : {homesite} ")
                    else:
                        email = detail[count][0]
                        dispatcher.utter_message(f"{nama} \
                                                \nEmail : {email} ")
                    count_detail += 1
                    
            elif len(l_nama) == 1: 
                if len(detail[0]) == 1:
                    dispatcher.utter_message(f"{l_nama[0]} \
                                        \nEmail  : {detail[0][0]}")
                else: 
                    dispatcher.utter_message(f"{l_nama[0]} \
                                        \nEmail  : {detail[0][0]} \
                                        \nHomesite : {detail[0][1]}")
            else:
                dispatcher.utter_message(f"{cari} ")
        except IndexError:
            dispatcher.utter_message(f"Nama tidak ditemukan, mungkin kamu bisa langsung cek ke situs [Staffsite](http://staffsite.gunadarma.ac.id/).")
        except: 
            dispatcher.utter_message(f"Hmm, maaf ya sepertinya Darma tidak bisa akses situsnya. Coba beberapa saat lagi ya. ")
        return []


class ActionBeritaStudentsite(Action):

    def name(self) -> Text:
        return "action_studentsite"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message("Berikut ini artikel yang bersumber \
            dari situs web [Studentsite](https://studentsite.gunadarma.ac.id/index.php/site/news) : ")
        judul = tracker.latest_message['text']
        post = berita_ss(judul)

        try:
            if len(post) > 1:
                for a in range(0, len(post), 3):
                    judul = post[a]
                    link = post[a+1]
                    tanggal = post[a+2]
                    dispatcher.utter_message(f"[{judul}]({link}) \
                                        \n{tanggal}")

            else:
                for a in post:
                    dispatcher.utter_message(f"{a}")

        except: 
            dispatcher.utter_message(f"Hmm, maaf ya sepertinya Darma tidak bisa akses situsnya. Coba beberapa saat lagi ya. ")
        return []

# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
