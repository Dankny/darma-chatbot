# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from kemahasiswaan import Kemahasiswaan
from baak import Berita_BAAK, Baak_Akademik
from staffsite import Nama_Dosen
from studentsite import berita_ss

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import html2text
import sys


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
