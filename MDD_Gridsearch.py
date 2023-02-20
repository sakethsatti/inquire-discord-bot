import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
import json

data = pd.read_csv("application_data.csv\\DataFinalBalanced.csv")

y = data["TARGET"]
X = data.drop(["TARGET"], axis = 1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25)

hyperparameter_dictionary={
                            'C':[0.01,0.1,10]
}

gridsearch=GridSearchCV(SVC(verbose=True),hyperparameter_dictionary,n_jobs=-1,verbose=3,refit=True)

gridsearch.fit(X_train,y_train)

print(gridsearch.best_estimator_)
print(gridsearch.best_score)

with open("GS_results.json", "w") as f:
    json.dump(gridsearch.cv_results_, f)