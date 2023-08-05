import pandas as pd
from sklearn.preprocessing import OrdinalEncoder
from .stringtodatetime import StringToDateTime
from .inconsistent_data import InconsistentData
import numpy as np
class Encoder:
    def __init__(self,df,type = "", columns = []):
        ''' this class is dessigned to help you make encoding your data simple
        the input variables for this class are
        df: a pandas dataframe
        type: by defalult this variable will br set to ONEHOTENCODER if you with to use
        OrdinalEncoder you would set type to ordinalencoder
        columns: when you have specific columns you want to be be corrected a specific way
        then import the column or column names to this variable and only those columns will get corrected
        they type you specificed
        then you can call the check method to make the corretions
        this method will return a pandas data frame
        if you wish to compare the returned value to the original dataset you may
        call copy'''
        self.df = df
        self.copy = df.copy()
        self.type = type
        self.columns = columns
        datetime = StringToDateTime(self.df)
        self.df = datetime.check()
        correcting = InconsistentData(self.df)
        correcting.column_names_white_space()
        self.df = correcting.data_white_space()
        self.np = np.array(self.df.iloc[:,:].values)
        self.categories = []
    def check(self):
        if (len(self.columns)==0):
            self.object_column = []
            for i in self.df.columns:
                if (self.df[i].dtype == "object"):
                    self.object_column.append(i)
        else:
            # print("yes")

            self.object_column = [i for i in self.columns]
        self.Correct()
        # print(self.object_column)
        # print("yes")
        # print(self.df)
        return self.df
    def Correct(self):
        if (self.type == "" or self.type.upper() == "ONEHOTENCODER"):
            self.OneHotEncoder()
        elif (self.type.upper() == "ORDINALENCODER"):
            self.OrdinalEncoder()
    def OrdinalEncoder(self):
        columns = [i for i in self.df.columns]
        for i in self.object_column:
            for j in range(len(self.df.columns)):
                if (columns[j] == i):
                    # print(self.df[i].array.reshape(-1,1))
                    self.categories.append(self.df[i].value_counts().keys())
                    translate = OrdinalEncoder()
                    final = translate.fit_transform(self.df[i].array.reshape(-1,1))
                    self.df.drop(columns=i, inplace=True)
                    self.df[i] = final
        # print(self.categories)
    def OneHotEncoder(self):
        for i in self.object_column:
            new_df = pd.get_dummies(self.df[i])
            for  j in new_df.columns:
                self.df[j] = new_df[j]
        self.df.drop(columns=self.object_column,inplace=True)




if __name__ == "__main__":
    import pandas as pd
    import numpy as np
    import islanders as ir
    import irdatacleaning
    from tensorflow import keras
    data = ir.datasets("amazon electronics")
    name = [i for i in data.name]
    data.drop(columns = "name", inplace=True)
    encoder = Encoder(df = data, type="ordinalencoder")
    data = encoder.check()
    print(encoder.categories)
