# -*- coding: utf-8 -*-
"""
Created on 2025/03/13 15:42:20

@File -> s2_1_动态过程前向模拟.py

@Author: luolei

@Email: dreisteine262@163.com

@Describe: 动态过程前向模拟
"""

import pandas as pd
import numpy as np
import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), "../" * 2))
sys.path.insert(0, BASE_DIR)

from setting import plt
from setting import U_COLS, X_COLS, Y_COLS
from mod.dir_file_op import load_pickle


class LinearParamModel(object):
    """线性参数模型"""

    def __init__(self, a: float, b: float):
        self.a = a
        self.b = b

    def __call__(self, x: float) -> float:
        return self.a * x + self.b
    

class DynamicModel(object):
    """动态模型"""

    def __init__(self, params_dict: dict):
        self.c0 = params_dict["c0"]
        self.c1 = params_dict["c1"]
        self.c2 = params_dict["c2"]

        self.d1 = params_dict["d1"]
        self.d2 = params_dict["d2"]

        """模型内部的l、k0、k1、g、f、h都是双参数线性模型"""

        self.l_a = params_dict["l_a"]
        self.l_b = params_dict["l_b"]
        self.l = LinearParamModel(self.l_a, self.l_b)

        self.k0_a = params_dict["k0_a"]
        self.k0_b = params_dict["k0_b"]
        self.k0 = LinearParamModel(self.k0_a, self.k0_b)

        self.k1_a = params_dict["k1_a"]
        self.k1_b = params_dict["k1_b"]
        self.k1 = LinearParamModel(self.k1_a, self.k1_b)

        self.hfw = 1200

        self.g_a = params_dict["g_a"]
        self.g_b = params_dict["g_b"]
        self.g = LinearParamModel(self.g_a, self.g_b)

        self.f_a = params_dict["f_a"]
        self.f_b = params_dict["f_b"]
        self.f = LinearParamModel(self.f_a, self.f_b)

        self.h_a = params_dict["h_a"]
        self.h_b = params_dict["h_b"]
        self.h = LinearParamModel(self.h_a, self.h_b)

    def cal_step_k(self, X_k: np.ndarray, U_k: np.ndarray, dt: float):
        """计算第k步的信息"""

        X_k = X_k.flatten()
        U_k = U_k.flatten()

        rb, Pm, hm = X_k
        _, _, _ = U_k

        Pst = Pm - self.g(Pm)
        
        A = np.array([
            [-1 / self.c0, 0, 0],
            [self.k0(rb) / self.c1, 0, 0],
            [self.k0(rb) / self.c2, 0, 0]
        ])

        B = np.array([
            [1 / self.c0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ])
        B[1, 1] = (self.hfw - self.d1) / self.c1
        B[1, 2] = self.f(Pst) * (self.h(Pst) - self.hfw) * (self.d1 - self.l(Pm) * hm) / self.c1 / 100 / (self.l(Pm) * hm - self.hfw)
        B[2, 1] = (self.hfw - self.d2) / self.c2
        B[2, 2] = self.f(Pst) * (self.h(Pst) - self.hfw) * (self.d2 - self.l(Pm) * hm) / self.c2 / 100 / (self.l(Pm) * hm - self.hfw)

        C = np.array([
            [Pst],
            [hm],
            [0]
        ])

        D = np.array([
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, self.k1(Pm) * self.f(Pst) * (self.h(Pst) - self.hfw) / 100]
        ])

        X_inc_k = (A @ X_k.reshape(-1, 1) + B @ U_k.reshape(-1, 1)) * dt
        Y_k = C + D @ U_k.reshape(-1, 1)

        return X_inc_k, Y_k
        

if __name__ == "__main__":
    dataset = load_pickle("runtime/dataset.pkl")

    # ---- 整理数据表 --------------------------------------------------------------------------------

    df = pd.DataFrame()

    for col in U_COLS + X_COLS:
        df[col] = dataset[col]

    """
    首先使用来自文档辨识出的参数结果，代入到模型中进行模拟，查看是否与实际数据吻合，从而验证方程结构是否正确

    注意：
    - 后续将使用NSGA-II算法对以下params_dict中的参数进行辨识
    """

    params_dict = {
        "c0": 1.128,
        "c1": 2.6736e+06,
        "c2": 4.6636e+05,
        "d1": 799.9997,
        "d2": 5.0000e+04,
        "l_a": 0.0024,
        "l_b": 1.2478,
        "k0_a": -13.9851,
        "k0_b": 12747,
        "k1_a": 1.25E-6,
        "k1_b": 1.28E-4,
        "g_a": 0.0709,
        "g_b": -0.0116,
        "f_a": 48.213,
        "f_b": -17.68,
        "h_a": -11.116,
        "h_b": 3616.5
        }

    self = DynamicModel(params_dict)

    # ---- 前向模拟 ----------------------------------------------------------------------------------
    
    k = 0
    X_k = np.array([df.iloc[k]["rb"], df.iloc[k]["Pm"], df.iloc[k]["hm"]]).reshape(-1, 1)
    U_k = np.array([df.iloc[k]["ub"], df.iloc[k]["Dfw"], df.iloc[k]["ut"]]).reshape(-1, 1)

    """离散间隔取为1"""

    dt = 1

    X_inc_k, Y_k = self.cal_step_k(X_k, U_k, dt)

    X_arr = X_k
    U_arr = U_k
    Y_arr = Y_k

    for k in range(1, len(df)):
        X_k = X_k + X_inc_k
        U_k = np.array([df.iloc[k]["ub"], df.iloc[k]["Dfw"], df.iloc[k]["ut"]]).reshape(-1, 1)
        X_inc_k, Y_k = self.cal_step_k(X_k, U_k, dt)

        # 记录当前步的状态量和输出量
        X_arr = np.hstack((X_arr, X_k))
        U_arr = np.hstack((U_arr, U_k))
        Y_arr = np.hstack((Y_arr, Y_k))

    # ---- 数据作图 ---------------------------------------------------------------------------------

    plt.figure(figsize = (12, 6))

    fig, axs = plt.subplots(3, 3, figsize = (10, 6))

    # 输入变量
    for i, col in enumerate(U_COLS):
        axs[0, i].plot(U_arr[i, :], label = col)
        axs[0, i].set_title(col)
        axs[0, i].legend()

    # 状态变量
    for i, col in enumerate(X_COLS):
        axs[1, i].plot(X_arr[i, :], label = col)
        axs[1, i].set_title(col)
        axs[1, i].legend()

    # 输出变量
    for i, col in enumerate(Y_COLS):
        axs[2, i].plot(Y_arr[i, :], label = col)
        axs[2, i].set_title(col)
        axs[2, i].legend()

    plt.tight_layout()
    plt.show()







