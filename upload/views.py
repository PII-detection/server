from distutils import extension
import imp
import re
from webbrowser import get
from django.shortcuts import render
import os
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import View

from .utils.getFilteredWords import getFilteredWords
from .utils.word_extract import word_extract
from .utils.mask import Redactor


def uploadFile(request):
    
    if request.method == "POST":
        # Fetching the form data
        fileTitle = request.POST["fileTitle"]
        uploadedFile = request.FILES["uploadedFile"]#bytes
        print(uploadedFile.name)
        extension = uploadedFile.name.split(".")[-1]
        fileBytes = uploadedFile.read()
        extractor = word_extract()
        # content = extractor.extract_from_pdf(uploadedFile)
        content = []
        if extension == 'pdf':
            content, content_txt = extractor.pdf_to_dict(fileBytes)
        elif extension == 'txt':
            content, content_txt = extractor.extract_from_txt(fileBytes.decode('utf-8'))
        ##[[word, word], [word, word]]
        ## calculate sensitive words
        filter = getFilteredWords()
        score, sensitive_word = filter.filter(content, content_txt) 
        redactor = Redactor()
        if extension == 'pdf':
            redactor.redaction(fileBytes, sensitive_word)
        elif extension == 'txt':
            redactor.redact_txt(content, sensitive_word)
        
        
        request.session['score'] = score
        return redirect("detail/")
    if request.method == "GET":
        return render(request, "upload-file.html")

def detail(request):
    score = request.session.get('score')
    return render(request, "detail.html", {'score': score})
        
    
def download(request):
    filename = ""
    if os.path.exists('./files/redacted.pdf'):
        file = open('./files/redacted.pdf', 'rb')
        filename = './files/redacted.pdf'
        response = HttpResponse(file)
        response['Content-Disposition'] = 'attachment;filename="redacted.pdf"'
    elif os.path.exists('./files/redacted.txt'):
        file = open('./files/redacted.txt', 'rb')
        filename = './files/redacted.txt'
        response = HttpResponse(file)
        response['Content-Disposition'] = 'attachment;filename="redacted.txt"'
   
    response['Content-Type'] = 'application/octet-stream' #设置头信息，告诉浏览器这是个文件
    
    os.remove(filename)
    return response