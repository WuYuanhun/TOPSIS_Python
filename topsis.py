# @file: topsis.py
# @Author: Liu Cetian 
# @github: WuYuanhun
# @https://github.com/WuYuanhun/TOPSIS_Python

import numpy as np

class topsisMatrix():

    
    def __init__(self, data, numObj=0, numCrt=0, mode="default"):
        '''
        init a topsisMatrix class object
        param @mode can be 'kname', 'all' or 'default', which refers to the type of param@data.
        'kname' means that @data is a array or list (1-dimensional), which only contains the name of criteria needed to be evaluate
        'default' means that @data is a 2-dimensional array or list, which each row contains orinigal marks or scores of the same object's evalution correspond with the criteria
        'all' means that @data is a 2-dimensional array or list, which the first row is 'kname'-type and rest of it is 'default'-type
        '''
        
        ''' number of object needed to be evaluate '''
        self.numObj = numObj 
        
        ''' number of Criteria needed to be evaluate'''
        self.numCrt = numCrt

        ''' Topsis: Evaluation Matrix '''
        self.topMat = 0
        self.topNaMat = []

        ''' Formulation Matrix '''
        self.fotMat = 0

        ''' Weight Formulation Matrix '''
        self.wgtMat = 0

        ''' weight of each criteria '''
        self.weight = []

        ''' Formulate Matrix need to be evalutate '''
        self.ndUpdate = True  

        ''' ideal solution '''
        self.idealSolution = []

        if(mode == "kname"):
            self.kname = data
        elif(mode == "all"):
            self.kname = data[0]
            data.pop(0)
            self.push_back(data)
        else:
            self.kname = []
            ''' store org data '''
            self.push_back(data)
