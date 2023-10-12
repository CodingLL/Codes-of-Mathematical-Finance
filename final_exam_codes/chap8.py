import numpy as np
import math
import copy
from scipy.stats import norm

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def tree_lay(root, u, d, T, sp_level=None, sp_r=None, sp_v=None):
    res = []
    stack = [root]
    level = 0

    while stack and level <= T:
        lay, lay_val = [], []
        while stack:
            cur = stack.pop(0)
            if level in sp_level:
                #派息
                if sp_r:
                    cur.left = TreeNode(cur.val * d * (1 - sp_r))
                    cur.right = TreeNode(cur.val * u * (1 - sp_r))
                elif sp_v:
                    cur.left = TreeNode(cur.val * (d- sp_v))
                    cur.right = TreeNode(cur.val * (u - sp_v))
            else:
                cur.left = TreeNode(cur.val * d)
                cur.right = TreeNode(cur.val * u)
            lay.append(cur.left)
            lay.append(cur.right)
            lay_val.append(np.round(cur.val,3))

        res.append(sorted(list(set(lay_val))))
        stack = lay
        level += 1
    return res

def post_process(res, K, r, p, sp_level=None, sp_r=None, sp_v=None, mode = 'C'):
    print('====================START====================')
    T = len(res)
    new_res = copy.deepcopy(res)
    post_res = []
    for i in range(T-1, 0, -1):
        if mode == 'C':
            print(f'-------看涨期权，第{i - 1}周期-------')
        else:
            print(f'-------看跌期权，第{i - 1}周期-------')
        C_a = []
        cur = res[i]
        cur_new = new_res[i]
        if mode == 'C':
            pre_cur = [max(i - K, 0) for i in res[i - 1]]
            # 看涨，风险中性概率下期望贴现
            expect = [np.exp(-r) * ((1 - p) * max(cur_new[i] - K, 0) + p * max(cur_new[i+1] - K, 0)) for i in range(len(cur_new) - 1)]
        else:
            if i-1 in sp_level:
                if sp_r:
                    pre_cur = [max(K - t * (1 - sp_r), 0) for t in res[i - 1]] #派息后作为当前价值依据
                elif sp_v:
                    pre_cur = [max(K - (t- sp_v), 0) for t in res[i - 1]]  # 派息后作为当前价值依据
            else:
                pre_cur = [max(K - t, 0) for t in res[i - 1]]
            # 看跌， 风险中性概率下期望贴现
            expect = [np.exp(-r) * ((1 - p) * max(K - cur_new[i], 0) + p * max(K - cur_new[i+1], 0)) for i in range(len(cur) - 1)]
        for j in range(len(expect)):
            # 看跌期权，需要维护一个派发利息后的价格list
            if mode == 'P':
                if i-1 in sp_level:
                    if sp_r:
                        new_res[i-1][j] *= (1 - sp_r)
                    elif sp_v:
                        new_res[i - 1][j] -= sp_v

            if pre_cur[j] > expect[j]:
                # 更新res中的元素，取风险中性下期望贴现和价值的较高项
                C_a.append(np.round(pre_cur[j], 3))
            else:
                C_a.append(np.round(expect[j], 3))
                new_res[i - 1][j] = expect[j] + K if mode == 'C' else K - expect[j]
        print('当前价值: {}\n风险中性下期望贴现: {}\n较高项: {}'.format(pre_cur, expect, C_a))
        post_res.insert(0, C_a)

    if mode == 'C':
        print('美式看涨期权定价:{:.3f}'.format(post_res[0][0]))
    else:
        print('美式看跌期权定价:{:.3f}'.format(post_res[0][0]))
    print('====================END====================\n')
    return post_res

def BS(S, K, t, sigma, r, mu=None, sp=None,):
    d1 = 1 / (sigma * np.sqrt(t)) * (np.log(S / K) + (r + sigma**2 / 2) * t)
    d2 = d1 - sigma * np.sqrt(t)
    C = S * norm.cdf(d1) - K * np.exp(-r * t) * norm.cdf(d2)
    D = K * np.exp(-r * t) * norm.cdf(-d2) - S * norm.cdf(-d1)
    if mu:
        tmp = (np.log(K) - (np.log(S) + (mu - sigma**2 / 2) * t )) / (sigma * np.sqrt(t))
        prob = norm.cdf(tmp)
        print('看涨被执行概率: {:.3f}'.format(1 - prob))
        print('看跌被执行概率: {:.3f}'.format(prob))
        if sp:
            tmp_sp = (np.log(sp) - (np.log(S) + (mu - sigma**2 / 2) * t )) / (sigma * np.sqrt(t))
            prob_sp = norm.cdf(tmp_sp)
            print('S(t)<sp概率: {:.3f}'.format(prob_sp))
    print('d1: {:.3f}, d2: {:.3f}, 看涨期权价格: {:.3f}, 看跌期权价格: {:.3f}'.format(d1, d2, C, D))

if __name__ == '__main__':
    # 以期权作业7补充3为例
    # 参数设定
    r = 0.02
    u = 1.1
    d = 0.9
    S = 50
    K = 50
    q = 0.1
    T = 4
    p = (1 + r - d)/(u - d) #风险中性概率
    sp_level = [2, 3]  # 派息周期
    sp_r = 0.1 #派息比例
    root = TreeNode(S)
    res = tree_lay(root, u, d, T, sp_level, sp_r)
    print('无派息期权二叉树:{}'.format(res))


    print('==============美式期权情况==============')
    post_res = post_process(res, K, r, p, sp_level, sp_r, mode='C')
    post_res = post_process(res, K, r, p, sp_level, sp_r, mode='P')



    print('==============欧式期权情况==============')
    C = [max(i - K, 0) for i in res[-1]][::-1] #从大到小排序，看涨期权
    P = [max(K - i, 0) for i in res[-1]][::-1]#从大到小排序，看跌期权
    print('看涨期权第{}周期价值：{}\n看跌期权第{}周期价值：{}'.format(T, [np.round(i, 3) for i in C], T, [np.round(i, 3) for i in P]))
    ans_C, ans_P = 0, 0
    for i in range(T+1):
        ans_C += (p ** (T - i)) * ((1 - p) ** (i)) * math.comb(T, i) * C[i] / (1 + r) ** T
    for i in range(T+1):
        ans_P += (p ** (T - i)) * ((1 - p) ** (i)) * math.comb(T, i) * P[i] / (1 + r) ** T
    print('看涨期权价格:{:.3f}\n看跌期权价格:{:.3f}'.format(ans_C, ans_P))