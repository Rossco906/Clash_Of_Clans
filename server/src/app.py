
from flask import Flask, render_template, make_response
import os
import time

app = Flask(__name__)

def format_server_time():
  server_time = time.localtime()
  return time.strftime("%I:%M:%S %p", server_time)


@app.route('/')
def index():
    context = { 'server_time': format_server_time() }
    # 1 Create the template given the context.
    template = render_template('index.html', context=context)
    # 2 Create a response with the template.
    response = make_response(template)
    # 3 Attach a Cache-Control header to control store the content for a 10 minute period in the local CDN edge server. This time period is referred to as a Time To Live or TTL.
    response.headers['Cache-Control'] = 'public, max-age=300, s-maxage=600'
    return response

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))