  
"""
Created on Mon Oct 21 18:30:14 2019

@author: cheremma
"""
import numpy as np
#import pandas as pd
import sklearn.metrics as mat
#import collections as cltn



class Entropy_Node():
    def __init__(self):
        self.data=None
        self.branch=None
        self.entropy=None
        self.unique=None
        self.result=np.inf
        self.name=None
        self.leaf=False
        self.split_name = None
        self.categs_entr = None
        self.next =[]
        
	#you can also remove few variables cuz we aren't using them but you can use them to make ID3 is some other way

        
class decision_tree():
    
    
    #initialize the root of the tree
    def __init__(self):
        self.root=None # root of the tree
        self.matched=[]
#        self.ig_container=[]
        
        
        
    # to count  the occunrence of feature
    def unique_counts(self,data):
        
        uni_count={}#dictionary to store the no. of occurence of a feature as 'value' as feature name  as key
       
        for i in data:
            if i not in uni_count:
                uni_count[i]=1
            else:
                uni_count[i]+=1
        return uni_count
    

    
    # calculating entropy 
    
    def entropy(self,data):
        length =len(data)
        counts = self.unique_counts(data[:,-1])
        entrp_y={}
        
        for labels in counts.keys():
            size=counts[labels]
            
            entrp_y[labels] = -((size/length)*np.log2(size/length))
            
        return entrp_y
    
    
    
    def split(self,categs,data,idx,feature_to_remove=False):
        result={}
        arr=np.array([]).reshape(0,data.shape[1])
        
#        arr_2 = np.array([]).reshape(0,data.shape[1]-1)
        
        for name in categs:
            #print(name)
            for i in range(len(data)):
                if data[i,idx]==name:
                    arr = np.vstack((arr,data[i,:]))
                    
            
            if feature_to_remove is True:
                arr=np.delete(arr,idx,axis=1)
#            print(arr)
#            arr_2=np.array([]).reshape(0,arr_2.shape[1])

            result[name]=arr.copy()
            arr=np.array([]).reshape(0,data.shape[1])
            
        
        return result
    
    
    def find_the_result(self,data):
        
        unique = np.unique(data[:,-1])
        fin_tok=0
        name = None
        
        for labels in unique:
            tok=0 
            for i in range(len(data)):
                if data[i,-1]==labels:
                    tok+=1
            if tok>fin_tok:
                fin_tok = tok
                name = labels
        return name
        
    
    def build_tree(self,data,pare_len,pare_entropy,paren_name):
        node=Entropy_Node()
        node.data=data
        
        max_entropy = sum(self.entropy(data).values())
        
        if max_entropy==0:
            node.result=self.find_the_result(data)
            #node.unique=np.unique(node.data[:,0])
            node.leaf = True
            node.split_name=paren_name
#            print("**********result*********")
#            print(node.unique,node.result)
#            print("***********result**********")
            return node
        
        if data.shape[1]<=1:
            #node.unique=np.unique(node.data[:,0])
            node.result=self.find_the_result(node.data)
            node.split_name=paren_name
            node.leaf=True
#           1 print("*******result************")
#            print(node.unique,node.result)
#            print("*******result**************")
            return node
        
        
        outer_entr = {}
        out_IG =0
        best_feature_no = None
        best_data =None
        data_len = len(data)
            
        for feature_no in range(data.shape[1]-1):
            in_IG=None
            entropies ={}
#            step_1 = sum(entropies.values())
#            unique=np.unique(data[:,feature_no])
            avg=0
            splitted_data = self.split(np.unique(data[:,feature_no]),data,feature_no)
            for spl_data in splitted_data.keys():
                entr=self.entropy(splitted_data[spl_data])
                entropies=entr
                avg += (len(spl_data)/data_len)*(sum(entr.values()))
                
                
                
                
                
#            avg = (len(data[:,feature_no])/pare_len)*step_1
            in_IG = pare_entropy-avg
            
            
            
            if out_IG<in_IG:
                out_IG=in_IG
                outer_entr = entropies
                best_feature_no = feature_no
                best_data = data[:,feature_no]
                
        
        if out_IG !=0:
            
            node.data = best_data
            node.split_name=paren_name
            node.unique = np.unique(data[:,best_feature_no])
            node.entropy = sum(outer_entr.values())
            node.categs_entr = outer_entr
            
            
            
            node.branch = self.split(node.unique,data,best_feature_no,True)
        
            for branch_name in node.branch.keys():
                node.next.append(self.build_tree(node.branch[branch_name],data_len,sum(self.entropy(node.branch[branch_name]).values()),branch_name))
        else:
            
            node.data=data
            #node.unique=(np.unique(node.data[:,0]))
            node.unique=[paren_name]
            node.result = self.find_the_result(data)
#            print("*******result************")
            #print(node.unique,node.result)
#            print("*************result********")
            node.leaf=True
            return node
        
        return node
    
    
    def contains_(self,node,c,append=None):
        found=0
        
        if node.unique is not None:
            
            
            #print(node.unique)
            for i in c:
                if node.unique.__contains__(str(i)):
                    #print(i)
#                    if append is not None and self.matched.__contains__(i)==False and len(self.matched)!=4:
#                        self.matched.append(i)
#                        print(self.matched)
                        found=1
#                    else:
#                        found=1
        return found,c
    
    
    
    
    
    
    def predict(self,node,c):
#        print(node.split_name)
        if node.leaf is True and  c.__contains__(node.split_name):
            y_pred.append(node.result)
            print(node.result)
            return
        
        
        for nex in node.next:
            if c.__contains__(nex.split_name):
                self.predict(nex,c)
                break
        return
        

            
            
y_pred=[]          
           
            
if __name__ =="__main__":
    data=[['slashdot','USA','yes','18','None'],
		['google','France','yes','23','Premium'],
		['digg','USA','yes','24','Basic'],
		['kiwitobes','France','yes','23','Basic'],
		['google','UK','no','21','Premium'],
		['(direct)','New Zealand','no','12','None'],
		['(direct)','UK','no','21','Basic'],
		['google','USA','no','24','Premium'],
		['slashdot','France','yes','19','None'],
		['digg','USA','no','18','None'],
		['google','UK','no','18','None'],
		['kiwitobes','UK','no','19','None'],
		['digg','New Zealand','yes','12','Basic'],
		['slashdot','UK','no','21','None'],
		['google','UK','yes','18','Basic'],
		['kiwitobes','France','yes','19','Basic']]
    
    c=data
    data=np.array(data)
    d_classifier = decision_tree()
    
    root=d_classifier.build_tree(data,len(data),sum(d_classifier.entropy(data).values()),"root")
    
#    for i in c:
    for i in c:

        d_classifier.predict(root,i)
        
    print("accuracy_score is {}%".format(mat.accuracy_score(data[:,-1],y_pred)*100))
