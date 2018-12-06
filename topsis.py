# @file: topsis.py
# @Author: Liu Cetian 
# @github: WuYuanhun
# @https://github.com/WuYuanhun/TOPSIS_Python

import numpy as np

def calEuclidDis(vector):
    sum = 0
    for x in vector:
        sum += (x**2)
    
    return np.sqrt(sum)

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
        if not isinstance(idx, int):
            raise TypeError()
        if len(self.kname) <=0:
            for i in range(0, self.numCrt):
                self.kname.append("Crit" + str(i))
        if len(self.kname) <= idx:
            raise Exception("Out of Range")
        else:
            return self.kname[idx]
    
    def genForMat(self):
        self.fotMat = self.topNaMat
        self.size()
        for obj in range(0, self.numCrt):
            base = calEuclidDis([self.topNaMat[x][obj] for x in range(0,self.numObj)])
            print(self.knameAt(obj)+" base: "+str(base))
            for v in range(0,self.numObj):
                self.fotMat[v][obj] /= base
                print(self.fotMat[v][obj],end=' ')
            print()
        return self.fotMat

    ''' generate weight formulate matrix'''
    def genWgtMat(self):
        self.wgtMat = self.fotMat

        if len(self.weight) != self.numCrt:
            self.weight = np.ones(shape=self.numCrt,dtype=np.float64)
        
        for obj in self.wgtMat:
            idx = 0
            for crit in obj:
                crit *= self.weight[idx]
                idx += 1
        
        return self.wgtMat

    def solIdealSolution(self):
        self.idealSolution = []
        for x in range(0,self.numCrt):
            nBig = self.wgtMat[0][x]
            for i in range(0,self.numObj):
                nBig = max(self.wgtMat[i][x],nBig)
            self.idealSolution.append(nBig)

    def readObjName(self,data):
        self.objName = data

    def run(self):
        print(self.genEvaMat())
        print("genEvaMat Comp")
        print(self.genFotMat())
        print("genFotMat Comp")
        print(self.genWgtMat())
        print("genWgtMat Comp")

def store(data,filename="./data/temp.csv",type="default",header=None):
    
    if type=="matrix":
        with open(filename,'w') as f:
            if header is not None:
                for x in header:
                    x +='      '
                    print("%.5s"%x,end='   ')
                    f.write("%.5s   "%x)
                f.write('\n')
                print()
                    
            for obj in data:
                for x in obj:
                   print("%5.3f"%x,end='    ')
                   f.write("%5.3f   "%x)
                print()
                f.write('\n')

def DEEPmain():
    #DATASET
    _DATASET = []
    dataset = _DATASET #import dataset here
    tMatrix = topsisMatrix(data=dataset[0],mode="all")
    tMatrix.readObjName(dataset[1])
    tMatrix.run()
    return tMatrix
    

if __name__ == "__main__":
    # tMatrix = main()
    # tMatrix.run()
    tMatrix = DEEPmain()
