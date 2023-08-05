import pandas as pd
import numpy as np
import islanders as ir
import irdatacleaning
from sklearn.model_selection import train_test_split
from sklearn import model_selection
import sklearn.tree as tree
import matplotlib.pyplot as plt

class DT:
    '''this class is designed to work with scikit-learns DecisionTreeClassifier
    by making it so that all you have to do when you initiate this class is set the X and Y values
    DT(X values,Y values, test_size=.2)
    once you have initialized the class you can build the model by calling the build merthod there are two ways to call this methodthe first way is

    dt = self.build() which will just return the model itself, the next way is a bit more useful I think,

    dt,X_test,y_test = dec.build(True) this method will return not just the model but the X_test data and the y_test allowing you to run test on the model
    this class is designed to return the most optimized model you can possible have
    the last method allows you to see what your tree looks like you can call this method by running
    self.show()
    '''
    def __init__(self,*array,model_spects = "acc",test_size=0.2):
        self.X_data = np.array(array[0])
        self.y_data = np.array(array[1])
        self.X_train,self.X_test, self.y_train,self.y_test = train_test_split(array[0],array[1],test_size=test_size)
        length_dt = tree.DecisionTreeClassifier()
        length_dt.fit(self.X_train,self.y_train)
        self.unique, counts = np.unique(self.y_train, return_counts=True)
        self.params_dt = {'criterion':['gini','entropy'],
                          'max_depth':[i for i in range(1,length_dt.get_depth()*2)],
                          'min_samples_leaf':list(range(2,length_dt.get_n_leaves()*2,2))}
        self.cv = np.unique(self.y_data).size
        # print(np.unique(self.y_test).size)
        self.model_spects = model_spects
        self.dt_opt = model_selection.GridSearchCV(tree.DecisionTreeClassifier(),self.params_dt,cv = self.cv,return_train_score=False)
    def build(self,test = False):
        if (self.model_spects.lower()=="acc"):
            self.acc()
        elif(self.model_spects.lower()=="speed"):
            print("speed is still being worked on sorry for the inconvenience please pick acc")
            return
        else:
            print("please enter either acc for accuracy or speed for speed when you initiate the module")
            return
        if test:
            return self.dt.fit(self.X_train,self.y_train),self.X_test,self.y_test
        else:
            return self.dt.fit(self.X_train,self.y_train)

    def acc(self):



        # fit the model and optimize
        self.dt_opt.fit(self.X_train,self.y_train)

        # store the resutl sin a dataframe
        results = pd.DataFrame(self.dt_opt.cv_results_)
        ranking = np.array(results.rank_test_score.sort_values().index)
        self.results = results
        top = {"rank":[],
               "score":[],
               "time":[],
               "stats":[]}
        count = 0
        for i in range(len(results["rank_test_score"])):
            top["rank"].append(results["rank_test_score"][ranking[i]])
            top["score"].append(results["mean_test_score"][ranking[i]])
            top["time"].append(results["mean_score_time"][ranking[i]])
            top["stats"].append(results["params"][ranking[i]])
        not_num_1 = []
        columns = top.keys()
        for  i in range(len(top["rank"])):
            if top["rank"][i] >1:
                not_num_1.append(i)
        if len(not_num_1)!=0:
            for i in reversed(not_num_1):
                for j in columns:
                    top[j].pop(i)
        if len(top["rank"])>1:
            #     print(len(top))
            top_1 = pd.DataFrame(data = top, columns = columns)
            #     print(top_1)
            best_score = top_1.score.sort_values()
            #     print(best_score)
            if best_score[0]== best_score[1]:
                best_time = top_1.time.sort_values().index[0]
                best = top_1["stats"][best_time]
            #         print(best)
            else:
                best = top_1["stats"][top_1.score.sort_values().index]
        else:
            best = top["stats"][0]
        self.dt = tree.DecisionTreeClassifier(criterion = best["criterion"],max_depth = best["max_depth"],
                                              min_samples_leaf = best["min_samples_leaf"])

    def speed(self):
        # fit the model and optimize
        self.dt_opt.fit(self.X_train,self.y_train)

        # store the resutl sin a dataframe
        results = pd.DataFrame(self.dt_opt.cv_results_)
        ranking = np.array(results.mean_score_time.sort_values(ascending=False).index)
        top = {"rank":[],
               "score":[],
               "time":[],
               "stats":[]}
        self.results = results
        for i in range(len(results["rank_test_score"])):
            top["rank"].append(results["rank_test_score"][ranking[i]])
            top["score"].append(results["mean_test_score"][ranking[i]])
            top["time"].append(results["mean_score_time"][ranking[i]])
            top["stats"].append(results["params"][ranking[i]])
        not_num_1 = []
        columns = top.keys()
        min_1 = min(top["time"])
        for  i in range(len(top["time"])):
            if top["rank"][i] <=min_1:
                not_num_1.append(i)
        if len(not_num_1)!=0:
            for i in reversed(not_num_1):
                for j in columns:
                    top[j].pop(i)
        if len(top["rank"])>=1:
            #     print(len(top))
            top_1 = pd.DataFrame(data = top, columns = columns)
            #     print(top_1)
            best_score = top_1.score.sort_values()
            #     print(best_score)
            if best_score[0]== best_score[1]:
                best_time = top_1.time.sort_values().index[0]
                best = top_1["stats"][best_time]
            #         print(best)
            else:
                best = top_1["stats"][top_1.score.sort_values().index]
        else:
            best = top["stats"][0]
        self.dt = tree.DecisionTreeClassifier(criterion = best["criterion"],max_depth = best["max_depth"],
                                              min_samples_leaf = best["min_samples_leaf"])

    def show(self):
        plt.figure(figsize=(15,20))
        tree.plot_tree(self.dt, rounded =True, class_names = ['A','B'],
                       proportion=True, filled =True, impurity=False,fontsize=10)

if __name__ == "__main__":
    import pandas as pd
    import numpy as np
    import islanders as ir
    import irdatacleaning
    data = pd.read_csv("/Users/williammckeon/Sync/islander/dataset/amazon electronics.csv")
    name = [i for i in data.name]
    data.drop(columns = "name", inplace=True)
    data_x = np.array(data.iloc[:,:-1].values)
    data_y = np.array(data.iloc[:,-1].values)
    decsion = DT(data_x,data_y)
    bob = decsion.acc()
    print(bob.score(decsion.X_test,decsion.y_test))