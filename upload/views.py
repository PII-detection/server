from codecs import ignore_errors
from distutils import extension
from distutils.log import error
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

import chardet
global extension
def uploadFile(request):
    
    if request.method == "POST":
        # Fetching the form data
        fileTitle = request.POST["fileTitle"]
        uploadedFile = request.FILES["uploadedFile"]#bytes
        print(uploadedFile.name)
        global extension
        extension = uploadedFile.name.split(".")[-1]
        fileBytes = uploadedFile.read()
        extractor = word_extract()
        # content = extractor.extract_from_pdf(uploadedFile)
        content = []
        dic = {}
        if extension == 'pdf':
            content = extractor.pdf_to_dict(fileBytes)
        elif extension == 'txt':
            dic = chardet.detect(fileBytes)
            content = extractor.extract_from_txt(fileBytes.decode(dic['encoding'], 'ignore'))
            
        ## content:
        ##[[word, word], [word, word]]
        ## calculate sensitive words
        filter = getFilteredWords()
        score, sensitive_word = filter.filter(content) 
        redactor = Redactor()
        if extension == 'pdf':
            redactor.redaction(fileBytes, sensitive_word)
        elif extension == 'txt':
            txt_string = fileBytes.decode(dic['encoding'], 'ignore')
            word_list = txt_string.split()
            redactor.redact_txt(word_list, sensitive_word)
        
        
        request.session['score'] = score
        return redirect("detail/")
    if request.method == "GET":
        return render(request, "upload-file.html")

def detail(request):
    score = request.session.get('score')
    return render(request, "detail.html", {'score': score})
        
    
def download(request):
    filename = ""
    global extension
    if extension == 'pdf':
        file = open('./files/redacted.pdf', 'rb')
        filename = './files/redacted.pdf'
        response = HttpResponse(file)
        response['Content-Disposition'] = 'attachment;filename="redacted.pdf"'
    elif extension == 'txt':
        file = open('./files/redacted.txt', 'rb')
        filename = './files/redacted.txt'
        response = HttpResponse(file)
        response['Content-Disposition'] = 'attachment;filename="redacted.txt"'
   
    response['Content-Type'] = 'application/octet-stream' #设置头信息，告诉浏览器这是个文件
    
    os.remove(filename)
    return response