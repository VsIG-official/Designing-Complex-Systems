# -*- coding: utf-8 -*-
"""DCS-Lab2-Valentyn-Dominskyi-IP-93.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LBol3yxJo3QsI2KU6gXfPfVoUMPkmCMY
"""

from random import randint, uniform
from threading import Thread, Lock
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import pandas as pd
import os
import time
import matplotlib.pyplot as plt

MIN_FLOAT_VALUE = 0.0
MAX_FLOAT_VALUE = 25.0
MIN_FLOAT_EXPONENT = 2
MAX_FLOAT_EXPONENT = 4

DIM_RANGE = range(110, 190)

EXCEL_NAME = 'values.xlsx'

DATA_COLUMNS = ['vector_b','vector_d','vector_e','matrix_mc', 'matrix_mz', 'matrix_mm', 'matrix_mt', 'matrix_me']
RESULT_FILE = "result.txt"

FIRST_PLOT = "А=В*МС+D*MZ+E*MM"
SECOND_PLOT = "MG=min(D+E)*MM*MT-MZ*ME"

class LabMathConstructs:
  def vector(self, d):
    return np.array(
        [
            round(
                uniform(MIN_FLOAT_VALUE, MAX_FLOAT_VALUE), 
                randint(MIN_FLOAT_EXPONENT, MAX_FLOAT_EXPONENT)
            ) 
            for _ in range(d)
          ]
    )

  def matrix(self, d):
    matrix = np.array(
        [
            round(
                uniform(MIN_FLOAT_VALUE, MAX_FLOAT_VALUE), 
                randint(MIN_FLOAT_EXPONENT, MAX_FLOAT_EXPONENT)
            )
            for _ in range(d ** 2)
        ]
    )
    return matrix.reshape((d, d))

mc = LabMathConstructs()

vector_b = [mc.vector(d) for d in DIM_RANGE]
vector_d = [mc.vector(d) for d in DIM_RANGE]
vector_e = [mc.vector(d) for d in DIM_RANGE]
matrix_mc = [mc.matrix(d) for d in DIM_RANGE]
matrix_mz = [mc.matrix(d) for d in DIM_RANGE]
matrix_mm = [mc.matrix(d) for d in DIM_RANGE]
matrix_mt = [mc.matrix(d) for d in DIM_RANGE]
matrix_me = [mc.matrix(d) for d in DIM_RANGE]

df = pd.DataFrame(list(zip(vector_b, vector_d, vector_e, matrix_mc, matrix_mz, matrix_mm, matrix_mt, matrix_me)), columns=DATA_COLUMNS)
df.to_excel(EXCEL_NAME)
df.head()

if (os.path.exists(RESULT_FILE)):
  os.remove(RESULT_FILE)

threadLock = Lock()

def save_result_as_file(text):
  file = open(RESULT_FILE, "a")
  file.write(f"{text}")
  file.close()

class FirstStatement:
  def b_dot_mc(self, b, mc):
    return np.dot(b, mc)

  def d_dot_mz(self, d, mz):
    return np.dot(d, mz)

  def e_dot_mm(self, e, mm):
    return np.dot(e, mm)

  def result_a(self, b_dot_mc, d_dot_mz, e_dot_mm):
    res = np.add(b_dot_mc, np.add(d_dot_mz, e_dot_mm))
    save_result_as_file(res)
    print(res)

class SecondStatement:
  def min_d_add_e(self, d, e):
    return np.amin(np.add(d, e))

  def mm_dot_mt(self, mm, mt):
    return np.dot(mm, mt)

  def mz_dot_me(self, mz, me):
    return np.dot(mz, me)

  def result_mg(self, min_d_add_e, mm_dot_mt, mz_dot_me):
    res = np.subtract(np.dot(min_d_add_e, mm_dot_mt), mz_dot_me)
    save_result_as_file(res)
    print(res)

class LabFirstThread:
    def __init__(self):
      self.fs = FirstStatement()
      self.first_thread_result = None
      self.second_thread_result = None
      self.third_thread_result = None

    def first_thread(self, b, mc): 
        result = self.fs.b_dot_mc(b, mc)
        
        threadLock.acquire()
        self.first_thread_result = result
        threadLock.release()

    def second_thread(self, d, mz):
        result = self.fs.d_dot_mz(d, mz)

        threadLock.acquire()
        self.second_thread_result = result
        threadLock.release()

    def third_thread(self, e, mm):
        result = self.fs.e_dot_mm(e, mm)

        threadLock.acquire()
        self.third_thread_result = result
        threadLock.release()

    def fourth_thread(self):
        if self.first_thread_result.all() and self.second_thread_result.all() and self.third_thread_result.all():
            self.fs.result_a(self.first_thread_result, self.second_thread_result, self.third_thread_result)

class LabSecondThread:
    def __init__(self):
      self.ss = SecondStatement()
      self.first_thread_result = None
      self.second_thread_result = None
      self.third_thread_result = None

    def first_thread(self, d, e):
        result = self.ss.min_d_add_e(d, e)

        threadLock.acquire()
        self.first_thread_result = result
        threadLock.release()

    def second_thread(self, mm, mt):
        result = self.ss.mm_dot_mt(mm, mt)

        threadLock.acquire()
        self.second_thread_result = result
        threadLock.release()

    def third_thread(self, mz, me):
        result = self.ss.mz_dot_me(mz, me)

        threadLock.acquire()
        self.third_thread_result  = result
        threadLock.release()

    def fourth_thread(self):
        if self.first_thread_result.all() and self.second_thread_result.all() and self.third_thread_result.all():
            self.ss.result_mg(self.first_thread_result, self.second_thread_result, self.third_thread_result)

class LabRuns:
  def __init__(self):
    self.xs_1_1 = []
    self.ys_1_1 = []

    self.xs_1_2 = []
    self.ys_1_2 = []

    self.xs_2_1 = []
    self.ys_2_1 = []

    self.xs_2_2 = []
    self.ys_2_2 = []

    self.starting_time = 0
    self.ending_time = 0
    self.actual_time = 0

  def start_time(self, thread_num, run_num):
      self.starting_time = time.time()
      self.print_thread_start(thread_num, run_num)

  def end_time(self):
      self.ending_time = time.time()
      self.actual_time = self.ending_time - self.starting_time

  def print_thread_start(self, thread_num, run_num):
    print(f"Start Thread #{thread_num}_{run_num}")

  def run_first_thread_first_run(self, i):
    fs = FirstStatement()

    thread = Thread(target=fs.result_a, args=[fs.b_dot_mc(vector_b[i], matrix_mc[i]), fs.d_dot_mz(vector_d[i], matrix_mz[i]), fs.e_dot_mm(vector_e[i], matrix_mm[i]),],)
    thread.start()
    thread.join()

  def run_second_thread_first_run(self, i):
    ss = SecondStatement()

    thread = Thread(target=ss.result_mg, args=[ss.min_d_add_e(vector_d[i], vector_e[i]), ss.mm_dot_mt(matrix_mm[i], matrix_mt[i]), ss.mz_dot_me(matrix_mz[i], matrix_me[i]),],)
    thread.start()
    thread.join()

  def first_run(self):
    for i in range(0, len(DIM_RANGE)):
        self.ys_1_1.append(len(vector_b[i]))
        
        self.start_time(i + 1, 1)
        self.run_first_thread_first_run(i)
        self.end_time()

        self.xs_1_1.append(self.actual_time)
        self.ys_1_2.append(len(vector_b[i]))
        
        self.start_time(i + 1, 2)
        self.run_second_thread_first_run(i)
        self.end_time()
        
        self.xs_1_2.append(self.actual_time)

  def run_first_threads_second_run(self, i):
    self.ys_2_1.append(len(vector_b[i]))

    mainThread = LabFirstThread()

    self.start_time(i + 1, 1)

    with ThreadPoolExecutor(max_workers=4) as executor:
        future1 = executor.submit(lambda: mainThread.first_thread(vector_b[i], matrix_mc[i]))
        future2 = executor.submit(lambda: mainThread.second_thread(vector_d[i], matrix_mz[i]))
        future3 = executor.submit(lambda: mainThread.third_thread(vector_e[i], matrix_mm[i]))

        future1.result()
        future2.result()
        future3.result()

        future4 = executor.submit(lambda: mainThread.fourth_thread())

        future4.result()
        
        executor.shutdown()

    self.end_time()

    self.xs_2_1.append(self.actual_time)
    self.ys_2_2.append(len(vector_b[i]))

  def run_second_threads_second_run(self, i):
        mainThread = LabSecondThread()

        self.start_time(i + 1, 2)

        with ThreadPoolExecutor(max_workers=4) as executor:
            future1 = executor.submit(lambda: mainThread.first_thread(vector_d[i], vector_e[i]))
            future2 = executor.submit(lambda: mainThread.second_thread(matrix_mm[i], matrix_mt[i]))
            future3 = executor.submit(lambda: mainThread.third_thread(matrix_mz[i], matrix_me[i]))

            future1.result()
            future2.result()
            future3.result()

            future4 = executor.submit(lambda: mainThread.fourth_thread())

            future4.result()

            executor.shutdown()

        self.end_time()
        self.xs_2_2.append(self.actual_time)

  def second_run(self):
    for i in range(0, len(DIM_RANGE)):
        self.run_first_threads_second_run(i)
        self.run_second_threads_second_run(i)

runs = LabRuns()

runs.first_run()

runs.second_run()

plt.title(FIRST_PLOT)
plt.xlim(0, 0.045)
plt.plot(runs.xs_1_1, runs.ys_1_1)
plt.plot(runs.xs_2_1, runs.ys_2_1)
plt.show()

plt.title(SECOND_PLOT)
plt.xlim(0, 0.045)
plt.plot(runs.xs_1_2, runs.ys_1_2)
plt.plot(runs.xs_2_2, runs.ys_2_2)
plt.show()