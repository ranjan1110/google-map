# -*- coding:utf8 -*-
# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") != "map":
        return {}
    #baseurl = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    yql_url = makeYqlQuery(req)
    if yql_url is None:
        return {}
    
    result = urlopen(yql_url).read()
    data = json.loads(result)
    place_id_1=data['results'][0]['place_id']
    
    yql_url_1=makeYqlQuery1(req,place_id_1)
    if yql_url_1 is None:
        return {}
    result_1 = urlopen(yql_url_1).read()
    data_1 = json.loads(result_1)
    
    res = makeWebhookResult(data,data_1)
    return res


def makeYqlQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    item = parameters.get("itemssss")
    cityarr=city.split(" ")
    itemarr=item.split(" ")
    
    if city is None:
        return None
    url_1="https://maps.googleapis.com/maps/api/place/textsearch/json?query="
    url_1=url_1 + cityarr[0]
    c=len(cityarr)

    for i in range(1,c):
          url_1=url_1+ '+' + cityarr[i]
    for i in itemarr:
          url_1 = url_1 + '+' + i
 
        
        
    url_1=url_1+ '+'+"office"+"&key=" +"AIzaSyD0HnUitzdPovQlJ-ifc2BbU6lm04QTtxE"
    
    return url_1

def makeYqlQuery1(req,place_id_1):
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    item = parameters.get("itemssss")
    cityarr=city.split(" ")
    itemarr=item.split(" ")
    
    if city is None:
        return None
    '''url_1="https://maps.googleapis.com/maps/api/place/textsearch/json?query="
    url_1=url_1 + cityarr[0]
    c=len(cityarr)

    for i in range(1,c):
          url_1=url_1+ '+' + cityarr[i]
    for i in itemarr:
          url_1 = url_1 + '+' + i
 
        
        
    url_1=url_1+ '+'+"office"+"&key=" +"AIzaSyD0HnUitzdPovQlJ-ifc2BbU6lm04QTtxE"
    
    return url_1'''
    url_2="https://maps.googleapis.com/maps/api/place/details/json?placeid="+place_id_1+"&key=AIzaSyD0HnUitzdPovQlJ-ifc2BbU6lm04QTtxE"
    return url_2


def makeWebhookResult(data,data_1):
    #results = data.get('results')
    #if results is None:
     #   return {}

    formatted_address_1 = data['results'][0]['formatted_address']
    name = data['results'][0]['name']
    if formatted_address_1 is None:
        return {}
    place_id_1=data['results'][0]['place_id']
    if place_id_1 is None:
        return {}
    phone=data_1['result']['formatted_phone_number']
    
   
    if 'opening_hours' in data_1['result']:
                weekday=data_1['result']['opening_hours']['weekday_text'][0]
                weekday1=data_1['result']['opening_hours']['weekday_text'][1]
                weekday2=data_1['result']['opening_hours']['weekday_text'][2]
                weekday3=data_1['result']['opening_hours']['weekday_text'][3]
                weekday4=data_1['result']['opening_hours']['weekday_text'][4]
                weekday5=data_1['result']['opening_hours']['weekday_text'][5]
                weekday6=data_1['result']['opening_hours']['weekday_text'][6]
     else:
        speech = name + " \n address of the office is " + formatted_address_1 + " \n \n phone no is "+phone
        print("Response:")
        print(speech)
        return {
        "speech": speech,
        "displayText": speech,
        "source": "https://github.com/ranjan1110/google-map"}
             
    
    

    speech = name + " \n address of the office is " + formatted_address_1 + " \n \n phone no is "+phone+ "\n \n daily opening hours \n \n"+weekday+"\n \n"+weekday1+"\n \n"+weekday2+"\n \n"+weekday3+"\n \n"+weekday4+"\n \n"+weekday5+"\n \n"+weekday6

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "https://github.com/ranjan1110/google-map"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
