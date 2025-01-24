import os
import ast
import torch
import time
import inspect
import pandas as pd
import numpy as np
import torch.nn as nn
from torchinfo import summary
from torch.nn import functional as F
from torch.utils.data import Dataset, DataLoader
import multiprocessing as mp
from transformers import AutoTokenizer

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class political_ads_Dataset(Dataset):
    def __init__(self):
        self.data = pd.read_csv('C:\\Users\\Gebruiker\\Documents\\GitHub\\MadManAndMachines\\pythonProject\dataset.csv', sep=',', converters={'labels': pd.eval})
    def __len__(self):
        return self.data.shape[0]
    def __getitem__(self, idx):
        input = self.data['inputs'].iloc[idx]
        input = ast.literal_eval(input)['input_ids']
        input = torch.tensor(input)
        input = F.pad(input,(0,(512-input.shape[0])),"constant",0)
        label = self.data['labels'].iloc[idx]
        return input,label
    def downsize(self):
        for i, value in enumerate(self.data['labels']):
            self.data['labels'][i] = value[0]
        self.data = self.data.drop(self.data[self.data['labels'].eq(0)].sample(700).index)
        self.data = self.data.reset_index()
        return self.data
    
data = pd.read_csv('C:\\Users\\Gebruiker\\Documents\\GitHub\\MadManAndMachines\\pythonProject\\dataset.csv', sep=',', converters={'labels': pd.eval})
for i, value in enumerate(data['labels']):
    data['labels'][i] = value[0]
    #print(value[0])
data = data.drop(data[data['labels'].eq(0)].sample(700).index)
count = data['labels'].value_counts()
print(count,count.index[0])
#calculate index inverse frequency

#calculate index inverse frequency
length = 1122
def get_ratio(value):
    return 1/(value/length)

weights = np.zeros((32,))
print(weights.shape)
for i, value in enumerate(count):
    loc = count.index[i]
    weights[loc] = get_ratio(value)

weight = torch.tensor(weights)
print(weight)

class config:
    n_embd = 768
    n_classes = 32

class bert_classifier(nn.Module):
    def __init__(self,config):
        super().__init__()
        self.config = config
        self.model_bert = torch.hub.load('huggingface/pytorch-transformers', 'model', 'bert-base-uncased')
        self.lin = nn.Linear(config.n_embd,config.n_classes)
        #self.softmax = nn.softmax()
    def forward(self,x):
        x = self.model_bert(x)
        x = self.lin(x[1])
        return x

model = bert_classifier(config).to(device)

#-----TRAINING-HYPERPARAMETERS-----#
max_lr = 5e-5
min_lr = max_lr * 0.01
warmup_steps = 35
max_steps = 350
theta = 0.9
#-----TRAINING-HYPERPARAMETERS-----#

#-----BATCH-SIZE/GRADIENT-ACCUMILATION-----#
dataset = political_ads_Dataset()
dataset.downsize()
train_set, test_set = torch.utils.data.random_split(dataset, [int(0.8*len(dataset)), len(dataset)-int(0.8*len(dataset))])
print(len(test_set))
batch_size = 32
B = 32
grad_accum_steps = batch_size // B
train_loader = DataLoader(train_set, batch_size=B, shuffle=True)
test_loader = DataLoader(test_set, batch_size=B, shuffle=False)
print(grad_accum_steps)
#-----BATCH-SIZE/GRADIENT-ACCUMILATION-----#

#-----BATCH-SIZE/GRADIENT-ACCUMILATION-----#
dataset = political_ads_Dataset()
train_set, test_set = torch.utils.data.random_split(dataset, [int(0.8*len(dataset)), len(dataset)-int(0.8*len(dataset))])
print(len(test_set))
batch_size = 32
B = 32
grad_accum_steps = batch_size // B
train_loader = DataLoader(train_set, batch_size=B, shuffle=True)
test_loader = DataLoader(test_set, batch_size=B, shuffle=True)
print(grad_accum_steps)
#-----BATCH-SIZE/GRADIENT-ACCUMILATION-----#

#-----LEARNING-RATE-SCHEDULER-----#
def get_lr(it):
    if it < warmup_steps:
        return max_lr * (it+1) / warmup_steps
    if it > max_steps:
        return min_lr
    decay = it-warmup_steps
    return max_lr - decay * (max_lr/(max_steps-warmup_steps))
#-----LEARNING-RATE-SCHEDULER-----#

#-----PARAMETER-SETUP-----#
for param in model.parameters():
     param.requires_grad = False
for param in model.model_bert.pooler.parameters():
     param.requires_grad = True
for param in model.lin.parameters():
     param.requires_grad = True
     
layer_names = []
for param in model.named_parameters():
     layer_names.append(param[0])
layer_names.reverse()
#-----PARAMETER-SETUP-----#

#-----GRADUAL-FREEZING----#
class gradual_freezing():
    def __init__(self):
        self.unlock_ratio = 0.083
        self.i = 12
    def check_unfreeze(self,it):
        ratio = it/max_steps
        #print(ratio)
        #print(self.unlock_ratio)
        if ratio > self.unlock_ratio and self.i != 0:
            self.unlock_ratio = self.unlock_ratio +  0.083
            self.i = self.i - 1
            print(self.i)
            for param in model.model_bert.encoder.layer[self.i].parameters():
                param.requires_grad = True
                #print(param[0])
            return True
        return False
#-----GRADUAL-FREEZING-----#
a = gradual_freezing()

#-----DISCRIMINATIVE-FINE-TUNING-----#
def disc_fine_tuning(lr):
    parameters = []
    list1 = []
    previous = layer_names[2].split('.')[2]
    lr_disc = lr
    for idx,name in enumerate(layer_names):
        if name.split(".")[0] == "lin":
            for p in model.named_parameters():
                if p[0] == name and p[1].requires_grad:
                    parameters.append({ "params":p[1] ,"lr":lr})
        if name.split(".")[1] == "pooler":
            for p in model.named_parameters():
                if p[0] == name and p[1].requires_grad:
                    parameters.append({ "params":p[1] ,"lr":lr_disc})
                    list1.append(p[0])
        if name.split(".")[1] == "embeddings":
            for p in model.named_parameters():
                if p[0] == name and p[1].requires_grad:
                    parameters.append({ "params":p[1] ,"lr":lr_disc})
        if name.split(".")[1] == "encoder":
                current = name.split('.')[3]
                if current != previous:
                    lr_disc = theta*lr_disc
                previous = current
                for p in model.named_parameters():
                    if p[0] == name and p[1].requires_grad:
                        parameters.append({ "params":p[1] ,"lr":lr_disc})
                        list1.append(p[0])
    return parameters, list1
#-----DISCRIMINATIVE-FINE-TUNING-----#

#-----OPTIMIZER-----#
def configure_optimizers(model, weight_decay, learning_rate, device):
    param_dict = {pn: p for pn, p in model.named_parameters()}
    param_dict = {pn: p for pn, p in param_dict.items() if p.requires_grad}
    decay_params = [p for n, p in param_dict.items() if p.dim() >= 2]
    nodecay_params = [p for n, p in param_dict.items() if p.dim() < 2]
    optim_groups = [
        {'params': decay_params, 'weight_decay': weight_decay},
        {'params': nodecay_params, 'weight_decay': 0.0}
    ]
    num_decay_params = sum(p.numel() for p in decay_params)
    num_nodecay_params = sum(p.numel() for p in nodecay_params) 
    print(num_decay_params,num_nodecay_params)
    fused_available = 'fused' in inspect.signature(torch.optim.AdamW).parameters
    use_fused = fused_available and device == "cuda"
    print(f"using fused AdamW: {use_fused}")
    optimizer = torch.optim.AdamW(optim_groups, lr=learning_rate, betas=(0.9, 0.999), eps=1e-8, fused=use_fused)
    return optimizer  
  
optimizer = configure_optimizers(model = model, weight_decay=0.05, learning_rate=6e-4, device=device)
#-----OPTIMIZER-----#

#-----LOSS-FUNCTION-----#
class FocalLoss(nn.Module):
    def __init__(self, alpha=None, gamma=2, ignore_index=-100, reduction='mean'):
        super().__init__()
        # use standard CE loss without reducion as basis
        self.CE = nn.CrossEntropyLoss(reduction='none', ignore_index=ignore_index)
        self.alpha = alpha
        self.gamma = gamma
        self.reduction = reduction

    def forward(self, input, target):
        '''
        input (B, N)
        target (B)
        '''
        minus_logpt = self.CE(input, target)
        pt = torch.exp(-minus_logpt) # don't forget the minus here
        focal_loss = (1-pt)**self.gamma * minus_logpt

        # apply class weights
        if self.alpha != None:
            focal_loss *= self.alpha.gather(0, target)
        
        if self.reduction == 'mean':
            focal_loss = focal_loss.mean()
        elif self.reduction == 'sum':
            focal_loss = focal_loss.sum()
        return focal_loss

criterion = FocalLoss(alpha=weight.to(device))
#criterion = nn.CrossEntropyLoss()
#-----LOSS-FUNCTION-----#

#-----MISC-----#
checkpoint = 0
torch.set_float32_matmul_precision("high")
#-----MISC-----#

#model = bert_classifier(config).to(device)
for step in range(max_steps):
    last_step = (step == max_steps - 1)
    t0 = time.time()
    #optimizer.zero_grad(set_to_none=True)
    
    #validation loss
    if step % 20 == 0 or last_step:
        model.eval()
        with torch.no_grad():
            correct_acum = 0
            val_accum = 0
            val_loss_steps = 2
            for val_steps in range(val_loss_steps):
                x, y = next(iter(test_loader))
                x,y = x.to(device), y.to(device)
                with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
                    logits = model(x)
                    loss = criterion(logits,y)
                values,ind = torch.max(logits,dim = 1)
                print(y)
                print(ind)
                correct = np.sum((torch.eq(ind.to("cpu"),y.to("cpu")).numpy()))
                correct_acum = correct_acum + correct
                val_accum = val_accum + loss.detach()
            accuracy = correct_acum / (val_loss_steps * B)
            val_loss = val_accum / val_loss_steps
    
    #save checkpoint
    if step % 500 == 0:
        torch.save(model.state_dict(),f"checkpoint{checkpoint}.pt")
        checkpoint = checkpoint+1

    #minibatch process
    loss_accum = 0
    model.train()
    for mini_step in range(grad_accum_steps):
        x, y = next(iter(train_loader))
        x,y = x.to(device), y.to(device)
        with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
            logits = model(x)
            loss = criterion(logits,y)
        #print(f"loss mini_step = {loss} | ministep = {mini_step}")
        loss = loss / grad_accum_steps
        loss_accum = loss_accum + loss.detach()
        loss.backward()
    norm = torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)

    t1 = time.time()
    dt = t1-t0
    
    a.check_unfreeze(step)
    lr = get_lr(step)
    parameter = disc_fine_tuning(lr)
    for param_group in optimizer.param_groups:
        param_group = parameter
        
    
    optimizer.step()
    print(f"| step = {step} | time = {dt:.4f}s | lr = {lr:.4e} | loss = {loss_accum.item():.6f} |norm = {norm:.4f}| latest val loss = {val_loss:.4f}| accuracy = {accuracy:.4f}")
torch.save(model.state_dict(),"Final.pt")