import numpy as np
import pdb
import scipy


class polynomial():
    def __init__(self,q,d=None,coeficient=None):
        self.q = q
        self.q_ = (q-1)//2
        if d:
            self.d = d
        else:
            self.d = len(coeficient)

        if isinstance(coeficient,np.ndarray):
            self.coeficient = coeficient.copy()
        elif isinstance(coeficient,list):
            self.coeficient = np.array(coeficient,dtype = np.int)
        else:
            self.coeficient = np.zeros(self.d,np.int)
        self.reduce()

    @property
    def copy(self):
        ans = polynomial(self.q,self.d)
        ans.coeficient = self.coeficient.copy()
        return ans

    def __repr__(self):
        return 'polynomial with coeficient {}'.format(self.coeficient)

    def reduce(self):
        self.coeficient = (self.coeficient+self.q_)%self.q-self.q_

    def __add__(self,other):
        ans = self.copy
        ans.coeficient += other.coeficient
        ans.q = max(ans.q,other.q)
        ans.q_ = (ans.q-1)//2
        ans.reduce()
        return ans

    def __sub__(self,other):
        ans = self.copy
        ans.coeficient -= other.coeficient
        ans.q = max(ans.q,other.q)
        ans.q_ = (ans.q-1)//2
        ans.reduce()
        return ans
    
    def __truediv__(self,other):
        try:
            ratio = float(other)
            ans = self.copy
            ans.coeficient = (ans.coeficient/ratio).astype(np.int)
            ans.reduce()
            return ans
        except:
            raise TypeError('the type must be a polynomial or can be interpred as a float, got {}'.format(type(other)))

    def __mul__(self,other):
        if type(self)==type(other):
            assert self.d == other.d, 'dimension mismatch'
            temp = np.zeros([self.d,self.d],np.int)
            for i in range(self.d):
                temp[i]=np.roll(other.coeficient,-1-i,0)
            mask = np.arange(self.d).reshape(-1,1).repeat(self.d,-1)
            mask_ = np.arange(self.d)
            mask = mask>mask_
            mask = np.flip(mask,0)
            mask = 1-2*mask
            temp = temp*mask
            temp2 = np.flip(self.coeficient,0)
            ans = temp2.dot(mask).view()
            ans = polynomial(max(self.q,other.q),self.d,ans)
            return ans
        
        try :
            ratio = float(other)
            ans = self.copy
            ans.coeficient = (ratio*ans.coeficient).astype(np.int)
            ans.reduce()
            return ans
        except TypeError:
            raise TypeError('the type must be a polynomial or can be interpred as a float, got {}'.format(type(other)))

    def __idiv(self,other):
        self = self/other

    def __imul__(self,other):
        self = self*other

    def __iadd__(self,other):
        self = self+other

    def __isub__(self,other):
        self = self/other

    def __neg__(self):
        ans = self.copy
        ans.coeficient = -ans.coeficient
    
def private_key(d=10):
    ans = polynomial(q=3,coeficient=np.random.randint(-1,2,d))
    return ans

def random_poly(q,d=10):
    ans = polynomial(q=q,coeficient=np.random.randint(-(q//2),q-1-q//2,d))
    return ans
def gaus_poly(std,d=10):
    coe = np.random.normal(0,std,d).astype(np.int)
    t1 = max(coe[coe>0])*2
    t2 = min(coe[coe<0])*-2+1
    t = max(t1,t2)
    ans = polynomial(t,coeficient=coe)
    return ans

def public_key(q,s,std=None):
    a = random_poly(q,s.d)
    if std==None:
        std = q/100
    return (gaus_poly(std,s.d)-a*s,a)

def both_key(q,d,std=None):
    s = private_key(d)
    pk = public_key(q,s,std)
    return s,pk

def encrypt(pk,m,std=None):
    if std==None:
        std = pk[0].q/100
    e1 = gaus_poly(std,pk[0].d)
    e2 = gaus_poly(std,pk[0].d)
    u = private_key(pk[0].d)
    q = pk[0].q
    t = m.q
    m.q = q
    return pk[0]*u+e1+m*(q/t),pk[1]*u+e2

def decrypt(ct,s,t):
    ans = ct[0]+ct[1]*s
    ans *= t/ans.q
    ans.q = t
    ans.reduce()
    return ans