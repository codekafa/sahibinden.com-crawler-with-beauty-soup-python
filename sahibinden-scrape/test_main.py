from s_scrape.scraping import DetailsScraper, MainPageScraper
from s_scrape.io import IO
from s_scrape.srequests import URLlib, URLreq, URLsln

import time
import datetime

now = datetime.datetime.now()
day = now.day
month = now.month
year = now.year
suffix = str(day)+"-"+str(month)+"-"+str(year)

listingswait = 5
mainwait = 15

ulib = URLlib()
ureq = URLreq()

#print("Currently loading listings from pre-scraped list...")
mscr = MainPageScraper(5, uutils=ulib, lowerdelay=1, upperdelay=2)
print("Scraping started...")
mscr.scrapeModels()
print("Main car models scraped...")
mscr.scrapeSubModels()
print("Sub car models scraped...")
print("Waiting %d seconds before scraping listings..." %listingswait)
time.sleep(listingswait)
mscr.scrapeListings()
IO.pickle_dump("listings.pkl", mscr.listings)
IO.save_list("listings.txt", mscr.listings)
scr = DetailsScraper(mscr.listings, 16, ureq, lowerdelay=3, upperdelay=8)
print("Waiting %d seconds before scraping listings..." %mainwait)
time.sleep(mainwait)
scr.scrapeDetails()


lss = IO.pickle_load('listings.pkl')

finlist = []
for itm in lss:
    if type(itm) == list:
        for j in itm:
            finlist.append(j)
    else:
        finlist.append(itm)

results = scr.final_list

print("Using pandas for easier CSV extraction...")
import pandas as pd
import datetime
#tempfix
df = [x for x in results if x is not None]
df = pd.DataFrame(df)
df.to_csv("listings.csv", index = False)




#IO.pickle_dump("listings_list.pkl", scr.final_list)
#print("--------------------------------finish-----------------------------------")
#print("Scraping & pickling complete.")
