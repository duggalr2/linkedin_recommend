from sklearn.datasets import load_iris



# load the iris dataset
iris = load_iris()
# store the feature matrix (X) and response vector (y)
X = iris.data
y = iris.target

print(X.shape)
print(y.shape)