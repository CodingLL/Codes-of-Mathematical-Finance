import numpy as np
import math
from scipy.stats import norm

if __name__ == '__main__':
    # 参数
    S = 49
    K = 50
    r = 0.05
    sigma = 0.2
    T_t = 20 / 52  # 20周(年)
    init_count = 100000  # 多少股的看涨期权
    S_price = [49, 48 + 1 / 8, 47 + 3 / 8]
    S_count = 0
    cum_cost = 0
    print('{:<5}  {:<5}{:<5}  {:<5}   {:<5}   {:<5}   {:<5}'.format('周', '股票价格', 'delta', '购买股票数', '购买股票成本', '累计成本',
                                                                    '利息费用'))

    for t in range(len(S_price)):
        d1 = 1 / (sigma * np.sqrt(T_t - t / 52)) * (np.log(S_price[t] / K) + (r + sigma ** 2 / 2) * (T_t - t / 52))
        delta = norm.cdf(d1)
        S_count_new = delta * init_count  # 新周期需要S_count份股票对冲

        S_change = S_count_new - S_count
        cost = S_change * S_price[t]
        cum_cost += cost
        interest = cum_cost * (np.exp(r * (1 / 52)) - 1)

        print(
            '{:<5d}   {:<5.3f}  {:<5.3f}  {:<5.3f}  {:<5.3f}  {:<5.3f} {:<5.3f}'.format(t, S_price[t], delta, S_change,
                                                                                        cost, cum_cost, interest))
        cum_cost += interest  # 下周期结算本周期利息
        S_count = S_count_new

    # 原本盈亏
    origin_diff = max((S_price[-1] - K) * init_count, 0)
    # 对冲盈亏
    impact_diff = K * init_count - cum_cost
    # 最终盈亏
    final_diff = impact_diff + origin_diff
    print('期权盈亏: {:.3f}\n对冲盈亏: {:.3f}\n最终盈亏: {:.3f}'.format(origin_diff, impact_diff, final_diff))