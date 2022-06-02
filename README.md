# Amazon-Price-Tracker
A script that can track prices of your desired products on Amazon, checks if it is available, and sends you email alerts when the price for an individual item drops below an amount specified by you.

The script uses BeautifulSoup for scraping the relevant data and smtplib, ssl and email modules to send the email. Every time the script is run, it appends relevant information to the Search_History.xlsx file.

To use the script:

1) Set up a virtual environment and install the relevant requirements.
2) Make edits to the main_script.py file to update the sender and receiver emails.
3) Add items off your wishlist to the Wishlist.csv file, in the correct format. A few example items have been provided.
4) Finally, set up the script to run at regular intervals according to your preference. The instructions for that can be found here: https://www.geeksforgeeks.org/schedule-a-python-script-to-run-daily/
