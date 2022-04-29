import os
import sys
cur_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(cur_dir)
from dataclasses import dataclass
import dataConvert as dc
import pickle
import torch
import numpy as np
import re
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive




class getFilteredWords:
    
    def __init__(self) -> None:
        pass
    
    def para_loader(self, file_dir):
        with open(file_dir, 'rb') as f:
            data = pickle.load(f)
        return data


    def model_loader(self, model_dir):
        use_gpu = 0
        device = torch.device("cuda" if use_gpu else "cpu")
        lstmModel = torch.load(model_dir, map_location=torch.device('cpu'))
        #for name, parameters in lstmModel.named_parameters():
        #    print(name, ': ', parameters.size())
        lstmModel.device = device
        return lstmModel
    
    
    def regularization(self, text_string):
        
        regex = '^(?!666|000|9\\d{2})\\d{3}-(?!00)\\d{2}-(?!0{4})\\d{4}.$' #from https://www.geeksforgeeks.org/how-to-validate-ssn-social-security-number-using-regular-expression/
        p = re.compile(regex)
        regex2 = '^(?!666|000|9\\d{2})\\d{3}-(?!00)\\d{2}-(?!0{4})\\d{4}$'
        p2 = re.compile(regex2)
        regexDate= '^\d{4}(-|/)(0[1-9]|1[0-2])(-|/)(0[1-9]|[12][0-9]|3[01]) $'
        d = re.compile(regexDate) 
        regexDate2= '^(0[1-9]|1[0-2])(-|/)(0[1-9]|[12][0-9]|3[01])(-|/)\d{4}$'
        d2 = re.compile(regexDate2) 
        email = '^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$'
        e = re.compile(email) 
        
        res = re.findall(p or p2 or d or d2 or e , text_string)
        
        return res
            
        
            
    
    ## input : word list
    def filter(self, sentences, text_string):
        gauth = GoogleAuth()           
        drive = GoogleDrive(gauth) 
        file_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format('1cIMiqUDUNldxO6Nl-KVuS9SV-cWi9WLi')}).GetList()
        for file in file_list:
            print('title: %s, id: %s' % (file['title'], file['id']))
        for i, file in enumerate(sorted(file_list, key = lambda x: x['title']), start=1):
        print('Downloading {} file from GDrive ({}/{})'.format(file['title'], i, len(file_list)))
        file.GetContentFile(file['title'])
        
        para_dir = '/Users/niwanchun/Documents/crowdstrike_PII_detection/upload/utils/paras/mapping.pkl'
        model_dir = '/Users/niwanchun/Documents/crowdstrike_PII_detection/upload/utils/models/test' 
        paras = self.para_loader(para_dir)
        # print(paras.keys())
        model = self.model_loader(model_dir)
        word_to_id = paras['word_to_id']
        char_to_id = paras['char_to_id']
        tag_to_id = paras['tag_to_id']
        delete = []
        all_words = 0
        id_to_delete = [tag_to_id['B-LOC'], tag_to_id['B-PER'], tag_to_id['B-ORG'], tag_to_id['I-PER'],
                            tag_to_id['I-ORG'],tag_to_id['B-MISC'], tag_to_id['I-LOC'], tag_to_id['I-MISC']]
        for sentence in sentences:
            all_words += len(sentence)
            test = dc.data_converting(sentence, word_to_id, char_to_id,lower = True)

            dwords, chars2_mask, dcaps, chars2_length, d = dc.masking(test)

            _, tag = model(dwords, chars2_mask, dcaps, chars2_length, d)
            
            delete_words = [ sentence[idx] for (idx, w) in enumerate(tag) if w in id_to_delete]
            delete.extend(delete_words)
        
       
        regex_res = self.regularization(text_string)
        
        delete.extend(regex_res)
        score = len(delete) / all_words
        
        delete = list(set(delete))
        print(delete)
        return score, delete