# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.shortcuts import render
import requests
from HW3.settings import PREDICT_PRICE_APP_URL, PREDICT_PRICE_APP_KEY
from django.http import HttpResponseRedirect



# Create your views here.


def predict_car_price_view(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login")
    return render(request, "predict_car_price.html", {})


def submit_info(request):
    if request.method == "POST":
        data = {
            "Inputs": {
                "input1":
                    {
                        "ColumnNames": ["symboling", "normalized-losses", "make", "fuel-type", "aspiration",
                                        "num-of-doors", "body-style", "drive-wheels", "engine-location", "wheel-base",
                                        "length", "width", "height", "curb-weight", "engine-type", "num-of-cylinders",
                                        "engine-size", "fuel-system", "bore", "stroke", "compression-ratio",
                                        "horsepower", "peak-rpm", "city-mpg", "highway-mpg", "price"],
                        "Values": [
                            ["0", "0", request.POST["make"], "value", "value", "value", request.POST['body_style'], "value", "value", request.POST["wheel_base"], "0", "0",
                             "0", "0", "value", "value", request.POST["engine_size"], "value", "0", "0", "0", request.POST["horsepower"], request.POST["peak_rpm"], "0", request.POST["highway_mpg"], "0"],
                             ]
                    }, },
            "GlobalParameters": {
            }
        }
        body = str.encode(json.dumps(data))

        url = PREDICT_PRICE_APP_URL
        api_key = PREDICT_PRICE_APP_KEY
        headers = {'Content-Type': 'application/json', 'Authorization': ('Bearer ' + api_key)}
        try:
            response = requests.post(url, body, headers=headers)
            result = response.json()
            # print(result)
            score = result["Results"]['output1']['value']['Values'][0][7]
            price_str = "$%.2f" % float(score)
            print(score)
            return render(request, "show_car_price.html", {"price": price_str})
        except Exception as error:
            print("The request failed with status code: " + str(error))



