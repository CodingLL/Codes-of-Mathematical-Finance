import pandas as pd
import numpy as np
import sympy
from sympy import *
from tqdm import tqdm

#   贴现
def discount(freq, r, final_value, end_time, *args, **kwargs):
    return final_value/(1+0.01*r/freq)**(end_time*freq)
    
#   辅助函数，求表达式
def get_V(freq, 
           r, 
           bond_r, 
           bond_face,
           end_time,
           start_time = 0,
           *args, **kwargs):
    bond_r = 0.01*bond_r/freq
    r = 0.01*r/freq 
    end_time -= start_time 
    end_time *= freq
    T = end_time
    result = bond_face / (1 + r) ** int(T)
    if int(T) == T:
        for t in range(1, int(T) + 1):
            result +=  bond_face * bond_r / (1 + r) ** t
        return result
    else:
        for t in range(0, int(T)+1):
            result +=  bond_face * bond_r / (1 + r) ** t
        return result / ((1+r) ** (((T) - int(T)) / (1 / freq)))
        
#   求到期收益率
def get_r(freq, 
          bond_r, 
          bond_face, 
          bond_cur,
          end_time,
          start_time = 0):
    r = sympy.Symbol('r')
    fr = get_V(freq, r, bond_r, bond_face, end_time, start_time) - bond_cur
    # 直接解
    # r0 = sympy.solve([fr],[r])[0][0]
    # 牛顿法：
    fr_diff = fr.diff(r)
    r0 = 10
    # 精度要求，当误差小于此值时，结束迭代
    prec = 1e-5
    # 最多迭代15次
    for idx in tqdm(range(15)):
        fr_val= float(limit(fr, r, r0))
        #print(i, r0, fr_val)
        if abs(fr_val) <= prec:
            break
        diff_fr_val = float(limit(fr_diff, r, r0))
        #print('\n',fr.diff(r),diff_fr_val)
        r0 -= fr_val / diff_fr_val
    return r0
        
#   求求到要买多少债券面值才能抵债，可以直接得到解析式
#   辅助函数，求表达式，见书本P27
def get_fx(freq, 
            r, 
            bond_r, 
            bond_face, 
            bond_cur, 
            bond_final, 
            cur_time, 
            start_time=0):
    result = bond_final
    bond_r = 0.01*bond_r/freq
    r = 0.01*r/freq
    T = (cur_time - start_time) * freq
    for t in range(0, int(T)):
        result -= bond_face * bond_r * (1 + r) ** t
    return result

#   求到要买多少债券面值才能抵债
def get_bond_face(freq, 
                  r, 
                  bond_r, 
                  bond_final, 
                  end_time, 
                  cur_time,
                  *args, **kwargs):
    '''
    args:
    freq: 每年付息次数
    cur_time: 还债期限
    end_time: 债券年限
    r: 市场收益率*100, 如6表示6%
    bond_r: 债券息票率
    bond_face: 面值
    '''
    bond_face = sympy.Symbol('bond_face')
    bond_cur = get_bond_price_discount(freq=freq, r=r, bond_r=bond_r, bond_face=bond_face, end_time=end_time, start_time=cur_time)
    #print(bond_cur)
    fr = get_fx(freq=freq, r=r, bond_r=bond_r, bond_face=bond_face, bond_cur=bond_cur, bond_final=bond_final, cur_time=cur_time) - bond_cur
    fr_diff = fr.diff(bond_face)
    bond_face0 = 1000
    # 精度要求，当误差小于此值时，结束迭代
    prec = 1e-4
    # 最多迭代20次
    for i in range(15):
        fr_val= float(limit(fr, bond_face, bond_face0))
        #print(i, bond_face0, fr_val)
        if abs(fr_val) <= prec:
            break
        diff_fr_val = float(limit(fr_diff, bond_face, bond_face0))
        #print('\n',fr.diff(r),diff_fr)
        bond_face0 -= fr_val / diff_fr_val
    return bond_face0


#   获取债券贴现价格
def get_bond_price_discount(freq, 
                            r, 
                            bond_r, 
                            bond_face, 
                            end_time, 
                            start_time=0,
                            *args, **kwargs):
    '''
    args:
    freq: 每年付息次数
    start_time: 期初
    end_time: 债券年限
    r: 市场收益率*100, 如6表示6%
    bond_r: 债券息票率
    bond_face: 面值
    '''
    
    start_time *= freq
    end_time *= freq
    time_gap = end_time-start_time
    r = 0.01*r/freq
    bond_r = 0.01*bond_r/freq
    bond_price = bond_face/(1+r)**time_gap
    for i in range(1, int(time_gap)+1):
        bond_price += bond_face*bond_r/((1+r)**i)
    return bond_price

#   获取债券终值价格
def get_bond_price_final(freq, 
                         r, 
                         bond_r, 
                         bond_face, 
                         end_time, 
                         start_time=0,
                         *args, **kwargs):
    '''
    args:
    freq: 每年付息次数
    start_time: 期初(一般为0)
    end_time: 期初+债券年限
    cur_time: 当前时点
    r: 市场收益率*100, 如6表示6%
    bond_r: 债券息票率
    bond_face: 面值
    '''
    end_time -= start_time
    end_time *= freq
    time_gap = end_time
    r = 0.01*r/freq
    bond_r = 0.01*bond_r/freq
    bond_price = bond_face
    for i in range(0, int(time_gap)):
        bond_price += bond_face*bond_r*((1+r)**i)
    return bond_price

#   获取中间某时间点债券价格
def get_bond_price_cur(freq, 
                       r, 
                       bond_r, 
                       bond_face, 
                       cur_time, 
                       end_time, 
                       start_time=0,
                       *args, **kwargs):
    end_time -= start_time
    cur_time -= start_time
    T = (cur_time - start_time)*freq
    bond_price = get_bond_price_discount(freq=freq, r=r, bond_r=bond_r, bond_face=bond_face, end_time=end_time, start_time=cur_time)
    r = 0.01*r/freq
    bond_r = 0.01*bond_r/freq
    for t in range(int(T)):
        bond_price += bond_face*bond_r*((1+r)**t)
    return bond_price


#   计算修正久期，单位为年
def get_bond_duration(freq, 
                      r, 
                      bond_r, 
                      bond_face, 
                      bond_cur, 
                      end_time, 
                      start_time=0,
                      *args, **kwargs):
    '''
    args:
    T: 债券剩余年限
    bond_cur: 债券现值
    '''
    r = 0.01*r/freq
    bond_r = 0.01*bond_r/freq
    T = (end_time - start_time) * freq
    duration = T*bond_face/(1+r)**(T+1)/(freq)
    for t in range(1, int(T)+1):
        duration += t*bond_face*bond_r/(1+r)**(t+1)/(freq)
    return duration/bond_cur

def get_convexity(freq, 
                  r, 
                  bond_r, 
                  bond_face, 
                  bond_cur,
                  end_time, 
                  start_time=0,
                  *args, **kwargs):
    r = 0.01*r/freq
    bond_r = 0.01*bond_r/freq
    T = (end_time - start_time) * freq
    convexity = T*(T+1)*bond_face/(1+r)**(T+2)/(freq**2)
    for t in range(1, int(T)+1):
        convexity += t*(t+1)*bond_face*bond_r/(1+r)**(t+2)/(freq**2)
    return convexity/bond_cur
        
#   直接通过表达式求导计算修正久期，单位为年
def get_bond_duration2(freq, 
                    r, 
                    bond_r, 
                    bond_face, 
                    bond_cur, 
                    end_time, 
                    start_time=0,
                    *args, **kwargs):
    r0 = r
    r = sympy.Symbol('r')
    fr = get_V(freq, r, bond_r, bond_face, end_time, start_time)
    fr_diff = fr.diff(r)

    return -100 * float(limit(fr_diff, r, r0))/bond_cur #get_V中变量r前有个系数0.01，这里求导会带上，这里抵消它乘100 * 100
        
#   直接通过表达式求导计算修正久期，单位为年
def get_convexity2(freq, 
                    r, 
                    bond_r, 
                    bond_face, 
                    bond_cur, 
                    end_time, 
                    start_time=0):
    r0 = r
    r = sympy.Symbol('r')
    fr = get_V(freq, r, bond_r, bond_face, end_time, start_time)
    fr_diff = fr.diff(r)
    fr_diff2 = fr_diff.diff(r)
    return 100 * 100 * float(limit(fr_diff2, r, r0))/bond_cur #get_V中变量r前有个系数0.01，这里求导会带上，这里抵消它乘100 * 100

# 等额本息还款，求总利息
def equal_interest(freq, 
                   r, 
                   base_money, 
                   end_time,
                   *args, **kwargs):
    r = 0.01*r/freq
    T = end_time * freq
    interest_freq = base_money * (1 + r) ** T * r / ((1 + r) ** T - 1)
    return T * interest_freq - base_money #每月偿还利息，共计偿还利息
    
# 等额本金还款，求总利息
def equal_benjin(freq, 
                 r, 
                 base_money, 
                 end_time,
                 *args, **kwargs):
    r = 0.01*r/freq
    T = end_time * freq
    interest = 0
    #interest_detail = []
    for t in range(1, T+1):
        interest_month = base_money * (t/T) * r
        interest += interest_month
        #interest_detail.append(interest_month)
    return interest #共计偿还利息
    
    
    
if __name__ == '__main__':
    # res = equal_interest(freq=1,
    #                      r=6,
    #                      base_money=100,
    #                      end_time=10)
    
    # res2 = equal_benjin(freq=1,
    #                      r=6,
    #                      base_money=100,
    #                      end_time=10)
    # res = get_bond_price_final(freq=2,
    #            start_time=0,
    #            end_time=5.5,
    #            r=10,
    #            bond_r=12.5,
    #            bond_face=8820262)
    # res = get_bond_duration(freq=2, 
    #                         r=12.5, 
    #                         bond_r=12.5,
    #                         T=5.5, 
    #                         bond_face=8820262, 
    #                         bond_cur=8820262)
    
    # price = get_bond_price_discount(freq=1, r=11, bond_r=8, bond_face=1, end_time=5, start_time=0)
    # res = get_bond_duration(freq=1, 
    #                         r=11, 
    #                         bond_r=8,
    #                         T=5, 
    #                         bond_face=1, 
    #                         bond_cur=price)
    # res = get_convexity(freq=2, 
    #                     r=10.91, 
    #                     bond_r=9,
    #                     T=8, 
    #                     bond_face=100, 
    #                     bond_cur=90)
    
    # res = get_bond_price_cur(freq=2, r=12.5, bond_r=10.125, bond_face=10**7, cur_time=5.5, end_time=8, start_time=0)
    # res2 = get_bond_price_discount(freq=2, r=12.5, bond_r=10.125, bond_face=10**7, end_time=8, start_time=5.5)
    
    #   标准到期日，求收益率，久期，凸度
    args = {'freq':2, 'bond_r':9, 'bond_face':100, 'bond_cur':95, 'end_time':6+2/12}
    res = get_r(**args)
    res2 = get_bond_duration2(**args,
                              r=res,)
    res3 = get_convexity2(**args,
                          r=res,)
    # print(res, '\n', res2, '\n', res3)
    #   全价，非标准到期日，求收益率，久期，凸度
    # res = get_r(freq=2, 
    #             bond_r=9, 
    #             bond_face=100, 
    #             bond_cur=95,
    #             end_time=6+2/12)
    # res2 = get_bond_duration(freq=2, 
    #                          r=res,
    #                          bond_r=9, 
    #                          bond_face=100, 
    #                          bond_cur=90,
    #                          end_time=8)
    # res3 = get_convexity(freq=2, 
    #                      r=res,
    #                      bond_r=9, 
    #                      bond_face=100, 
    #                      bond_cur=90,
    #                     end_time=8)
    #print(res)
    print(res, '\n', res2, '\n', res3)
    