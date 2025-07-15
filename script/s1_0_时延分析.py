# -*- coding: utf-8 -*-
"""
Created on 2025/03/17 14:39:35

@File -> s1_0_时延分析.py

@Author: luolei

@Email: dreisteine262@163.com

@Describe: 分析给煤量ub和实际入炉燃料量rb之间的时延关系
"""

import numpy as np
import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), "../" * 2))
sys.path.insert(0, BASE_DIR)

from setting import plt
from mod.dir_file_op import load_pickle

if __name__ == "__main__":
    dataset = load_pickle("runtime/dataset.pkl")

    ub = np.array(dataset["ub"])
    rb = np.array(dataset["rb"])

    # 画图
    fig, ax = plt.subplots(figsize = (6, 6))
    ax.plot(ub, c="b", label="ub")
    ax.plot(rb, c="r", label="rb")
    ax.set_xlabel("Time")
    ax.set_ylabel("Value")
    ax.legend()
    plt.show()

    # ---- 进行时延相关分析 ---------------------------------------------------------------------------
    
    lags2test = np.arange(-10, 10 + 1, 1)

    corr_lst = []
    for lag in lags2test:
        ub_lag = np.roll(ub, lag)
        corr = np.corrcoef(ub_lag, rb)[0, 1]

        corr_lst.append(corr)

    # 画图
    fig, ax = plt.subplots(figsize = (6, 6))
    ax.plot(lags2test, corr_lst, c="b")
    ax.set_xlabel("Lag")
    ax.set_ylabel("Correlation")
    ax.axvline(0, c="r", linestyle="--")
    plt.show()

    """从图中结果可见，时延参数tau为0"""