from bs4 import BeautifulSoup
import re
import requests

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

# tes = berita_ss(judul)

# if len(tes) > 1:
#     for a in range(0, len(tes), 3):
#         print(tes[a])
#         print(tes[a+1])
#         print(tes[a+2])
#         print('')
# else:
#     for a in tes:
#         print(a)


