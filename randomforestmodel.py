#Downloaded Colab Notebook

#Creating dataframe with data
import pandas as pd
import numpy as np
import math

def check_nan(arr):
  for x in arr:
    if math.isnan(x):
      x = 0.0

CAT_data = pd.read_excel("New_CAT_Data.xlsx", index_col=0)
NonCAT_data = pd.read_excel("New_NonCAT_Data.xlsx", index_col=0)
CAT_data = CAT_data[np.isnan(CAT_data['Direction']) == False]
windshear_target = np.ones(len(CAT_data))
CAT_data['Target'] = windshear_target
windshear2_target = np.zeros(len(NonCAT_data))
NonCAT_data['Target'] = windshear2_target
new_data = pd.concat([CAT_data, NonCAT_data], ignore_index=True).sample(frac=1)

#View Average CAT vs NonCAT Magnitude & Direction
CAT_mag = CAT_data['Magnitude'].to_numpy()
CAT_dir = CAT_data['Direction'].to_numpy()
NonCAT_mag = NonCAT_data['Magnitude'].to_numpy()
NonCAT_dir = NonCAT_data['Direction'].to_numpy()
print(f"Average CAT Magnitude: {round(sum(CAT_mag) / len(CAT_mag), 2)}")
print(f"Average CAT Direction: {round(sum(abs(CAT_dir)) / len(CAT_dir), 2)}")
print(f"Average NonCAT Magnitude: {round(sum(NonCAT_mag) / len(NonCAT_mag), 2)}")
print(f"Average NonCAT Direction: {round(sum(abs(NonCAT_dir)) / len(NonCAT_dir), 2)}")

#Setting up models
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import xgboost
from xgboost import XGBClassifier
X_train, X_test, y_train, y_test = train_test_split(new_data.drop(['Target'], axis='columns'), new_data['Target'], test_size=0.1, random_state=42)
model = RandomForestClassifier(n_estimators=10000, max_features=3, max_depth=3)
model.fit(X_train, y_train)

print(f"Train accuracy: {round(model.score(X_train, y_train), 3) * 100}%")
print(f"Test accuracy: {round(model.score(X_test, y_test), 3) * 100}%")

from sklearn.metrics import roc_curve, roc_auc_score
y_pred = model.predict_proba(X_test)[:, 1]
roc_auc = roc_auc_score(y_test, y_pred)
print(roc_auc)

#Visualize ROC Curve
import matplotlib.pyplot as plt
false_pos, true_pos, threshold = roc_curve(y_test, y_pred, pos_label=1)
plt.plot(false_pos, true_pos, label='ROC Curve')
plt.plot([0, 1], [0, 1], label='Random Curve')
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve")
plt.legend(loc="lower right")
plt.show()

#Visualize confusion matrix
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sn
classes = ['No CAT', 'CAT']
y_pred = model.predict(X_test)
matrix = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(5, 5))
sn.heatmap(matrix, annot=True, xticklabels=classes, yticklabels=classes)
plt.xlabel('Predicted')
plt.ylabel('Truth')

#Method to train and evaluate model
def train_model(model, X_train, y_train, X_test, y_test):
  model.fit(X_train, y_train)
  return [round(model.score(X_train, y_train), 3) * 100, round(model.score(X_test, y_test), 3) * 100]

#Evaluating Model w/ K fold Cross Validation
from sklearn.model_selection import KFold
kf = KFold(n_splits=6)
average_test, average_train = 0, 0
for train_index, test_index in kf.split(new_data):
  X_test = new_data.drop(['target'], axis='columns').iloc[min(test_index): max(test_index)]
  y_test = new_data['target'].iloc[min(test_index): max(test_index)]
  X_train1 = new_data.drop(['target'], axis='columns').iloc[min(train_index): min(test_index)]
  X_train2 = new_data.drop(['target'], axis='columns').iloc[max(test_index): max(train_index)]
  y_train1 = new_data['target'].iloc[min(train_index): min(test_index)]
  y_train2 = new_data['target'].iloc[max(test_index): max(train_index)]
  X_train = pd.concat([X_train1, X_train2], ignore_index=True)
  y_train = pd.concat([y_train1, y_train2], ignore_index=True)
  train_score, test_score = train_model(model2, X_train, y_train, X_test, y_test)
  average_train+=train_score
  average_test+=test_score
average_test/=6
average_train/=6
print(f"Train Performance: {average_train}%")
print(f"Test Performance: {average_test}%")

#Selecting hyperparameters to tune
from sklearn.model_selection import RandomizedSearchCV
n_estimators = [int(x) for x in np.linspace(start=100, stop=5000, num=20)]
#max_features = ['auto', 'sqrt']
#max_depth = [int(x) for x in np.linspace(10, 200, num=10)]
#max_depth.append(None)
#min_sample_split = [2, 5, 10]
#min_sample_leaf = [1, 2, 4]
#bootstrap = [True, False]
random_grid = {'n_estimators': n_estimators,
               #'max_features': max_features,
               #'max_depth': max_depth,
               #'min_samples_split': min_sample_split,
               #'min_samples_leaf': min_sample_leaf,
               #'bootstrap': bootstrap
               }

#Find best hyperparameter combination through random search w/ cross validation
model_random = RandomizedSearchCV(estimator=model,
                                  param_distributions=random_grid,
                                  n_iter=100,
                                  cv = 3,
                                  verbose=2
                                  )
model_random.fit(X_train, y_train)