.\src\vocabulary\vocabulary.py -i .\data\COV_train.xlsx -o .\out\vocabulary.txt
.\src\language_model.py -i .\data\COV_train.xlsx -o .\out\language_model
.\src\clasificator.py -i data\COV_test.xlsx -o out
.\error.py