import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import smtplib, ssl
import email.message
from datetime import date

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
             'Accept-Language': 'en-US, en;q=0.5'})


def price_parse(price_raw):
    price_raw = price_raw.replace('.', ',')
    price = ''.join(price_raw.split(','))
    price = float(price)
    return price

def send_email(email_message = ""):
    port = 465
    #Enter password for sender email id. I generated a third party app password from a yahoo email id
    password = ''
    #Enter the sender email id
    sender_email = ''
    #Enter the receiver email id
    receiver_email = ''

    m = email.message.Message()
    today = date.today()

    date_today = today.strftime("%b-%d-%Y")
    
    m['From'] = sender_email
    m['To'] = receiver_email
    m['Subject'] = f"Amazon Wishlist on {date_today}"
    m.set_payload(email_message);
    message = m.as_string()

    # Create a secure SSL context
    context = ssl.create_default_context()

    #first parameter can be smpt.gmail.com also, depending on the sender's email server
    with smtplib.SMTP_SSL("smtp.mail.yahoo.com", port,context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message) 
        

def search_product_list():
    #Enter the path to the Wishlist
    prods = pd.read_csv('D:\Amazon_Price_Tracker\Amazon_Price_Tracker_Code\Wishlist.csv', sep=';')
    prod_URLS = prods["url"]
    tracker_log = pd.DataFrame()
    now = datetime.now().strftime('%Y-%m-%d %Hh%Mm')
    list_of_items = []
    for x, url in enumerate(prod_URLS):
            
            page = requests.get(url, headers=HEADERS)
            soup = BeautifulSoup(page.content, features="lxml")
            
            
            title = soup.find(id='productTitle').get_text().strip()
            availability = soup.find(id='availability').find('span').get_text().strip()
            
            available = True
            if availability == 'Currently unavailable.' or availability == '':
                available = False
    
            if available == True:
                price_raw = soup.find(id='corePriceDisplay_desktop_feature_div').find(class_="a-price-whole").get_text().strip()
                price = price_parse(price_raw)
            else:
                price = ''
            
            
            log = pd.DataFrame({'date': [now.replace('h',':').replace('m','')],
                                'code': prods.code[x], # this code comes from the TRACKER_PRODUCTS file
                                'url': url,
                                'title': title,
                                'buy_below': prods.buy_below[x], # this price comes from the TRACKER_PRODUCTS file
                                'price': price,
                               })
            
            if available and price <= prods.buy_below[x]:
                list_of_items.append(f"{prods.code[x]} is available at {price} with given buy under {prods.buy_below[x]}")
                
            
            tracker_log = pd.concat([tracker_log, log])
    
    #Enter path to the search history file
    search_hist = pd.read_excel('D:\Amazon_Price_Tracker\Amazon_Price_Tracker_Code\Search_History.xlsx')
    final_df = pd.concat([search_hist, tracker_log], sort=False)
    #final_df = search_hist.append(tracker_log, sort=False)
    final_df.to_excel('D:\Amazon_Price_Tracker\Amazon_Price_Tracker_Code\Search_History.xlsx', index=False)

    if len(list_of_items) > 0:
        email_message = '\n'.join(list_of_items)
        send_email(email_message)


if __name__ == '__main__':
    search_product_list()

            
    