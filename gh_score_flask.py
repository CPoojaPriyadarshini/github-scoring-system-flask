from flask import Flask, request, render_template
from bs4 import BeautifulSoup
import requests

app=Flask(__name__)
@app.route('/')
def ghscore_template():
    return render_template("ghscore_template.html")

@app.route('/', methods=['POST'])
def get_url():
    url = request.form['url']
    print(url)

    gh_score=0
    #url=input("Enter the url : ")
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    if(soup.title.string != 'Page not found · GitHub'):
        gh_score += 10

    else:
        return "No such GitHub account found"

    url_repo=url+"?tab=repositories"
    response_repo = requests.get(url_repo)
    soup_repo = BeautifulSoup(response_repo.content, 'html.parser')

    forked_commits = 0
    for sentence in soup_repo.find_all('li', {"class": "col-12 d-flex width-full py-4 border-bottom public fork"}):
        url_commits = url+"/"+sentence.h3.get_text().strip()
        response_commits = requests.get(url_commits)
        soup_commits = BeautifulSoup(response_commits.content, 'html.parser')
        c = soup_commits.find('span', {"class": "num text-emphasized"})
        cc = c.get_text().strip()
        cc = cc.replace(",","")
        forked_commits += int(cc) 
        if (forked_commits > 5):
            gh_score += 20
            break

    original_commits = 0
    for sentence in soup_repo.find_all('li', {"class": "col-12 d-flex width-full py-4 border-bottom public source"}):
        url_commits = url+"/"+sentence.h3.get_text().strip()
        response_commits = requests.get(url_commits)
        soup_commits = BeautifulSoup(response_commits.content, 'html.parser')
        c = soup_commits.find('span', {"class": "num text-emphasized"})
        cc = c.get_text().strip()
        cc = cc.replace(",","")
        original_commits += int(cc) 
        if (original_commits > 10):
            gh_score += 20
            break
    score="GitHub Score = "+str(gh_score)
    return score

app.run()
