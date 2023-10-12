import pandas as pd
import numpy as np
import sympy
from sympy import *
from tqdm import tqdm
from chap1_codes import *
from chap2_codes import *
from typing import *


# libor结算表
def libor_detail(freq: float,
                 base_money: float, 
                 libor: list, 
                 r: float,
                 end_time: float,
                 ):
    #   libor = [10, 9.2, 8.5, 8, 7.6, 7.2, 6.6]
    #   kwargs = {'freq':2, 'base_money':100, 'libor':libor, 'r':8.1, 'end_time':3}
    r = r * 0.01 / freq
    libor = [i * 0.01 / freq for i in libor]
    T = end_time * freq
    profits = []
    for t in range(int(T)+1): #签约日起
        profits.append(libor[t] - r)
    return [format(i*100, '.3f') for i in profits]
    
# 给定债券，转换因子，求收益
# 流程：先算期货报价*转换因子，再算可交割券报价

    

if __name__ == '__main__':
    libor = [10, 9.2, 8.5, 8, 7.6, 7.2, 6.6]
    kwargs = {'freq':2, 'base_money':100, 'libor':libor, 'r':8.1, 'end_time':3}
    ans = libor_detail(**kwargs)
    print(ans)