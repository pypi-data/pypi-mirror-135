import pandas as pd
from sklearn.preprocessing import StandardScaler

class FeatureScaler:
    '''FeatureScaler:
    this class is dessigned to make featur scaling very simple and begginer friendly.
    this class has 2 input arguments.
    FeatureScaler(df,checker=2)
    df: which is the dataset that you will be applying standard scaller
    checker is the threshold that your columns will be evluated at, by default this variable is set to 2 but you can change
    this depending on what you need'''
    def __init__(self, df, checker = 2):
        self.df = df
        self.scalerchecker = []
        self.scaler = StandardScaler()
        self.next_one = []
        self.checker = checker
    def Check(self):

        for i in self.df.columns:
            scalerdata = self.scaler.fit(self.df[i].array.reshape(-1, 1))
            # scalerchecker[i] = []
            checker = scalerdata.mean_
            for j in range(len(self.df[i])):
                if checker > 1:
                    if (self.df[i][j] > checker * self.checker):
                        self.scalerchecker.append(i)
        for i in self.scalerchecker:
            if (i in self.next_one):
                pass
            elif (i not in self.next_one):
                self.next_one.append(i)
        if (len(self.next_one)>0):
            scalerdata = self.scaler.fit_transform(self.df[self.next_one])
            self.df.drop(columns = self.next_one, inplace=True)
            newdf = pd.DataFrame(scalerdata, columns=self.next_one)
            for  i in newdf.columns:
                self.df[i] = newdf[i]
        return (self.df)