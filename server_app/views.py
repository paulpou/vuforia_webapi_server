from django.shortcuts import render , HttpResponse
from .models import TargetData , TreasureHuntData,SearchTargetData
from .forms import TargetForm,TreasureHuntForm,SearchTargetDataForm
import json
from rest_framework.test import RequestsClient
import base64
from django.conf import settings
import hashlib
import hmac
import urllib3
from datetime import datetime , timezone
from time import mktime
from time import strftime, gmtime
from wsgiref.handlers import format_date_time
from email.utils import formatdate
from .models import TargetData
import sys
import mimetypes
import cv2
import numpy as np
from django.db.models import Min , Max


# Create your views here.

# The hostname of the Cloud Recognition Web API
CLOUD_RECO_API_ENDPOINT = 'cloudreco.vuforia.com'

class LoadJson(object):
    def __init__(self, data):
	    self.__dict__ = json.loads(data)

def compute_md5_hex(data):
    """Return the hex MD5 of the data"""
    h = hashlib.md5()
    h.update(data)
    return h.hexdigest()


def compute_hmac_base64(key, data):
    """Return the Base64 encoded HMAC-SHA1 using the provide key"""
    h = hmac.new(key, None, hashlib.sha1)
    h.update(data)
    return base64.b64encode(h.digest())


def authorization_header_for_request(access_key, secret_key, method, content, content_type, date, request_path):
    """Return the value of the Authorization header for the request parameters"""
    components_to_sign = list()
    components_to_sign.append(method)
    components_to_sign.append(str(compute_md5_hex(content)))
    components_to_sign.append(str(content_type))
    components_to_sign.append(str(date))
    components_to_sign.append(str(request_path))
    string_to_sign = "\n".join(components_to_sign)
    signature = compute_hmac_base64(secret_key, string_to_sign.encode('utf-8'))
    auth_header = "VWS %s:%s" % (access_key.decode('utf-8'), signature.decode('utf-8'))
    return auth_header



http = urllib3.PoolManager()
date = formatdate(None, localtime=False, usegmt=True)
request_path='/targets'
content_type = 'application/json'
client = RequestsClient()

def uploadTD(request):

    target_data_form = TargetForm()
    target_data_form2 = TargetForm(request.POST)
    if request.method == 'POST':
        form = target_data_form.save(commit=False)
        #get the data from http request and add it to database
        target_name = request.POST.get("target_name")
        nameTH = request.POST.get("NameTH")
        target_text = request.POST.get("target_text")
        target_image = request.POST.get("target_image")
        target_3d_model = request.POST.get("target_3d_model")
        target_recognition_image = request.POST.get("target_recognition_image")
        form.target_name = target_name
        form.target_text = target_text
        form.target_image = target_image
        form.target_3d_model = target_3d_model
        form.target_recognition_image = target_recognition_image
        #make a http request to vuforia cloud for creation of a new target

        image = target_image
     	imagedata = base64.b64encode(f.read())

        print(target_name)
        data = {"name":str(target_name),
                "width": 11.0,
                "image":str(imagedata.decode('utf-8')),
                "active_flag": True

                }
        print(imagedata)
        encoded_data = json.dumps(data).encode('utf-8')
        target_auth = authorization_header_for_request(settings.API_SERVICE_ACCESS_KEY.encode('utf-8'), settings.API_SERVICE_SECRET_KEY.encode('utf-8'),'POST',encoded_data,content_type,date, request_path)
        print(target_auth)
        create_target = http.request('POST','https://vws.vuforia.com/targets',body=encoded_data,headers = {'Host': 'vws.vuforia.com', 'Authorization':str(target_auth),'Date':date,'Content-Type': 'application/json'})
        print(create_target.status)
        print(create_target.data)
        form.save()
    return render(request, "uploadTD.html", {'target_data_form': target_data_form})


def searchTargetData(request):
    target_data_form = SearchTargetDataForm()
    target_data_form2 = SearchTargetDataForm(request.POST)
    if request.method == 'POST':
        targetid = request.POST.get("targetid")
        ip = request.POST.get("ip")
        targetdata = TargetData.objects.filter(target_id = targetid)
        #return a json with deatils
        data = {
            'target_image': targetdata.target_image,
            'target_3d_model': targetdata.target_3d_model,
            'target_text': targetdata.target_text,
        }
    dump = json.dumps(data)
    return HttpResponse(dump, content_type='application/json')

