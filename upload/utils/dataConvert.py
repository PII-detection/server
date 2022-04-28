# coding=utf-8
import optparse
import torch
import time
import pickle
from torch.autograd import Variable
import numpy as np
from loader import *
from utils import *


# python -m visdom.server

optparser = optparse.OptionParser()
optparser.add_option(
    "-t", "--test", default="data/eng.testb",
    help="Test set location"
)
optparser.add_option(
    '--score', default='evaluation/temp/score.txt',
    help='score file location'
)
optparser.add_option(
    "-g", '--use_gpu', default='1',
    type='int', help='whether or not to use gpu'
)
optparser.add_option(
    '--loss', default='loss.txt',
    help='loss file location'
)
optparser.add_option(
    '--model_path', default='models/test',
    help='model path'
)
optparser.add_option(
    '--map_path', default='models/mapping.pkl',
    help='model path'
)
optparser.add_option(
    '--char_mode', choices=['CNN', 'LSTM'], default='CNN',
    help='char_CNN or char_LSTM'
)

opts = optparser.parse_args()[0]

mapping_file = opts.map_path


import numpy as np
from torch.autograd import Variable

# word_to_id
# char_to_id
# tag_to_id

def data_converting(sentence, word_to_id, char_to_id, lower = True):
    '''
    Input

    + sentence: raw word list
    + word_to_id: loaded parameters
    + char_to_id: loaded parameters

    Return:

    + dico: a dictionary
    '''
    f = lambda x: x.lower() if lower else x
    data = []
    str_words = [w for w in sentence]
    words = [word_to_id[f(w) if f(w) in word_to_id else '<UNK>']
            for w in str_words]
    chars = [[char_to_id[c if c in char_to_id else '<UNK>'] for c in w]
            for w in str_words]
    caps = [cap_feature(w) for w in str_words]
    # tags = [tag_to_id[w[-1]] for w in sentence]
    dico = {
        'str_words': str_words,
            'words': words,
            'chars': chars,
            'caps': caps,
    }
    return dico

def cap_feature(s):
    if s.lower() == s:
        return 0
    elif s.upper() == s:
        return 1
    elif s[0].upper() == s[0]:
        return 2
    else:
        return 3

def masking(data, char_mode='CNN'):
    '''
    This function is to convert dictionary input into 

    Input: 

    + data: dictionary (dico);

    + char_mode: ['LSTM','CNN']

    Output:

    + dwords:
    + chars2_mask:
    + dcaps:
    + chars2_length:
    + d:
    '''
    assert type(data) == dict, "The input data should be a dictionary. Please check your input! "
    # words = data['str_words']
    chars2 = data['chars']
    caps = data['caps']
    if char_mode == "LSTM":
        chars2_sorted = sorted(chars2, key = lambda p: len(p), reverse=True)
        d = {} # 
        for i, ci in enumerate(chars2):
            for j, cj in enumerate(chars2_sorted):
                if ci == cj and not j in d and not i in d.values():
                    d[j] = i
                    continue
        chars2_length = [len(c) for c in chars2_sorted]
        char_maxl = max(chars2_length)
        chars2_mask = np.zeros((len(chars2_sorted), char_maxl),dtype='int')
        for i, c in enumerate(chars2_sorted):
            chars2_mask[i, :chars2_length[i]] = c
        chars2_mask = Variable(torch.LongTensor(chars2_mask))
        

    if char_mode == "CNN":
        d = {}
        chars2_length = [len(c) for c in chars2]
        char_maxl = max(chars2_length)
        chars2_mask = np.zeros((len(chars2_length),char_maxl), dtype = 'int')
        for i, c in enumerate(chars2):
            chars2_mask[i, :chars2_length[i]] = c
        chars2_mask = Variable(torch.LongTensor(chars2_mask))

    dwords = Variable(torch.LongTensor(data['words']))
    dcaps = Variable(torch.LongTensor(caps))
    
    return dwords, chars2_mask, dcaps, chars2_length, d






if __name__ == '__main__':
    test_words = "EU rejects German call to boycott British lamb ."
    sample = test_words.split()  
    dir = './src/models/test'
      


