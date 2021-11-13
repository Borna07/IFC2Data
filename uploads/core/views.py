from django.forms import models
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from ifcopenshell.file import file

from uploads.core.models import Document
# from uploads.core.forms import DocumentForm, FormatForm
from uploads.core.forms import DocumentForm

from uploads.core.forms import DownloadForm
from django.http import FileResponse

# Import HttpResponse module
from django.http.response import HttpResponse

from uploads.Functions import all_divide, parser, unique, unique_csv, unique_divide
import os

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
MEDIA_DIR = Path(BASE_DIR) / 'media'
DOCU_DIR = Path(BASE_DIR) / 'media' / 'documents'


def home(request):
    documents = Document.objects.all()
    return render(request, 'core/home.html', { 'documents': documents, 'form': DownloadForm() })



def model_form_upload(request):
    if request.method == 'POST':
        myfile = request.FILES['document']                      
        if myfile.name.endswith('.Ifc'.lower()):                # checking if the file is a ifc file
            form = DocumentForm(request.POST, request.FILES)    # declarin the file as form
            if form.is_valid():
                form.save(commit=True)

                MODEL_DIR = Path(MEDIA_DIR) / myfile.name        # path to saved ifc file
                
                return redirect('model_form_download')
    else:
        form = DocumentForm()
    return render(request, 'core/model_form_upload.html', {
        'form': form
    })





def model_form_download(request):
    form = DownloadForm(request.POST or None, initial={"file_download": "all","file_format": "xlsx"})

    if form.is_valid():
        selected = form.cleaned_data.get("file_download")     #get the radio button value
        file_format = form.cleaned_data.get("file_format")
        
        last_model = Document.objects.latest("uploaded_at")         # QuerySet method to take the last uploaded element; "uploaded_at" is a model field
        last_model_name = last_model.document.name
        MODEL_DIR = Path(MEDIA_DIR) / last_model_name   
        last_model_name = last_model.document.path

        last_model_name = last_model.document.name
        MODEL_DIR = Path(MEDIA_DIR) / last_model_name               # path to last uploaded document
        model = parser(MODEL_DIR)                                   # parsing the ifc file and converting to xlsx
        xlsx_name = Path(last_model_name).stem                      # get the name of last uploaded document without the suffix            

        if selected == "all":
            if file_format == "xlsx":
                XLS_DIR = Path(DOCU_DIR) / (xlsx_name + '_ALL.xlsx')  
                model.to_excel(XLS_DIR)                                # saving the converted ifc file to documents
                response = FileResponse(open(XLS_DIR, 'rb'))
            if file_format == "csv":
                CSV_DIR = Path(DOCU_DIR) / (xlsx_name + '_ALL.csv')  
                model.to_csv(CSV_DIR, encoding = 'utf-8')                                # saving the converted ifc file to documents
                response = FileResponse(open(CSV_DIR, 'rb'))
            return response



        if selected == "all_divide":
            XLS_DIR = Path(DOCU_DIR) / (xlsx_name + '_ALL_per_Type.xlsx')  
            all_divide(model, XLS_DIR)
            response = FileResponse(open(XLS_DIR, 'rb'))
            return response

        if selected == "unique":
            if file_format == "xlsx":
                XLS_DIR = Path(DOCU_DIR) / (xlsx_name + '_UNIQUE.xlsx') 
                unique(model, XLS_DIR)
                response = FileResponse(open(XLS_DIR, 'rb'))
            if file_format == "csv":
                CSV_DIR = Path(DOCU_DIR) / (xlsx_name + '_ALL.csv')  
                unique_csv(model, CSV_DIR)
                response = FileResponse(open(CSV_DIR, 'rb'))
            return response

        if selected == "unique_divide":
            XLS_DIR = Path(DOCU_DIR) / (xlsx_name + '_UNIQUE_per_Type.xlsx') 
            unique_divide(model, XLS_DIR)
            response = FileResponse(open(XLS_DIR, 'rb'))
            return response
    
    return render(request, 'core/model_form_download.html', {'form':form, })



