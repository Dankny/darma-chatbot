import requests
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
topik = 'kip'.lower()
cari = []
intent_bersih = []
factory = StopWordRemoverFactory()
stopword = factory.create_stop_word_remover()


def Kemahasiswaan(topik):
    api_address='https://kemahasiswaan.gunadarma.ac.id/wp-json/wp/v2/categories'

    json_data = requests.get(api_address).json()

    for x in range(0, len(json_data)):
        api_address_post = json_data[x]['_links']['wp:post_type'][0]['href']
        json_data_post = requests.get(api_address_post).json()
        for y in range(0, len(json_data_post)):
            topik_pencarian = json_data_post[y]['title']['rendered'].lower()
            stop = stopword.remove(topik_pencarian)          
            cari.append(stop)
    
    for z in range(0, len(cari)):
        intent = cari[z]
        print(intent)
        intent_bersih.extend(intent)

    return print()
         
Kemahasiswaan(topik)