#!/usr/bin/env python
# coding: utf-8

# In[2]:


import time
from collections import Counter
import pandas as pd
import numpy as np

#read Sudoki Matrix
def readdata():
    
    m=pd.read_csv('sample.csv',index_col=None,header=None)
    m=m.values
    n=m.flatten()
    
    return m,n

#Function para, used to generate row, column, and range of 9 squares.

def para(i):
    r=i//9
    c=i%9
    rr=r//3
    cr=c//3
    rr_d=rr*3
    rr_u=rr*3+3
    cr_d=cr*3
    cr_u=cr*3+3
    return r,c,rr_d,rr_u,cr_d,cr_u


#Generate a available value list for a cell

def ql(m,i):
    f_l=[0,1,2,3,4,5,6,7,8,9]
    r,c,rr_d,rr_u,cr_d,cr_u=para(i)
    a=list(set(list(m[r])+list(m[:,c])+list(m[rr_d:rr_u,cr_d:cr_u].flatten())))
    q_l=[x for x in f_l if x not in a]
    return q_l,r,c


#generate a dict for all empty cell

def dq_l(m,n):
    dql={}
    for i in range(81):
        if n[i]==0:
            q_l,r,c=ql(m,i)
            dql[i]=q_l
    return dql



#recursive loop to test all available list one by one and find the final solution.

def dg(m,n,i,l,flag):
    if flag==0:
        for j in range(i,l+1):
            if n[j]==0:
                break
        q_l,r,c=ql(m,j)
        
        if len(q_l)==0:

            flag=-1
            return flag
        if j==l and len(q_l)>1:
            flag=-1
            return flag
        for t in q_l:
            m[r,c]=t
            k=j+1
            if k==l+1:
                flag=1
                return flag
            else:
                flag=0
                flag=dg(m,n,k,l,flag)
                if flag==1:
                    break
        if flag==-1:
            m[r,c]=0
            return flag
        if flag==1:
            return flag


#find the cell whose available value only have 1.
def wy(m,n): 
    flag=0
    for i in range(81):
        if n[i]==0:
            q_l,r,c=ql(m,i)
            if len(q_l)==1:
                m[r,c]=q_l[0]
                n[i]=q_l[0]
                flag=1
    return m,n,flag

        
#check all available list in one row and find the value which only exist in one cell

def h_c(m,n):
    flag=0
    dql=dq_l(m,n)
    for i in range(9):
        la=[]
        k_l=[x for x in range(9*i,9*i+9) if x in dql.keys()]
        for k in k_l:
            la+=dql[k]
        ct=Counter(la)
        lb=[]
        
        for j,v in ct.items():
            if v==1:
                lb.append(j)
        for t in lb:
            for k in k_l:
                if t in dql[k]:
                    r,c,_,_,_,_=para(k)
                    n[k]=t
                    m[r,c]=t
                    k_l.remove(k)
                    flag=1
                    break
    dql={}
    return m,n,flag


#check all available list in one column and find the value which only exist in one cell

def v_c(m,n):
    flag=0
    dql=dq_l(m,n)
    for i in range(9):
        la=[]
        k_l=[x for x in range(i,73+i,9) if x in dql.keys()]
        for k in k_l:
            la+=dql[k]
        ct=Counter(la)
        lb=[]
        for j,v in ct.items():
            if v==1:
                lb.append(j)
        for t in lb:
            for k in k_l:
                if t in dql[k]:
                    
                    r,c,_,_,_,_=para(k)
                    n[k]=t
                    m[r,c]=t
                    k_l.remove(k)
                    flag=1
                    break            
    dql={}
    return m,n,flag

#check all available list in one square and find the value which only exist in one cell

def n_c(m,n):
    flag=0
    dql=dq_l(m,n)
    c_l=[x for x in range(0,9,3)]+[x for x in range(27,36,3)]+[x for x in range(54,63,3)]
    for i in range(9):
        la=[]
        u=c_l[i]
        n_l=[x for x in range(u,u+3)]+[x for x in range(u+9,u+12)]+[x for x in range(u+18,u+21)]
        k_l=[x for x in n_l if x in dql.keys()]
        for k in k_l:
            la+=dql[k]
        ct=Counter(la)
        lb=[]
        for j,v in ct.items():
            if v==1:
                lb.append(j)
        for t in lb:
            for k in k_l:
                if t in dql[k]:
                    r,c,_,_,_,_=para(k)
                    n[k]=t
                    m[r,c]=t
                    k_l.remove(k)
                    flag=1
                    break     
    dql={}
    return m,n,flag


#Solver1: Only use Recursive Loop:

def solver1(m,n):
    
    #find the last empty cell
    
    for i in reversed(range(1,81)):
        if n[i]==0:
            l=i
            break
    flag=0
    i=0
    flag=dg(m,n,i,l,flag)
    return m


#Solver2: loop search only value in available list first, then do the recursive loop

def solver2(m,n):
    
    flag=1
    while flag==1:
        m,n,flag=wy(m,n)
    
    
    l=0
    for i in reversed(range(1,81)):
        if n[i]==0:
            l=i
            break
    
    if l!=0:
        flag=0
        i=0
        flag=dg(m,n,i,l,flag)
        
    return m


#Solver3: loop check row, column and square, then do the recursive loop

def solver3(m,n):

    flag=1
    
    while flag==1:
        
        m,n,flag=h_c(m,n)
        m,n,flag=v_c(m,n)
        m,n,flag=n_c(m,n)
    
    l=0
    for i in reversed(range(1,81)):
        if n[i]==0:
            l=i
            break
    if l!=0:
        i=0
        flag=0
        flag=dg(m,n,i,l,flag)

    return m

# generate result

if __name__ == "__main__":
    
    m,n=readdata()
    
#     Solver1
    st1=time.time()
    m_res1=solver1(m,n)
    ut1=time.time()-st1
    print(m_res1,ut1)
    
#     Solver2
    st2=time.time()
    m_res2=solver2(m,n)
    ut2=time.time()-st2
    print(m_res2,ut2)

#     solver3
    st3=time.time()
    m_res3=solver3(m,n)
    ut3=time.time()-st3
    print(m_res3,ut3)


# In[ ]:




