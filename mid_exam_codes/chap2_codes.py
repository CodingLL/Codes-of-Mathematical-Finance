import pandas as pd
import numpy as np
import sympy
from sympy import *
from tqdm import tqdm
from chap1_codes import *
from typing import *

def min_var_overall(mu: np.mat,
                    sigma: np.mat,):
    # kwargs = {'mu':np.mat([7/60,3.2/40]).T , 'sigma':np.mat([[50/60**2,0],[0,25/40**2]]).T, 'rp':8, 'rf':5}
    sigma_rev = np.linalg.inv(sigma)
    one = np.mat([1 for i in range(mu.shape[0])]).T
    denominator = one.T*sigma_rev*one
    print('mu:\n{},\n sigma_rev:\n{}'.format(mu, sigma_rev))
    print('方差', 1 / denominator)
    print('期望', mu.T*sigma_rev*one / denominator)
    
    print('c', denominator, 'b',mu.T*sigma_rev*one )
    return (sigma_rev*one)/denominator
    
def get_musigma_withrf(mu: np.mat,
                       sigma: np.mat,
                       rp: float,
                       rf: float,):
    rf /= 100
    rp /=100
    sigma_rev = np.linalg.inv(sigma)
    one = np.mat([1 for i in range(mu.shape[0])]).T1
    a = mu.T * sigma_rev * mu
    b = mu.T * sigma_rev * one
    c = one.T * sigma_rev * one
    H = a - 2 * b * rf + c * rf**2
    print('a:{}\nb:{}\nc:{}\nH:{}'.format(a, b, c, H))
    wp = float((rp - rf)/H) * sigma_rev *(mu - rf * one)
    w0 = (1 - one.T * wp)
    #print('w0:\n', res, '\nwp:\n',res2)
    std = float((rp - rf) ** 2 / H)**0.5
    print('收益标准差:{:.4f}'.format(std))
    return w0, wp

def get_musigma_norf(mu: np.mat,
                    sigma: np.mat,
                    rp: Optional[float]=None):
    # kwargs = {'mu':np.mat([1, 2, 0.5]).T , 'sigma':np.mat([[2, 3, 0],[3, 5, 0],[0, 0, 1]]).T}
    flag = True if rp else False
    if not flag:
        rp = sympy.Symbol('rp')
    sigma_rev = np.linalg.inv(sigma)
    one = np.mat([1 for i in range(mu.shape[0])]).T
    a = mu.T * sigma_rev * mu
    b = mu.T * sigma_rev * one
    c = one.T * sigma_rev * one
    delta = a * c - b ** 2
    print('a:{}\nb:{}\nc:{}\ndelta:{}'.format(a, b, c, delta))
    lam1 = (rp * c - b) / delta
    lam2 = (a - rp * b) / delta
    lam1 = lam1.tolist()[0][0]
    lam2 = lam2.tolist()[0][0]
    w = sigma_rev * (lam1 * mu + lam2 * one) #1,3
    w = np.array(w).reshape(3) #转变shape为3
    if not flag:
        sigma2 = c / delta * (rp - b / c) ** 2 + 1 / c
        print('方差-均值双曲线方程:sigma^2 =', sigma2)
        print('购买组合w表达式:\n', w)
        print('不允许卖空情况下,rp取值节点:')
        print(solve([w[0]], [rp]), solve([w[1]], [rp]), solve([w[2]], [rp]))
    return w

if __name__ == '__main__':
    # kwargs = {'mu':np.mat([1, 2, 0.5]).T , 'sigma':np.mat([[2, 3, 0],[3, 5, 0],[0, 0, 1]]).T}
    # res = get_musigma_norf(**kwargs)
    # print('========print_mode========')
    # print(res)
    
    kwargs = {'mu':np.mat([0.2, 0.3, 0.2]).T , 'sigma':np.mat([[1, 2, 0],[2, 5, 1],[0, 1, 2]]).T}
    res = min_var_overall(**kwargs)
    print(res)