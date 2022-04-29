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
    
    
    def regularization(self, word_list):
        res = []
        regex_list = ['^(?!666|000|9\\d{2})\\d{3}-(?!00)\\d{2}-(?!0{4})\\d{4}.$', '^(?!666|000|9\\d{2})\\d{3}-(?!00)\\d{2}-(?!0{4})\\d{4}$','^\d{4}(-|/)(0[1-9]|1[0-2])(-|/)(0[1-9]|[12][0-9]|3[01]) $','^(0[1-9]|1[0-2])(-|/)(0[1-9]|[12][0-9]|3[01])(-|/)\d{4}$','^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$']
        for word in word_list:
            for i in range(len(regex_list)):
                rule = re.compile(regex_list[i])
                if(len(re.findall(rule, word))) > 0:
                    res.append(word)
            
        return list(set(res))
            
        
            
    
    ## input : word list
    def filter(self, sentences):
        
        para_dir = 'upload/utils/paras/mapping.pkl'
        model_dir = 'upload/utils/models/test' 
        paras = self.para_loader(para_dir)
        # print(paras.keys())
        model = self.model_loader(model_dir)
        word_to_id = paras['word_to_id']
        char_to_id = paras['char_to_id']
        tag_to_id = paras['tag_to_id']
        delete = []
        all_words = []
        id_to_delete = [tag_to_id['B-LOC'], tag_to_id['B-PER'], tag_to_id['B-ORG'], tag_to_id['I-PER'],
                            tag_to_id['I-ORG'],tag_to_id['B-MISC'], tag_to_id['I-LOC'], tag_to_id['I-MISC']]
        for sentence in sentences:
            all_words.extend(sentence)
            test = dc.data_converting(sentence, word_to_id, char_to_id,lower = True)

            dwords, chars2_mask, dcaps, chars2_length, d = dc.masking(test)

            _, tag = model(dwords, chars2_mask, dcaps, chars2_length, d)
            
            delete_words = [ sentence[idx] for (idx, w) in enumerate(tag) if w in id_to_delete]
            delete.extend(delete_words)
        
        
        
        regex_res = self.regularization(all_words)
        print("regex_res:", regex_res)
        delete.extend(regex_res)
        score = len(delete) / len(all_words)
        
        delete = list(set(delete))
        print(delete)
        return score, delete