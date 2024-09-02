

import requests
from bs4 import BeautifulSoup
import time

def get_snapshots(url, limit):  #the limit is the number of snapshots we want to test, starting from the most recent one
    cdx_url = f"http://web.archive.org/cdx/search/cdx?url={url}&output=json&fl=timestamp,original&collapse=timestamp:6"
    response = requests.get(cdx_url)
    snapshots = response.json()[1:]  # ignore the header
    return snapshots[len(snapshots)-limit:]

def get_snapshot_content(snapshot_url): #here we compare only the text, but maybe comparing the CSS is more interesting
    response = requests.get(snapshot_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.get_text() 

def compare_snapshots(url):
    number_tests=10   #here we test only the last 10 snapshots of the website
    snapshots = get_snapshots(url,number_tests)
    if number_tests>len(snapshots):
        number_tests=len(snapshots)
    i=len(snapshots)-1 

    while (i>=len(snapshots)-number_tests)+1:  #we start from the most recent snapshot and we increment to the past

        timestamp1, original_url = snapshots[i]
        timestamp2, _ = snapshots[i-1]
        
        snapshot_url1 = f"http://web.archive.org/web/{timestamp1}/{original_url}"
        snapshot_url2 = f"http://web.archive.org/web/{timestamp2}/{original_url}"
        
        content1 = get_snapshot_content(snapshot_url1)
        content2 = get_snapshot_content(snapshot_url2)
        
        if content1 == content2: #if the 2 versions are the same
            print(f"no differences detected between the snapshots of the "+ timestamp1[0:4]+"/"+timestamp1[4:6]+"/"+timestamp1[6:8] +" and of "+ timestamp2[0:4]+"/"+timestamp2[4:6]+"/"+timestamp2[6:8])
        else:
            print(f"Differences detected between the snapshots of the "+ timestamp1[0:4]+"/"+timestamp1[4:6]+"/"+timestamp1[6:8] +" and of "+ timestamp2[0:4]+"/"+timestamp2[4:6]+"/"+timestamp2[6:8])
            print("last content update detected on :"+ timestamp1[0:4]+"/"+timestamp1[4:6]+"/"+timestamp1[6:8])
            
            break
        time.sleep(9)  #there is a delay between each request we can do
        i-=1


# test on a URL
url = "https://www.igloorental.se/"  #a random website of the database
compare_snapshots(url)