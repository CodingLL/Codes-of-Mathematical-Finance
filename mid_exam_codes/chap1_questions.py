import pandas as pd
import numpy as np
import sympy
from sympy import *
from tqdm import tqdm
from chap1_codes import *



class chap1():
    #输入为dict
    def Q1(kwargs):
        #题型1: 贷款求等额本金还款，等额本息还款的支付利息总额
        '''
        args:
        freq: 每年还款频率
        r: 年利率*100(如6。表示6%)
        base_money:借款金额
        end_time:借款期限
        '''
        # 参数示例：
        # kwargs = {'freq':1, 'r':6, 'base_money':100, 'end_time':10}
        benxi = equal_interest(**kwargs)
        benjin = equal_benjin(**kwargs)
        print('等额本金还款{:.3f}万元利息\n等额本息还款共{:.3f}万元利息'.
              format(benjin, benxi))
    def Q2(kwargs):
        #题型2： 求债券价格
        '''
        args:
        freq: 每年付息频率
        r: 到期收益率
        bond_r: 息票率
        bond_face: 债券面值
        end_time: 剩余期限
        start_time: 期初,一般为0
        '''
        # 参数示例：
        # kwargs = {'freq':2, 'r':8, 'bond_r':10, 'bond_face':1000, 'end_time':10, 'start_time':0}
        price = get_V(**kwargs)
        print('债券现值为：{:.3f}'.format(price))
        
    def Q3(kwargs):
        #题型3： 求债券收益率
        '''
        args:
        freq: 每年付息频率
        bond_r: 息票率
        bond_face: 债券面值
        bond_cur: 债券现值（价格）
        end_time: 剩余期限
        start_time: 期初,一般为0
        '''
        # 参数示例：
        # kwargs = {'freq':1, 'bond_r':6, 'bond_face':1000, 'bond_cur':750 ,'end_time':10, 'start_time':3}
        r = get_r(**kwargs)
        print('债券收益率为：{:.3f}'.format(r))
        
    
    def Q4(kwargs):
        #题型4:1. 给定债券面值，期限，价格，求到期收益率，久期，凸度
        #     2. 给定到期收益率的情况，求久期，凸度
        '''
        e.g. 设某债券的面值为 bond_face 元，息票率(票面利率)为 bond_r,每年付息两次，剩余为期限 end_time,
        当前交易的全价为bond_cur元,求该债券的到期收益率,修正久期,以及凸度。
        这里剩余期限可以正好是交易日,也可以不是,见chap1 ppt29页
        args:
        freq: 每年付息频率
        r: 到期收益率
        bond_r: 息票率
        bond_face: 债券面值
        bond_cur: 债券现值（价格）
        end_time: 剩余期限
        start_time: 期初,一般为0
        '''
        # 参数示例：
        # 1. kwargs = {'freq':2, 'bond_r':9, 'bond_face':100, 'bond_cur':95, 'end_time':6+2/12, 'start_time':0}
        # 2. kwargs = {'freq':2, 'r':6, 'bond_r':5,  'end_time':10, 'start_time':0}
        if 'r' not in kwargs:
            r = get_r(**kwargs)
            duartion = get_bond_duration2(**kwargs, r = r,)
            convexity = get_convexity2(**kwargs, r = r,)
            print('到期收益率{:.3f}, 修正久期{:.3f}(年), 凸度{:.3f}(年)'.format(r, duartion, convexity))
        else:
            bond_face = 100 #最后会被消掉，无所谓取值
            bond_cur = get_bond_price_discount(**kwargs, bond_face=bond_face)
            duartion = get_bond_duration2(**kwargs, bond_cur=bond_cur, bond_face=bond_face)
            convexity = get_convexity2(**kwargs, bond_cur=bond_cur, bond_face=bond_face)
            print('修正久期{:.3f}(年), 凸度{:.3f}(年)'.format(duartion, convexity))

    def Q5(kwargs1, kwargs2, kwargs3, r_new):
        #题型5: 给定3种债券在到期时间抵债，分别比较到期收益率上升/下降时的盈亏
        '''
        args:
        freq: 每年付息频率
        r: 到期收益率
        bond_r: 息票率
        bond_final: 债券到期时抵债的价格
        cur_time: 债务剩余期限
        end_time: 债券剩余期限
        start_time: 期初,一般为0
        r_new: 变化的到期收益率
        '''
        # 参数示例：
        # kwargs1 = {'freq':1, 'r':6, 'bond_r':6.7, 'bond_final':1790.85, 'cur_time':10, 'end_time':10}
        # kwargs2 = {'freq':1, 'r':6, 'bond_r':6.988, 'bond_final':1790.85, 'cur_time':10, 'end_time':15}
        # kwargs3 = {'freq':1, 'r':6, 'bond_r':5.9, 'bond_final':1790.85, 'cur_time':10, 'end_time':30}
        # r_new = 5
        # ans.Q5(kwargs1, kwargs2, kwargs3, r_new)
        
        V_a = get_bond_face(**kwargs1)
        V_b = get_bond_face(**kwargs2)
        V_c = get_bond_face(**kwargs3)
        print('债券A需要买面值{:.3f},\n 债券B需要买面值{:.3f},\n债券C需要买面值{:.3f}\n'.
              format(V_a, V_b, V_c))
        
        kwargs1['r'] = r_new
        kwargs2['r'] = r_new
        kwargs3['r'] = r_new
        
        bondA_rnew = get_bond_price_cur(**kwargs1, bond_face=V_a)
        bondB_rnew = get_bond_price_cur(**kwargs2, bond_face=V_b)
        bondC_rnew = get_bond_price_cur(**kwargs3, bond_face=V_c)
        
        print('新到期收益率{:.1f}%下,\n债券A到还债时价格{:.3f},\n债券B到还债时价格{:.3f},\n债券C到还债时价格{:.3f},\n'.
              format(r_new, bondA_rnew, bondB_rnew, bondC_rnew))
    




if __name__ == '__main__':
    # ans = chap1
    # kwargs1 = {'freq':1, 'r':6, 'bond_r':6.7, 'bond_final':1790.85, 'cur_time':10, 'end_time':10}
    # kwargs2 = {'freq':1, 'r':6, 'bond_r':6.988, 'bond_final':1790.85, 'cur_time':10, 'end_time':15}
    # kwargs3 = {'freq':1, 'r':6, 'bond_r':5.9, 'bond_final':1790.85, 'cur_time':10, 'end_time':30}
    # r_new = 5
    # ans.Q5(kwargs1, kwargs2, kwargs3, r_new)
    # kwargs = {'freq':2, 'bond_r':9, 'bond_face':100, 'bond_cur':95, 'end_time':6+2/12, 'start_time':0}
    # chap1.Q4(kwargs)
    # 模拟题：给定债券每年的即期收益率，来求债券现值，到期收益率，久期和凸度
    freq = 1
    rt = [6, 8 ,9]
    bond_r = 9
    bond_face = 100
    end_time = 3
    rt = [0.01 * i / freq for i in rt]
    bond_r = 0.01 * bond_r / freq
    end_time = end_time * freq
    V = bond_face/(1+rt[-1])**end_time
    for t in range(end_time):
        V += bond_face * bond_r / (1 + rt[t]) ** (t + 1)
    print('现值:', V)
    kwargs = {'freq':freq, 'bond_r':bond_r*freq*100, 'bond_cur':V, 'bond_face':bond_face, 'end_time':end_time/freq, 'start_time':0}
    chap1.Q4(kwargs)