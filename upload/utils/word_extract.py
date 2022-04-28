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
    
            
    def pdf_to_dict(self, file_bytes):

        with fitz.Document(stream=file_bytes, filetype='pdf') as doc:
            text = ""
            for page in doc:
                text += page.get_text()

        default_st = nltk.sent_tokenize
        alice_sentences = default_st(text=text)   
        res = []
        
        whitespace_wt = nltk.WhitespaceTokenizer()
        for sentence in alice_sentences:
            words = whitespace_wt.tokenize(sentence)
            res.append(words)
        # print(res)
        return res
    
    def extract_from_txt(self, file_bytes):
        text = file_bytes.rstrip()
        # print(text)
        default_st = nltk.sent_tokenize
        alice_sentences = default_st(text=text)   
        res = []
        
        whitespace_wt = nltk.WhitespaceTokenizer()
        for sentence in alice_sentences:
            words = whitespace_wt.tokenize(sentence)
            res.append(words)
        # print(res)
        return res, text
        

        
        
    