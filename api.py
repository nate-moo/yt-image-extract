from flask import Flask, request, render_template
from httpx import Client
from bs4 import BeautifulSoup
import re
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/api/v1/uri", methods=['POST'])
def uri():
    input_uri = request.form['uri']
    with Client() as c:
        res = c.get(input_uri).text
        soup = BeautifulSoup(res, features="html.parser")
        soup = soup.find_all('script')
        ytInitialData = "None"
        for i in soup:
            if "ytInitialData" in i.text:
                ytInitialData = i.text.strip()
                break
        # ytInitialData = ytInitialData.replace("var ytInitialData = ", "").strip()
        print(ytInitialData[0:15])
        outside = re.compile(r"(image[\s\S]*?\])")
        main = re.compile(r"(\"url\":\"([\S]*?\"))")
        # outsideMatched = re.match(outside, ytInitialData)
        outsideMatched = re.search(outside, ytInitialData).group(0)
        print(outsideMatched)
        mainMatched = re.search(main, outsideMatched).string
        print(mainMatched)
        loaded = json.loads("{\"" + mainMatched + "}" + "}")["image"]["thumbnails"][-1]
        # mainMatched = re.match(main, outsideMatched)
        image = ""
        return f"<a href='{loaded['url']}'>{loaded['url']}</a>"

if __name__ == '__main__':
    app.run(debug=True)