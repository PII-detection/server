import PyPDF2 as p2
import nltk
import fitz  
nltk.download('punkt')
from pprint import pprint

class word_extract():
    content = []
    def __init__(self) -> None:
        pass
    
    def extract_from_pdf(self, file):
        pdfread = p2.PdfFileReader(file)
        # Extract single page

        if pdfread.getIsEncrypted() :
            return False
        
        # Extract entire pdf
        
        for i in range(0, pdfread.getNumPages()):
            pageinfo = pdfread.getPage(i)
            self.content.extend(pageinfo.extractText().split())
        return self.content
    
    def preprocess(self, content):
        def extractDigits(lst):
            return [[el.strip('""')] for el in lst]
        a_list = nltk.tokenize.sent_tokenize(content)    
        tmp = []
        list_list=extractDigits(a_list)
        
        for i in list_list:
            a = nltk.word_tokenize(i[0])
            tmp.append(a)

        for i in tmp:
            for n in i:
                if "@" in n:
                    sentencenum = tmp.index(i)
                    x = i.index(n)
                    tmp[sentencenum][x-1 : x+2] = [''.join(tmp[sentencenum][x-1 : x+2])]
        return tmp
    
    def pdf_to_dict(self, file_bytes):
        text = ""
        with fitz.Document(stream=file_bytes, filetype='pdf') as doc:
            
            for page in doc:
                text += page.get_text()
        # print(res)
        list_list = self.preprocess(text)
        return list_list
    
    def extract_from_txt(self, file_bytes):
        text = file_bytes.rstrip()
        # print(text)
        list_list = self.preprocess(text)
        # print(res)
        return list_list
        

        
        
    