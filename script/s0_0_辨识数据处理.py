# -*- coding: utf-8 -*-
"""
Created on 2025/03/17 13:54:10

@File -> s0_0_辨识数据处理.py

@Author: luolei

@Email: dreisteine262@163.com

@Describe: 辨识数据处理
"""

from scipy.io import loadmat
import numpy as np
import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), "../" * 2))
sys.path.insert(0, BASE_DIR)

from setting import plt
from setting import U_COLS, X_COLS, Y_COLS
from mod.dir_file_op import save_pickle


if __name__ == "__main__":
    # 输入变量：给煤指令、给水量、阀门开度
    ub = loadmat(f"{BASE_DIR}/data/辨识数据/ub.mat")["ub"]
    Dfw = loadmat(f"{BASE_DIR}/data/辨识数据/Dfw.mat")["Dfw"]
    ut = loadmat(f"{BASE_DIR}/data/辨识数据/ut.mat")["ut"]

    ub = np.array(ub).flatten()
    Dfw = np.array(Dfw).flatten()
    ut = np.array(ut).flatten()

    # 输出变量：主汽压力、中间点焓值、机组功率
    Pst = loadmat(f"{BASE_DIR}/data/辨识数据/Pst.mat")["Pst"]
    hm = loadmat(f"{BASE_DIR}/data/辨识数据/hm.mat")["hm"]
    Ne = loadmat(f"{BASE_DIR}/data/辨识数据/Ne.mat")["Ne"]

    Pst = np.array(Pst).flatten()
    hm = np.array(hm).flatten()
    Ne = np.array(Ne).flatten()

    # 状态量：入炉燃料量、中间点压力、中间点焓值
    rb = loadmat(f"{BASE_DIR}/data/辨识数据/rb.mat")["rb"]
    Pm = loadmat(f"{BASE_DIR}/data/辨识数据/Pm.mat")["Pm"]
    # hm = loadmat(f"{BASE_DIR}/data/辨识数据/hm.mat")["hm"]

    rb = np.array(rb).flatten()
    Pm = np.array(Pm).flatten()
    # hm = np.array(hm).flatten()

    # 状态量：入炉燃料量、中间点压力、中间点焓值
    rb_init = 181.63
    Pm_init = 24
    hm_init = 2441.5

    # ---- 保存数据 ---------------------------------------------------------------------------------

    dataset = {
        "ub": ub,
        "Dfw": Dfw,
        "ut": ut,
        "Pst": Pst,
        "hm": hm,
        "Ne": Ne,
        "rb": rb,
        "Pm": Pm,
        "rb_init": rb_init,
        "Pm_init": Pm_init,
        "hm_init": hm_init,
    }

    if "runtime" not in os.listdir():
        os.makedirs("runtime")

    save_pickle(dataset, "runtime/dataset.pkl")
    
    # ---- 数据作图 ---------------------------------------------------------------------------------

    plt.figure(figsize = (12, 6))

    fig, axs = plt.subplots(3, 3, figsize = (10, 6))

    # 输入变量
    for i, col in enumerate(U_COLS):
        axs[0, i].plot(dataset[col], label = col)
        axs[0, i].set_title(col)
        axs[0, i].legend()

    # 状态变量
    for i, col in enumerate(X_COLS):
        axs[1, i].plot(dataset[col], label = col)
        axs[1, i].set_title(col)
        axs[1, i].legend()

    # 输出变量
    for i, col in enumerate(Y_COLS):
        axs[2, i].plot(dataset[col], label = col)
        axs[2, i].set_title(col)
        axs[2, i].legend()

    plt.tight_layout()
    plt.show()
