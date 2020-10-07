from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import AlprForm
import sys
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import datetime
import requests
from pprint import pprint
import os


@login_required
def alpr(request):

    if request.method == 'POST':

        form = AlprForm(request.POST, request.FILES)

        if form.is_valid():  

            myfile = request.FILES['image']
            
            fs = FileSystemStorage(location='media/alpr/')

            filename = fs.save(myfile.name, myfile)

            uploaded_file_url = fs.url(filename)
            
            abs_path =  os.path.join(os.path.dirname(os.path.dirname(__file__)),'media/alpr/'+filename)

            messages.success(request, f'Your image is being processed. Kindly wait...')

            regions = ['in'] # Change to your country

            with open(abs_path, 'rb') as fp:
                response = requests.post(
                    'https://api.platerecognizer.com/v1/plate-reader/',
                    data=dict(regions=regions),  # Optional
                    files=dict(upload=fp),
                    headers={'Authorization': 'Token '+os.getenv("ALPR_TOKEN")})

                result = response.json()

                context = {
                    'form': form,
                    'img' : '/media/alpr/'+filename,
                    'plate': result['results'][0]['plate'],
                    'result': result['results']
                }

    else:
        form = AlprForm()

        context = {
            'form': form
        }

    return render(request, 'alpr/alpr.html', context)
