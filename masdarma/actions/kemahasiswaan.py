import requests
# topik = 'lomba mahasiswa'


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
                        # print('Pencarian:', topik)
                        # print('KATEGORI:', json_data[y]['name'])
                        # print('JUDUL:', json_data_post[y]['title']['rendered'] )
                        # print('Link:', json_data_post[y]['link'])
                        # print('')
                        post = json_data_post[y]
                        kategori = json_data[y]
                        l_kategori.append(kategori)
                        l_post.append(post)
                
        format_add = [l_post, l_kategori]
        return format_add

    except UnboundLocalError:
        format_add = None
        
# post = Kemahasiswaan(topik)
# print(post[0][0]['title']['rendered'])
# print('')
# print(post[1][0]['name'])
# for x in range(0,len(post[0])):
#     print('Judul :', post[0][x]['title']['rendered'])
#     print('Kategori : ', post[1][x]['name'])