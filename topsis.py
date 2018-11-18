# @file: topsis.py
# @Author: Liu Cetian 
# @github: WuYuanhun
# @https://github.com/WuYuanhun/TOPSIS_Python

import numpy as np

class topsisMatrix():

    
    def __init__(self, data, numObj=0, numCrt=0, mode="default"):
        '''
        init a topsisMatrix class object \n
        param @mode can be 'kname', 'all' or 'default', which refers to the type of param@data. \n
        'kname' means that @data is a array or list (1-dimensional), which only contains the name of criteria needed to be evaluate \n
        'default' means that @data is a 2-dimensional array or list, which each row contains orinigal marks or scores of the same object's evalution correspond with the criteria \n
        'all' means that @data is a 2-dimensional array or list, which the first row is 'kname'-type and rest of it is 'default'-type \n
        '''
        
        ''' number of object needed to be evaluate '''
        self.numObj = numObj 
        
        ''' number of Criteria needed to be evaluate'''
        self.numCrt = numCrt

        ''' Topsis: Evaluation Matrix '''
        self.topMat = 0
        self.topNaMat = []

        ''' Formulation Matrdix '''
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

    def __push_back_list(self, data):
        ''' 
            add another group data

            WARNING: BUILD-IN Method, high risk operation
        '''
        if(isinstance(data, list)):
            self.topNaMat.append(np.array(data,dtype=np.float64))


    def push_back(self, data):
        ''' 
        add extra group of data 

        data could be 2D list, 2D array & topsisMatrix
        '''
        
        if(isinstance(data,list)):
            self.ndUpdate = True
            if(isinstance(data[0],list)):
                for adata in data:
                    self.__push_back_list(adata)
            else:
                self.topNaMat.append(np.array(data))
        
        elif(isinstance(data, np.ndarray)):
            self.ndUpdate = True
            self.topNaMat.append(data)

        elif(isinstance(data, topsisMatrix)):
            self.ndUpdate = True
            for adata in data.topNaMat:
                self.topNaMat.append(adata)
        
        else:
            raise TypeError("data is a not supported type")
        
        self.genEvaMat()


    def genEvaMat(self):
        '''
            generate evaluation Matrix and return the matrix
        '''
        if self.ndUpdate:
            self.topMat = np.array(self.topNaMat)
            self.ndUpdate = False
        return self.topMat

    def size(self):
        '''
            update the number of object and number of criteria 
            and return as tuple
        '''
        self.numObj = len(self.topNaMat)
        self.numCrt = len(self.topNaMat[0])
        return (self.numObj, self.numCrt)

    def knameAt(self, idx):
        '''
        return key name of criteria at position @idx
        '''