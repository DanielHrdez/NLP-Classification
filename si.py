import pandas as pd

train = pd.read_excel('data/test/COV_train.xlsx', header=None)
# test is the random middle of the train
test = train.sample(frac=0.5, random_state=1)

# remove the test from the train
train = train.drop(test.index)

# export test
test.to_excel('data/test/COV_test.xlsx', header=None)
# export train
train.to_excel('data/test/COV_train.xlsx', header=None)
