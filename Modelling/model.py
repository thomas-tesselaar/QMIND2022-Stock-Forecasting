#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 18:40:12 2023

@author: thomastesselaar
"""


import pandas as pd
import numpy as np
import sys
sys.path.append("../DataPreprocessing")
# from DataPreprocessing 
import data_preprocessing as data_prep
# sys.path.append("../Data")
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score


def main():

  
  
  pass




def get_data():
  stock_name = 'TSLA'
  search_names = ['Term'+str(i) for i in range(1,8)]
  main_df = data_prep.merge_csv(stock_name, search_names, search_suffix = '', pathname = "../Modelling/", print_head = False, stock_rows_to_drop=[0,1,522])
  data_prep.derive_columns(main_df, len(search_names), print_head = False)
  clean_df = data_prep.prep_for_learning(main_df, normalize = 'min-max')

  test_df = clean_df.sample(frac=(2/10))

  train_df = clean_df.drop(index = test_df.index)

  test_y = test_df["Price Movement"].to_numpy()
  test_x = test_df.drop(columns = "Price Movement").to_numpy()

  train_y = train_df["Price Movement"].to_numpy()
  train_x = train_df.drop(columns = "Price Movement").to_numpy()
  
  return test_x, test_y, train_x, train_y

def fit_data(train_x, train_y):
  clf = MLPClassifier(hidden_layer_sizes=(6,5),
  random_state=5,
  verbose=True,
  learning_rate_init=0.01)

  clf.fit(train_x, train_y)
  return clf
  
def predict(test_x, test_y, train_x, train_y):
  clf = fit_data(train_x, train_y)
  ypred = clf.predict(test_x)
  a_score = accuracy_score(test_y, ypred)
  return a_score, ypred, test_y


test_x, test_y, train_x, train_y = get_data()
score, preds, test_y = predict(test_x, test_y, train_x, train_y)

print(score)
print(preds)
print(test_y)


