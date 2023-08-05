import pandas as pd
from sklearn.preprocessing import StandardScaler, normalize
import numpy as np

class FeatureScaler:
    '''This class is designed to allow you to scale your data with ease. You have the ability to scaler your
by using StandardScaler or normalize. Not only that, but you can also scale either the whole dataset or
you can just scale one column at a time.
the initialization of this module is
FeatureScaler(data,scaler=StandardScaler,columns=[])
data is where you can either enter a pandas data frame or a NumPy array,
by default the scaler this module will use is StandardScaler, but you can change this variable to normalize to use
normalization.
the columns input argument is to allow you the ability to have more control over what columns get scaled if you leave this
empty, you will end up scaling the whole dataset
to tell the module to do something with the data, all you have to do is call the check method by .check()
this will return the scaled data that you imported in the same format that you entered it as

'''
    def __init__(self,data, scaler = "StandardScaler", columns=[]):
        self.data = data
        self.scaler = scaler
        self.columns = columns
        if isinstance(data, np.ndarray):
            self.type = "numpy"
        elif isinstance(data, pd.core.frame.DataFrame):
            self.type = "pandas"

    def check(self):
        if self.scaler.lower() == "standardscaler":
            self.standardscaler_()
        elif self.scaler.lower() =="normalize":
            self.normalizion_()
        if self.type == "pandas":
            return pd.DataFrame(data = self.data,columns= self.columns_names)
        else:

            return self.data
    def standardscaler_(self):
        scaler = StandardScaler()
        if self.type == "pandas":
            self.converting_to_np_()

        if len(self.columns)>0:
            for  i in  self.columns:
                self.data[:,i] = scaler.fit_transform(self.data[:,i].reshape(-1,1)).flatten()

        else:
            for i in range(self.data.shape[1]):
                self.data[:,i] = scaler.fit_transform(self.data[:, i].reshape(-1,1)).flatten()
    def normalizion_(self):
        if self.type == "pandas":
            self.converting_to_np_()
        if len(self.columns)>0:
            for i in self.columns:
                self.data[:,i] = normalize(self.data[:,i].reshape(-1,1)).flatten()


        else:
            for i in range(self.data.shape[1]):
                self.data[:,i] = normalize(self.data[:,i].reshape(-1,1)).flatten()

    def converting_to_np_(self):
        self.copy = self.data
        self.columns_names = self.data.columns
        temp = np.array(self.data.iloc[:,:])
        self.data = temp
        if len(self.columns)>0:
            column_dt = {}
            index = []
            for i in range(len(self.columns_names)):
                column_dt[self.columns_names[i]] = i
            for i in self.columns:
                index.append(column_dt[i])
            self.columns = index
if __name__ == "__main__":
    import islanders as ir
    data = ir.datasets(
        "titanic")
    scaler = FeatureScaler(data = data, scaler = "normalize")
    scaler.check()