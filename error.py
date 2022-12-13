#!/usr/bin/python

import pandas as pd

real = pd.read_excel('data/COV_train.xlsx').iloc[:, 1].values
pred = open('out/resumen_alu0101331720.txt').read().split('\n')

acierto = 0

n_tweets = len(real)

for i in range(n_tweets):
    if real[i].lower() == pred[i].lower():
        acierto += 1

pc_acierto = acierto / n_tweets * 100

color = ''
if pc_acierto <= 60:
    color = '\033[1;31m'
elif pc_acierto <= 75:
    color = '\033[1;33m'
elif pc_acierto <= 90:
    color = '\033[1;32m'
else:
    color = '\033[1;34m'

print('Porcentaje de acierto: \033[{}{}%\033[m'.format(color, round(pc_acierto, 2)))
