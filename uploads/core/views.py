from django.forms import models
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from uploads.core.models import Document
from uploads.core.forms import DocumentForm
from uploads.core.forms import FileFormatForm 
from django.http import FileResponse
import mimetypes

# Import HttpResponse module
from django.http.response import HttpResponse

from uploads.Functions import all_divide, parser, unique, unique_divide
import os

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
MEDIA_DIR = Path(BASE_DIR) / 'media'
DOCU_DIR = Path(BASE_DIR) / 'media' / 'documents'


def home(request):
    documents = Document.objects.all()
    return render(request, 'core/home.html', { 'documents': documents, 'form': FileFormatForm() })



def model_form_upload(request):
    if request.method == 'POST':
        myfile = request.FILES['document']                      
        if myfile.name.endswith('.Ifc'.lower()):                # checking if the file is a ifc file
            form = DocumentForm(request.POST, request.FILES)    # declarin the file as form
            if form.is_valid():
                form.save(commit=True)

                MODEL_DIR = Path(MEDIA_DIR) / myfile.name        # path to saved ifc file
                
                return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'core/model_form_upload.html', {
        'form': form
    })




def model_form_download(request):
    form = FileFormatForm(request.POST)

    if form.is_valid():
        selected = form.cleaned_data.get("file_format")     #get the radio button value
        
        last_model = Document.objects.latest("uploaded_at")         # QuerySet method to take the last uploaded element; "uploaded_at" is a model field
        last_model_name = last_model.document.name
        MODEL_DIR = Path(MEDIA_DIR) / last_model_name   
        last_model_name = last_model.document.path

        last_model_name = last_model.document.name
        MODEL_DIR = Path(MEDIA_DIR) / last_model_name               # path to last uploaded document
        model = parser(MODEL_DIR)                                   # parsing the ifc file and converting to xlsx

        if selected == "all":        
            xlsx_name = Path(last_model_name).stem                      # get the name of last uploaded document without the suffix            
            XLS_DIR = Path(DOCU_DIR) / (xlsx_name + '_ALL.xlsx')  
        
            model.to_excel(XLS_DIR)                                # saving the converted ifc file to documents
            response = FileResponse(open(XLS_DIR, 'rb'))
            return response

        if selected == "all_divide":
            xlsx_name = Path(last_model_name).stem                      # get the name of last uploaded document without the suffix            
            XLS_DIR = Path(DOCU_DIR) / (xlsx_name + '_ALL_per_Type.xlsx')  
        
            all_divide(model, XLS_DIR)
            response = FileResponse(open(XLS_DIR, 'rb'))
            return response

        if selected == "unique":
            xlsx_name = Path(last_model_name).stem                      # get the name of last uploaded document without the suffix            
            XLS_DIR = Path(DOCU_DIR) / (xlsx_name + '_UNIQUE.xlsx') 
            unique(model, XLS_DIR)
            response = FileResponse(open(XLS_DIR, 'rb'))
            return response

        if selected == "unique_divide":
            xlsx_name = Path(last_model_name).stem                      # get the name of last uploaded document without the suffix            
            XLS_DIR = Path(DOCU_DIR) / (xlsx_name + '_UNIQUE_per_Type.xlsx') 
            unique_divide(model, XLS_DIR)
            response = FileResponse(open(XLS_DIR, 'rb'))
            return response
    
    return render(request, 'core/model_form_download.html', {'form':form})




        # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # # Define text file name
        # filename = 'test.txt'
        # # Define the full file path
        # filepath = BASE_DIR + '/downloadapp/Files/' + filename
        # Open the file for reading content





        # # Set the mime type
        # mime_type, _ = mimetypes.guess_type(BASE_DIR)
        # # Set the return value of the HttpResponse
        # response = HttpResponse(path, content_type=mime_type)
        # # Set the HTTP header for sending to browser
        # response['Content-Disposition'] = "attachment; last_model_name=%s" % last_model_name
        

        # model = parser(MODEL_DIR)                       # parsing the ifc file and converting to xlsx

        # xlsx_name = myfile.name + '.xlsx'               
        # XLS_DIR = Path(DOCU_DIR) / xlsx_name
        
        # model[1].to_excel(XLS_DIR)  
        # path = open(MODEL_DIR, 'r')
        
        #print(last_model_name)
        #return(response)

