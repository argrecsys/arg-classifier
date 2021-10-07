# -*- coding: utf-8 -*-
"""
Created on Thu Oct  7 06:58:05 2021

@author: ansegura
"""
import matplotlib.pyplot as plt

# since sklearn 0.22, you can use sklearn.metrics.plot_confusion_matrix()
def plot_confusion_matrix(matrix):
    """If you prefer color and a colorbar"""
    fig = plt.figure(figsize=(8,8))
    ax = fig.add_subplot(111)
    cax = ax.matshow(matrix, cmap=plt.cm.gray)
    fig.colorbar(cax)