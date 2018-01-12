from Classifier import linear_classifier

X = [x for x in range(5)]

Y = [5,10,15,20,25]


print (str(len(X)), " : "+ str(len(Y)))
test = linear_classifier()
test.compile("squared","grad",lr=0.001)

#test.compile(loss="something",optimizer="grad",lr=0.001)

test.fit(X,Y,epochs=20)






