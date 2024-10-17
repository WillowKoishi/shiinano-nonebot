import ctypes
import os
import time
import pandas as pd
import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def GADSM(sequence_str: str, year_0_str: str, year_1_str: str, C_3: str):

    cur_path = os.path.dirname(__file__)
    GADSM_path = os.path.join(cur_path, "GADSM")
    if not os.path.exists(GADSM_path):
        os.makedirs(GADSM_path)

    time_str = time.strftime("%Y%m%d%H%M%S", time.localtime())
    csv_path = os.path.join(GADSM_path, time_str + ".csv")
    
    sequence_list = list(sequence_str)
    sequence = list(range(3))
    sequence[0] = int(sequence_list[0])
    sequence[1] = int(sequence_list[1])
    sequence[2] = int(sequence_list[2])
    year_0 = int(year_0_str)
    year_1 = int(year_1_str)
    C_3 = float(C_3)

    csv_path_c = ctypes.c_char_p(csv_path.encode("utf-8"))
    sequence_c = (ctypes.c_int * 3)(*sequence)
    year_0_c = ctypes.c_int(year_0)
    year_1_c = ctypes.c_int(year_1)
    C_3_c = ctypes.c_double(C_3)

    dll_path = os.path.join(cur_path, "GADSM.dll")

    GADSM_dll = ctypes.WinDLL(dll_path)
    MS = ctypes.c_int(5) # 多启动次数
    pop = ctypes.c_int(100) # 种群数量
    gen = ctypes.c_int(2000) # 迭代次数
    err = GADSM_dll.GADSM_for_bot(csv_path_c, sequence_c, year_0_c, year_1_c, C_3_c, MS, pop, gen)

    if err == 0:
        data = pd.read_csv(csv_path)

        date = np.array(data[["date"]])
        t_1_str = date[0][0]
        t_2_str = date[202][0]
        t_3_str = date[-1][0]

        dv_xys = np.array(data[["dv_x", "dv_y", "dv_z"]])
        dv_1 = np.linalg.norm(dv_xys[101][:]) * 1000
        dv_2 = np.linalg.norm(dv_xys[303][:]) * 1000

        v_inf_xys = np.array(data[["v_inf_x", "v_inf_y", "v_inf_z"]])
        C_3_f = np.linalg.norm(v_inf_xys[-1][:]) ** 2

        r = np.array(data[["r_x", "r_y"]])

        eph_path = os.path.join(cur_path, "EPH")
        eph_list = os.listdir(eph_path)

        data = pd.read_csv(os.path.join(eph_path, eph_list[sequence[0] - 1]), sep=" ", header=None)
        r_planet_1 = np.array(data.iloc[:, 0:2])
        data = pd.read_csv(os.path.join(eph_path, eph_list[sequence[1] - 1]), sep=" ", header=None)
        r_planet_2 = np.array(data.iloc[:, 0:2])
        data = pd.read_csv(os.path.join(eph_path, eph_list[sequence[2] - 1]), sep=" ", header=None)
        r_planet_3 = np.array(data.iloc[:, 0:2])

        plt.figure(figsize=(12,9))
        img = plt.imread("C:\\Users\\Administrator\\shiinano\\src\\img\\gadsm\\GADSM底图.png")

        # plt.xkcd(scale=0.5, length=50, randomness=1)
        # plt.text(0, 0, "SETI", fontsize=180, color="gray", ha="center", va="center", alpha=0.1)
        plt.plot(0, 0, "o", color="darkred")
        plt.plot(r_planet_1[:, 0], r_planet_1[:, 1], color="#aaaaaa", linewidth=1)
        plt.plot(r_planet_2[:, 0], r_planet_2[:, 1], color="#aaaaaa", linewidth=1)
        plt.plot(r_planet_3[:, 0], r_planet_3[:, 1], color="#aaaaaa", linewidth=1)

        plt.plot(r[:, 0], r[:, 1], color="#1E90FF", linewidth=0.7)
        plt.plot(r[:, 0], r[:, 1], color="#1E90FF", linewidth=0.7)
        plt.plot(r[:, 0], r[:, 1], color="#1E90FF", linewidth=0.7)

        plt.plot(r[0, 0], r[0, 1], ".", color="mediumblue")
        plt.plot(r[202, 0], r[202, 1], ".", color="mediumblue")
        plt.plot(r[-1, 0], r[-1, 1], ".", color="mediumblue")

        plt.plot(r[101, 0], r[101, 1], ".", color="dodgerblue")
        plt.plot(r[303, 0], r[303, 1], ".", color="dodgerblue")
        plt.xlabel("X (AU)")
        plt.ylabel("Y (AU)")
        plt.axis("equal")
        plt.grid(linestyle='--', linewidth=0.5)
        #plt.imsave(GADSM_path, time_str + ".png", format="png")
        plt.figimage(img, 0, 0, alpha=1)
        plt.savefig(os.path.join(GADSM_path, time_str + ".png"))
        #plt.show()

        # return [(
        #     "出发时间：%s，"
        #     + "借力时间：%s，"
        #     + "到达时间：%s，"
        #     + "深空机动ΔV：[%.1f, %.1f] m/s，"
        #     + "到达C3：%.2f km^2/s^2"
        # ) % (t_1_str, t_2_str, t_3_str, dv_1, dv_2, C_3_f),f"{time_str}.png"]
        return [f"出发时间:{t_1_str},借力时间：{t_2_str}到达时间：{t_3_str}深空机动ΔV：[{round(dv_1,3)}m/s,{round(dv_2)}m/s]到达C3：{round(C_3_f,4)}km²/s²",f"{time_str}.png"]
    elif err == 1:
        return "Write result into CSV error"
    elif err == -11:
        return "sequence[0] out of range"
    elif err == -12:
        return "sequence[1] out of range"
    elif err == -13:
        return "sequence[2] out of range"
    elif err == -21:
        return "year_0 out of range"
    elif err == -31:
        return "year_1 out of range"
    elif err == -32:
        return "year_1 not big than year_0"
    elif err == -41:
        return "C_3 out of range"
    else:
        return "Unknown error"


def GADSM_demo():
    sequence = "225"
    year_0 = "2025"
    year_1 = "2030"
    C_3 = "30"
    result = GADSM(sequence, year_0, year_1, C_3)
    print(result)
    return result

def calcu_GADSM(seq:str,y1:str,y2:str,c3:str):
    result = GADSM(seq, y1, y2, c3)
    print(result)
    return result

if __name__ == "__main__":
    GADSM_demo()
