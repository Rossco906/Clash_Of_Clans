
from flask import Flask, render_template, make_response, request
import requests
import os
import time

app = Flask(__name__)

def format_server_time():
  server_time = time.localtime()
  return time.strftime("%I:%M:%S %p", server_time)


@app.route('/')
def index():
    context = { 'server_time': format_server_time() }
    ip = requests.get('https://api.ipify.org').text
    context["ipAdd"] = ip
    # 1 Create the template given the context.
    template = render_template('index.html', context=context)
    # 2 Create a response with the template.
    response = make_response(template)
    # 3 Attach a Cache-Control header to control store the content for a 10 minute period in the local CDN edge server. This time period is referred to as a Time To Live or TTL.
    response.headers['Cache-Control'] = 'public, max-age=300, s-maxage=600'
    return response

@app.route("/home", methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route("/clandata", methods=['GET', 'POST'])
def clanData():
    if request.method == 'POST':
        clanNo = request.form['clanNo']
        print(f"CLAN NUMBER: {clanNo}")
        # 2PJQP2C2Q - farruhk
    url = f"https://api.clashofclans.com/v1/clans/%23{clanNo}"
    headers = {
        "authorization" : "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjY1YmQxMDEyLTQ2ZTMtNGU2OC04MGUyLTE4ZGU0N2NhZDcxMiIsImlhdCI6MTU4ODA5OTgzMiwic3ViIjoiZGV2ZWxvcGVyL2ZkOTVlNmQ1LTVjMTMtNDc0OC01Mzc3LWY5ZmE0YTI3YzZhMSIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjkyLjIzNy4xNTYuNzEiLCI4Mi42OS4xMy4xMCIsIjM1LjIwMy4yNTEuNDMiXSwidHlwZSI6ImNsaWVudCJ9XX0.IN-dBo1KySkY2ANDeH1dXGSCyYvGUTIl7dxEq9a9grctYLh6ZMKQ-6golhDQi3zSbOETuiZpck3N_z1udOmyDg"
        }

    json = requests.get(url, headers=headers).json()
    clan = json["name"]
    clanMembers = json["memberList"]
    memberList = []
    members = []
    print(f"clan name: {clan}")
    for member in clanMembers:
        name = member["name"]
        rank = member["clanRank"]
        trophs = member["trophies"]
        tag = member["tag"]
        encodedTag = "".join(("%23", tag[1:]))
        memberList.append(tag)
        memberUrl = f"https://api.clashofclans.com/v1/players/{encodedTag}"

        memberJson = requests.get(memberUrl, headers=headers).json()
        members.append(memberJson)
        # print(memberJson)
    return render_template('clan.html', members=members, clanName = clan )

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))