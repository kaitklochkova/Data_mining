from numpy import savetxt, loadtxt
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib

print('import OK')

dataset = joblib.load('training_set.pkl')
print('load OK')

forest = RandomForestClassifier(n_estimators = 1000, n_jobs = 1)
target = [x[0] for x in dataset]
train = [x[1:] for x in dataset]
print('forest create OK')

forest.fit(train, target)
print('forest fit OK')

joblib.dump(forest, 'forest.pkl')

print('OK')
