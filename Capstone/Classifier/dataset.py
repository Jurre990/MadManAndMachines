import os
import numpy as np
import pandas as pd
import multiprocessing as mp
from transformers import AutoTokenizer

#read data
def load():
    df = pd.read_csv('C:\\Users\\vd00r\\OneDrive\\Documenten\\GitHub\\MadManAndMachines\\pythonProject\\text_data.csv', sep=',')
    #turn string to list
    for i, id in enumerate(df['codes']):
        df['codes'][i] = eval(id)
    #drop data
    df = df.drop(['Unnamed: 0'],axis = 1)
    return(df.to_numpy())

#multiprocessing
tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
cpu_c = os.cpu_count()//2 

def transform(fw):
    print(fw[0])
    tok = tokenizer.encode_plus(fw[0])
    return tok,fw[1]

def proc(fw):
    with mp.Pool(cpu_c) as pool:
        tokenized_text = []
        labels = []
        for data in pool.imap(transform,fw,chunksize=16):
            tokenized_text.append(data[0])
            labels.append(data[1])
        return tokenized_text,labels

if __name__ == '__main__':
    df = load()
    #print(df)
    a = proc(df)
    #print(a[0]['input_ids'])
    d = {"inputs": a[0],"labels": a[1]} 
    array = pd.DataFrame(data = d).to_csv('dataset.csv',index=False)
    print(array)