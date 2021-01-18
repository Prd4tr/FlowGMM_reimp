import torch, torchvision
import torch.optim as optim
import torch.nn as nn
import numpy as np
import os
import pandas as pd
from torch.utils.data import DataLoader
#import oil.augLayers as augLayers
from oil.model_trainers.classifier import Classifier
from oil.model_trainers.piModel import PiModel
from oil.model_trainers.vat import Vat
from oil.datasetup.datasets import CIFAR10
from oil.datasetup.dataloaders import getLabLoader
from oil.architectures.img_classifiers.networkparts import layer13
from oil.utils.utils import LoaderTo, cosLr, recursively_update,islice, imap
from oil.tuning.study import Study, train_trial
from flow_ssl.data.nlp_datasets import AG_News,YAHOO
#from flow_ssl.data import GAS, HEPMASS, MINIBOONE
from torchvision import transforms
import torch
from torch.autograd import Variable
from torch.nn import Parameter
import torch.nn.functional as F
import torch.nn as nn
import numpy as np
from torch.nn.utils import weight_norm
from oil.utils.utils import Expression,export,Named
from collections import defaultdict

@export
class SmallNN(nn.Module,metaclass=Named):
    """
    Very small CNN
    """
    def __init__(self, dim_in=768, num_classes=4,k=512):
        super().__init__()
        self.num_classes = num_classes
        self.net = nn.Sequential(
            nn.Linear(dim_in,k),
            nn.ReLU(),
            nn.Dropout(.5),
            nn.Linear(k,k),
            nn.ReLU(),
            nn.Dropout(.5),
            nn.Linear(k,num_classes),
        )
    def forward(self,x):
        return self.net(x)



PI_trial = train_trial(makeTabularTrainer,strict=True)

if __name__=='__main__':
    # thestudy = Study(PI_trial,uci_pi_spec2,study_name='uci_baseline2234_')
    # thestudy.run(num_trials=3,ordered=False)
    # #print(thestudy.covariates())
    # covars = thestudy.covariates()
    # covars['test_Acc'] = thestudy.outcomes['test_Acc'].values
    # covars['dev_Acc'] = thestudy.outcomes['dev_Acc'].values
    # print(covars.drop(['log_suffix','saved_at'],axis=1))

    # PI model baselines for AG-NEWS w/ best hyperparameters
    text_pi_cfg = {'dataset':AG_News,'num_epochs':50,'trainer':PiModel,'trainer_config':{'cons_weight':30},'opt_config':{'lr':1e-3},
                    'loader_config': {'amnt_labeled':200+5000,'lab_BS':200}}
    text_classifier_cfg = {'dataset':AG_News,'num_epochs':500,'trainer':Classifier,'opt_config':{'lr':1e-3},
                    'loader_config': {'amnt_labeled':200+5000,'lab_BS':200}}
    y_text_pi_cfg = {'dataset':YAHOO,'num_epochs':50,'trainer':PiModel,'trainer_config':{'cons_weight':[30]},'opt_config':{'lr':[1e-4]},
                    'loader_config': {'amnt_labeled':800+5000,'lab_BS':800}}
    y_text_classifier_cfg = {'dataset':YAHOO,'num_epochs':500,'trainer':Classifier,'opt_config':{'lr':1e-3},
                    'loader_config': {'amnt_labeled':800+5000,'lab_BS':800}}
    # Searched from
    # text_pi_cfg = {'num_epochs':50,'trainer':PiModel,'trainer_config':{'cons_weight':[10,30]},'opt_config':{'lr':[1e-3,3e-4,3e-3]},
    #                   'loader_config': {'amnt_labeled':200+5000,'lab_BS':200}}

    textstudy = Study(PI_trial,y_text_pi_cfg,study_name='Agnews')
    textstudy.run(3)
    print(textstudy.covariates())
    print(textstudy.outcomes)
