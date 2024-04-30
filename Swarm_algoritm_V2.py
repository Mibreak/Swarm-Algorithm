from functions import *
from math import *
import random as rnd
import matplotlib.pyplot as plt
import imageio
import os
import csv

class Unit:
    def __init__(self, dimension, lower_bounds, upper_bounds, currentVelocityRatio, localVelocityRatio, globalVelocityRatio, function):
        # область поиска
        self.lower_bounds = lower_bounds
        self.upper_bounds = upper_bounds
        # размерность решаемой задачи
        self.dimension = dimension
        # коэффициенты для изменения скорости
        self.currentVelocityRatio = currentVelocityRatio
        self.localVelocityRatio = localVelocityRatio
        self.globalVelocityRatio = globalVelocityRatio
        # функция
        self.function = function
        # лучшая локальная позиция
        self.localBestPos = self.getFirsPos()
        self.localBestScore = self.function(*self.localBestPos)
        # текущая позиция
        self.currentPos = self.localBestPos[:]
        self.score = self.function(*self.localBestPos)
        # значение глобальной позиции
        self.globalBestPos = []
        # скорость
        self.velocity = self.getFirstVelocity()

    def getFirstVelocity(self):
        """ Метод для задания первоначальной скорости"""
        minvals = [lower - upper for lower, upper in zip(self.lower_bounds, self.upper_bounds)]
        maxvals = [upper - lower for lower, upper in zip(self.lower_bounds, self.upper_bounds)]
        return [rnd.uniform(minval, maxval) for minval, maxval in zip(minvals, maxvals)]

    def getFirsPos(self):
        """ Метод для получения начальной позиции"""
        return [rnd.uniform(lower, upper) for lower, upper in zip(self.lower_bounds, self.upper_bounds)]

    def nextIteration(self):
        """ Метод для нахождения новой позиции частицы"""
        # случайные данные для изменения скорости
        rndCurrentBestPosition = [rnd.random() for _ in range(self.dimension)]
        rndGlobalBestPosition = [rnd.random() for _ in range(self.dimension)]
        # делаем перерасчет скорости частицы исходя из всех введенных параметров
        velocityRatio = self.localVelocityRatio + self.globalVelocityRatio
        commonVelocityRatio = 2 * self.currentVelocityRatio / abs(2-velocityRatio-sqrt(velocityRatio ** 2 - 4 * velocityRatio))
        multLocal = list(map(lambda x: x * commonVelocityRatio * self.localVelocityRatio, rndCurrentBestPosition))
        betweenLocalAndCurPos = [self.localBestPos[i] - self.currentPos[i] for i in range(self.dimension)]
        betweenGlobalAndCurPos = [self.globalBestPos[i] - self.currentPos[i] for i in range(self.dimension)]
        multGlobal = list(map(lambda x: x * commonVelocityRatio * self.globalVelocityRatio, rndGlobalBestPosition))
        newVelocity1 = list(map(lambda coord: coord * commonVelocityRatio, self.velocity))
        newVelocity2 = [coord1 * coord2 for coord1, coord2 in zip(multLocal, betweenLocalAndCurPos)]
        newVelocity3 = [coord1 * coord2 for coord1, coord2 in zip(multGlobal, betweenGlobalAndCurPos)]
        self.velocity = [coord1 + coord2 + coord3 for coord1, coord2, coord3 in zip(newVelocity1, newVelocity2, newVelocity3)]
        # передвигаем частицу и смотрим, какое значение целевой функции получается
        self.currentPos = [coord1 + coord2 for coord1, coord2 in zip(self.currentPos, self.velocity)]
        newScore = self.function(*self.currentPos)
        if newScore < self.localBestScore:
            self.localBestPos = self.currentPos[:]
            self.localBestScore = newScore
        return newScore



class Swarm:
    def __init__(self, sizeSwarm, dimension, currentVelocityRatio, localVelocityRatio, globalVelocityRatio, numbersOfLife, function, start, end, accuracy):
        # размер популяции частиц
        self.sizeSwarm = sizeSwarm
        # размерность решаемой задачи
        self.dimension = dimension
        # коэффициенты изменения скорости
        self.currentVelocityRatio = currentVelocityRatio
        self.localVelocityRatio = localVelocityRatio
        self.globalVelocityRatio = globalVelocityRatio
        # Размерность (количество итераций алгоритма)
        self.numbersOfLife = numbersOfLife
        # функция для поиска экстремума
        self.function = function
        # область поиска
        self.start = start
        self.end = end
        # рой частиц
        self.swarm = []
        # данные о лучшей позиции
        self.globalBestPos = []
        self.globalBestScore = float('inf')
        self.globalBestScoreList = []
        #количество итераций
        self.iteration_count = 0
        self.accuracy = accuracy
        # создаем рой
        self.createSwarm()

    def createSwarm(self):
        """ Метод для создания нового роя"""
        pack = [self.dimension, self.start, self.end, self.currentVelocityRatio, self.localVelocityRatio, self.globalVelocityRatio, self.function]
        self.swarm = [Unit(*pack) for _ in range(self.sizeSwarm)]
        # пересчитываем лучшее значение для только что созданного роя
        for unit in self.swarm:
            if unit.localBestScore < self.globalBestScore:
                self.globalBestScore = unit.localBestScore
                self.globalBestPos = unit.localBestPos

    def startSwarm(self):
        """ Метод для запуска алгоритма"""
        dataForGIF = []
        check = False
        for _ in range(self.numbersOfLife):
            oneDataX = []
            oneDataY = []
            if (check):
                break
            for unit in self.swarm:
                oneDataX.append(unit.currentPos[0])
                oneDataY.append(unit.currentPos[1])
                unit.globalBestPos = self.globalBestPos
                score = unit.nextIteration()
                if (score < self.globalBestScore):
                    self.globalBestScore = score
                    self.globalBestPos = unit.localBestPos
                    self.globalBestScoreList.append(self.globalBestScore)
                    print("Iteration:", self.iteration_count, "BestScore:", self.globalBestScore, "BestPosition:", self.globalBestPos)
                    if (self.globalBestScore <= self.accuracy ):
                        print("Required accuracy reached!", self.globalBestScore)
                        print("Number of iterations:", self.iteration_count)
                        check = True
                        break
            dataForGIF.append([oneDataX, oneDataY])
            self.iteration_count += 1
            # Check if the specified accuracy is reached
            

        # Запись результатов в CSV файл
       
        with open('results5.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Iteration', 'BestScore', 'BestPosition'])
            for i, (score, pos) in enumerate(zip(self.globalBestScoreList, self.globalBestPos)):
                writer.writerow([i, score, pos])

size_swarm = 650
dimesion = 2
inertia = 0.1
local_velocity = 2
global_velocity = 5
iterations = 1000
lower_bounds = [-20, -5]
upper_bounds = [20, 5]
accuracy = pow(10, -6)
a = Swarm(size_swarm, dimesion, inertia, local_velocity, global_velocity, iterations, Griewank, lower_bounds, upper_bounds, accuracy)
a.startSwarm()
print("Размерность решаемой задачи:", a.dimension)
print("Конечный РЕЗУЛЬТАТ:", a.globalBestScore, "Конечный В ТОЧКЕ:",a.globalBestPos)
