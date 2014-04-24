from numpy import zeros
from numpy import array
def predict(theta, X):
    '''Predict whether the label
    is 0 or 1 using learned logistic
    regression parameters '''
    m, n = X.shape
    p = zeros(shape=(m, 1))

    h = sigmoid(X.dot(theta.T))

    for it in range(0, h.shape[0]):
        if h[it] > 0.5:
            p[it, 0] = 1
        else:
            p[it, 0] = 0

    return p

#Compute accuracy on our training set
p = predict(array(theta), it)
print 'Train Accuracy: %f' % ((y[where(p == y)].size / float(y.size)) * 100.0)