# Islanders
this is a python packaged dessigned to make artificial Intelligence engineers, machine learning engineers, and Data 
Sciencist lives easier to do there job. within this package you will have the ability to use irdatacleanings  methods as well as

- datasets: this method is for those part of the islander community where you will be able to run code like,
```python
import islanders as ir
gifts = ir.dataset("amazon electronic")
titanic = ir.dataset("titanic")
movie = ir.datasets("movie")
```
## DT
this class is designed to work with scikit-learns DecisionTreeClassifier
by making it so that all you have to do when you initiate this class is set the X and Y values
DT(X values,Y values, test_size=.2)
once you have initialized the class you can build the model by calling the build merthod there are two ways to call this methodthe first way is
dt = self.build() which will just return the model itself, the next way is a bit more useful I think,
dt,X_test,y_test = dec.build(True) this method will return not just the model but the X_test data and the y_test allowing you to run test on the model. 
This class is designed to return the most optimized model you can possible have
the last method allows you to see what your tree looks like you can call this method by running
self.show()