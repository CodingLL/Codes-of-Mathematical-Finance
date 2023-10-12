import pandas as pd
import numpy as np
import sympy
from sympy import *
from tqdm import tqdm
from chap1_codes import *
from typing import *


def discount_rate(r, m, mode='cont'):
    if mode == 'cont':
        return 1 / np.exp(r * m)
    elif mode == 'single':
        return 1 / (1 + r * m)


def exchange_value1(freq, bond_rate, libor_rate, start_time, total_round, base_invent, mode='cont'):
    '''
    :param freq: 交易频率，以年为单位
    :param bond_rate: 债券面值利率
    :param libor_rate: libor利率
    :param start_time: 开始交易时间
    :param total_round: 总共的交易次数
    :param base_invent: 名义本金
    :param mode: 'single'表示单利，‘cont’表示连续利率
    :return: 返回现金流和合约价值
    '''
    #    kwargs = {'freq':2, 'bond_rate':4, 'libor_rate':[4.8,4.5,5,6], 'start_time': 0.25, 'total_round': 3, \
    #         'base_invent': 100, 'mode':'cont'}
    bond_rate = 0.01 * bond_rate / freq
    libor_rate = [0.01 * i for i in libor_rate]
    m = [i * 1 / freq - start_time for i in range(1, total_round + 1)]
    print('日期:', m)
    rate = []  # 贴现率
    last_libor = libor_rate.pop(0)
    for i in range(total_round):
        if mode == 'single':
            rate.append(1 / (1 + libor_rate[i] * m[i]))
        elif mode == 'cont':
            rate.append(1 / np.exp(libor_rate[i] * m[i]))
    print('贴现率:', rate)
    forward_r = last_libor / freq
    # if mode == 'single':
    B_fl = base_invent * (1 + forward_r)
    # else:#cont
    #     B_fl = base_invent * np.exp(forward_r)
    print('B_fl:', B_fl)
    B_fix = []
    B_fix_discount = []
    B_fl_discount = B_fl * rate[0]
    print('B_fl现金流:', B_fl_discount)
    for i in range(1, total_round):
        B_fix.append(base_invent * bond_rate)
    B_fix.append(base_invent * (1 + bond_rate))
    for i in range(0, total_round):
        B_fix_discount.append(B_fix[i] * rate[i])
    print('B_fix:', B_fix)
    print('B_fix现金流:', B_fix_discount)
    print('B_fix现金流合计:', sum(B_fix_discount))
    print('合约价值:', sum(B_fix_discount) - B_fl_discount)
    # return sum(B_fixnet) - B_flnet


def exchange_value2(freq, bond_rate, libor_rate, start_time, total_round, base_invent, mode='cont'):
    '''
    :param freq: 交易频率，以年为单位
    :param bond_rate: 债券面值利率
    :param libor_rate: libor利率
    :param start_time: 开始交易时间
    :param total_round: 总共的交易次数
    :param base_invent: 名义本金
    :param mode: 'single'表示单利，‘cont’表示连续利率
    :return: 返回现金流和合约价值
    '''
    #     kwargs = {'freq':2, 'bond_rate':4, 'libor_rate':[4.8,4.5,5,6], 'start_time': 0.25, 'total_round': 3, \
    #     'base_invent': 100, 'mode':'cont'}
    libor_rate = [0.01 * i for i in libor_rate]
    bond_rate = 0.01 * bond_rate / freq
    m = [i * 1 / freq - start_time for i in range(1, total_round + 1)]
    print('日期:', m)
    rate = []  # 贴现率
    last_libor = libor_rate.pop(0)
    for i in range(total_round):
        if mode == 'single':
            rate.append(1 / (1 + libor_rate[i] * m[i]))
        elif mode == 'cont':
            rate.append(1 / np.exp(libor_rate[i] * m[i]))
    print('贴现率:', rate)
    forward_r = [last_libor / freq]
    if mode == 'cont':
        for i in range(1, total_round):
            forward_r.append(np.exp(
                (12 / freq * i + start_time * 12) / 12 * libor_rate[i] - (12 / freq * i - start_time * 12) / 12 *
                libor_rate[i - 1]) - 1)
    elif mode == 'single':
        for i in range(1, total_round):
            forward_r.append((1 + (12 / freq * i + start_time * 12) / 12 * libor_rate[i]) / (
                        1 + (12 / freq * i - start_time * 12) / 12 * libor_rate[i - 1]) - 1)
    B_fl = base_invent * np.array(forward_r)
    print('B_fl:', B_fl.tolist())
    B_fix = base_invent * np.array([bond_rate for _ in range(total_round)])
    print('B_fix:', B_fix.tolist())
    clear_money = B_fix - B_fl
    print('B_net(B_fix - B_fl):', clear_money.tolist())
    clear_money_discount = np.array(clear_money) * np.array(rate)
    print('LIBOR净现金流现值:', clear_money_discount.tolist())
    print('合约价值:', np.sum(clear_money_discount).tolist())


if __name__ == '__main__':
    kwargs = {'freq': 2, 'bond_rate': 4, 'libor_rate': [4.8, 4.5, 5, 6], 'start_time': 0.25, 'total_round': 3, \
              'base_invent': 100, 'mode': 'single'}
    # exchange_value1(**kwargs)
    exchange_value2(**kwargs)
