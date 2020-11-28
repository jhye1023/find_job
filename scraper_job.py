import requests
from bs4 import BeautifulSoup

headers = {
  'User-Agent':
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
}

def search_stackoverflow(param):
  results = []

  contents = requests.get(f"https://stackoverflow.com/jobs?r=true&q={param}")
  codes_soup = BeautifulSoup(contents.text, "html.parser")

  divs = codes_soup.find_all("div", {"class": "grid--cell fl1"})
  for div in divs:
    data = div.find("h2")
    title = data.find("a")["title"]
    url = data.find()["href"]
    # company = div.find("h3").find("span").text.strip()
    company, location= div.find("h3", {"class":"mb4"}).find_all("span", recursive=False)
    company = company.get_text(strip=True)
    location = location.get_text(strip=True)

    results.append({
      "title": title,
      "company": company,
      "location": location,
      "link": f"https://stackoverflow.com{url}"
      })

  return results
# print(search_stackoverflow("python"))

def search_indeed(param):
  results = []

  contents = requests.get(f"https://www.indeed.com/jobs?q={param}")
  codes_soup = BeautifulSoup(contents.text, "html.parser")
  divs = codes_soup.find_all("div", {"class":"jobsearch-SerpJobCard"})
  for div in divs:
    title = div.find("h2", {"class":"title"}).find("a")["title"]
    company = div.find("span", {"class":"company"})
    if company:
        company_anchor = company.find("a")
        if company_anchor is not None:
            company = str(company_anchor.string)
        else:
            company = str(company.string)
    else:
        company = None
    company = company.strip() 
    location = div.find("div", {"class":"recJobLoc"})
    
    if location is not None:
        location = div.find("div", {"class":"recJobLoc"})["data-rc-loc"]
    else:
        location = None
    job_id = div["data-jk"]

    results.append({
      "title": title,
      "company": company,
      "location": location,
      "link": f"http://www.indeed.com/viewjob?jk={job_id}"
      })
    
  return results
