import numpy as np
import random
import pandas as pd
import main_config as mc
import matplotlib.pyplot as plt

city_distance = pd.read_excel('dataset/最短路.xlsx')
city_distance.set_index('序号')
city_distance = city_distance.values[:, 1:]


class Sample:
    def __init__(self, routine=None):
        self.len = mc.getvalue('city_number')
        if routine is None:
            self.rout = [i for i in range(1, self.len+1)]
            random.shuffle(self.rout)
        else:
            self.rout = routine
        self.time_needed = self.get_time()

    def get_time(self):
        city_first = mc.getvalue("city_first")
        city_first_pos = self.rout.index(city_first)
        time1 = time2 = 0
        if city_first_pos != 0:
            time1 = city_distance[city_first-1][self.rout[0]-1]
            for i in range(city_first_pos):
                time1 += city_distance[self.rout[i]-1][self.rout[i + 1]-1]
        if city_first_pos != self.len - 1:
            for j in range(city_first_pos, self.len - 1):
                time2 += city_distance[self.rout[j]-1][self.rout[j + 1]-1]
            time2 += city_distance[self.rout[-1]-1][city_first-1]
        time = max(time1, time2)
        return time

    def len_bool(self):
        return self.len == 21


def new_sample(current_sample):
    a = random.randint(0, current_sample.len-2)
    b = random.randint(a, current_sample.len-1)
    revised = current_sample.rout[b:a:-1]
    new_one = current_sample.rout[:a+1] + revised + current_sample.rout[b+1:]
    new_one = Sample(new_one)
    return new_one


class SA:
    def __init__(self):
        self.city_number = mc.getvalue('city_number')
        self.city_first = mc.getvalue('city_first')
        self.times = mc.getvalue('times')
        self.num_epochs = mc.getvalue('num_epochs')
        self.current_temperate = mc.getvalue('initial_temperate')
        self.temperate_loss = mc.getvalue('temperate_loss')
        self.best_answer = []

    def prob(self, a, b):
        return np.exp(-(a-b)/self.current_temperate)

    def temperate_next(self):
        self.current_temperate *= self.temperate_loss

    def train(self):
        best_sample = current_sample = Sample()
        for _ in range(self.num_epochs):
            for _ in range(self.times):
                new_one = new_sample(current_sample)
                if new_one.time_needed < current_sample.time_needed:
                    current_sample = new_one
                    if new_one.time_needed < best_sample.time_needed:
                        best_sample = new_one
                elif random.random() < self.prob(new_one.time_needed, current_sample.time_needed):
                    current_sample = new_one
            self.best_answer.append(best_sample)
            self.temperate_next()
        print(self.best_answer[-1].rout)
        print(self.best_answer[-1].time_needed)
        plt.figure(figsize=(12, 8))
        plt.plot(np.arange(1, self.num_epochs+1), [i.time_needed for i in self.best_answer], c='red')
        plt.show()
