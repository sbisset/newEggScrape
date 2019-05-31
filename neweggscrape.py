from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from pprint import pprint
import csv
import os
import smtplib
from email.message import EmailMessage

#Webscrape Newegg graphics cards
my_url = "https://www.newegg.com/global/uk-en/Video-Cards-Video-Devices/Category/ID-38?Tpk=graphics%20cards"
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

page_soup = soup(page_html, "html.parser")
contain = page_soup.findAll("div",{"class":"item-container"})
price = page_soup.findAll("li", {"class" : "price-current"} )

# CSV File Set up
graphic_name = "graphicscards.csv"
f = open(graphic_name, "w")
headers = "Brand, Price \n"

f.write(headers)
# Loop the scraped data and writes into csv
for i, items in enumerate(contain):   
    title = items.a.img["title"]
    pounds = price[i].strong.get_text()
    pence = price[i].sup.get_text()

    print (title)
    print("£",pounds,pence)

  
    # Replaces commas as it signals a new column and \n for new line after each loop
    f.write(title.replace(","," | ") + "," + "£" + pounds.replace(",","") + pence + "\n")
 
f.close()

#Email Send
EMAIL_PASSWORD = 'ENTER YOUR PASSWORD'
EMAIL_ADDRESS = 'ENTER YOUR EMAIL ' 
msg = EmailMessage()
msg['Subject'] = "Graphics cards"
msg['From'] = EMAIL_ADDRESS 
msg['To'] = EMAIL_ADDRESS
msg.set_content("Graphics Card and Prices doc")

with open('graphicscards.csv', 'rb') as attachment:
    file_data = attachment.read()
    attach_name = f.name
msg.add_attachment(file_data, maintype="csv", subtype="excell", filename=attach_name)

with smtplib.SMTP_SSL('smtp.gmail.com', 465 ) as smtp:
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD )
    smtp.send_message(msg)