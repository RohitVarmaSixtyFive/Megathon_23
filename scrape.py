#!/bin/python3
import requests
from bs4 import BeautifulSoup
import certifi

# Path to the CA certificates (you need to provide the actual path)
# ca_certificates_path = certifi.where()

profile_url = input('>')

f = open('scraped_data.txt', 'w')

cookie_strings = 'lang=v=2&lang=en-us; bcookie="v=2&3bd75170-6a43-4697-850d-99fc0267e71a"; bscookie="v=1&20230803201825576bec9b-2631-4217-8f68-6fcc1516a6ceAQEMb1QYzxcnroEXXgdf5wi6TQYjkM9u"; JSESSIONID=ajax:0943570843674297750; fid=AQEVfncOKT_f6QAAAYm_qzC19C5bXchfP3DsKwsWQCne8Fc4XroDkxi6FfU4wW4pVw-6nnSefm95DQ; lidc="b=TGST08:s=T:r=T:a=T:p=T:g=2570:u=1:x=1:i=1691399797:t=1691486197:v=2:sig=AQHhryiI3gvjBSCA_BgBerSSA4jPorLF"; fcookie=AQEGIWM3v7wsSAAAAYnQOmapZ4wgt7r6rUT5h3izKUUayAGxcrC6crXkA7pZ4RNAJayHaA4G3zMtVyGXbeADHzTglPwlw40_2S5-KOSapI4u_-VvYGBMsXcekPtQ86WuSiRo11iWT0Z3e8hYsioh7A0rdlHge5YUHAfFr3tuvvEjxGFln8EFBe7Tzr8cSGMHlEXT56AexKDCYsBb1q0yGrvumGRAuKNuGkfEA22WCkBgml2cIsDszX6r5wZVHZ2vhLDDiUXDf2bE2WeZ35ERTAz7AUYIKD4q2XTMpidAjVsRJqp7sCmftU7a6djCbkRWaKCP6OS+7qMbZhmz9BuzMQ==; g_state={"i_p":1691422839742,"i_l":1}; fid=AQFZ_EZlhT2_SwAAAYnQOoceTschZlcQcuOgysDASdKVYcnAtBcwx6h-GKFvM_vd1YpOpv1z0U50lA'


headers = {
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'Connection':'keep-alive',
  'accept-encoding': 'gzip, deflate, br',
  'Referer':'http://www.linkedin.com/',
  'accept-language': 'en-US,en;q=0.9',
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
  'Cookie': cookie_strings
}

response = requests.get(profile_url, verify=True, headers=headers)

if response.status_code == 200:
    #    Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
#with open('scrape.txt', 'r', encoding='utf-8') as file:
#    file_contents = file.read()
else:
    print(response)
    exit(1)


#soup = BeautifulSoup(file_contents, 'html.parser')

name = soup.find("h1", {"class": "top-card-layout__title font-sans text-lg papabear:text-xl font-bold leading-open text-color-text mb-0"})

if name:
    # Find the inner div structure containing the span element
    print("Name", file=f)
    print(name.text.strip(), file=f)
else:
    print("Outer div element not found in the HTML.")
    exit(1)

descr = soup.find("h2", {"class": "top-card-layout__headline break-words font-sans text-md leading-open text-color-text"})

if descr:
    # Find the inner div structure containing the span element
    print("Description", file=f)
    print(descr.text.strip(), file=f)
else:
    print("Outer div element not found in the HTML.")
    exit(1)

descr = soup.find_all("h3", {"class": "base-main-card__title font-sans text-[18px] font-bold text-color-text overflow-hidden"})

for temp in descr:
    print(temp.text.strip(), file=f)

try:
    exp = soup.find("section", {"class": "core-section-container my-3 core-section-container--with-border border-b-1 border-solid border-color-border-faint m-0 py-3 pp-section experience"})
    pos = exp.find_all("h3", {"class": "profile-section-card__title"})
    org = exp.find_all("h4", {"class": "profile-section-card__subtitle"})

    print("Experience:", file=f)


    if len(pos) == len(org):
        for i, (position, organization) in enumerate(zip(pos, org)):
            print(f"Position {i + 1}: {position.text.strip()}", file=f)
            print(f"Organization {i + 1}: {organization.text.strip()}", file=f)
    else:
        print("Mismatch in the number of positions and organizations found.")
except:
    pass


try:
    educ = soup.find("section", {"class": "core-section-container my-3 core-section-container--with-border border-b-1 border-solid border-color-border-faint m-0 py-3 pp-section education"})

    pos = educ.find_all("h3", {"class": "profile-section-card__title"})
    org = educ.find_all("h4", {"class": "profile-section-card__subtitle"})

    print("Education:", file=f)

    if len(pos) == len(org):
        for i, (position, organization) in enumerate(zip(pos, org)):
            print(f"University {i + 1}: {position.text.strip()}", file=f)
            print(f"Degree {i + 1}:\n {organization.text.strip()}", file=f)
    else:
        print("Mismatch in the number of positions and organizations found.")
except:
    pass

try:
    pub = soup.find("section", {"class": "core-section-container my-3 core-section-container--with-border border-b-1 border-solid border-color-border-faint m-0 py-3 pp-section publications"})

    pos = pub.find_all("h3", {"class": "[&amp;&gt;*]:mb-0 text-[18px] text-color-text leading-regular group-hover:underline font-semibold"})
    org = pub.find_all("p", {"class": "show-more-less-text__text--less"})

    if len(pos) == len(org):
        for i, (position, organization) in enumerate(zip(pos, org)):
            print(f"University {i + 1}: {position.text}", file=f)
            print(f"Degree {i + 1}:\n {organization.text}", file=f)
    else:
        print("Mismatch in the number of positions and organizations found.")
except:
    pass

f.close()
