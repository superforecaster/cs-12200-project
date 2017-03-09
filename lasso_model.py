import numpy as np
import pandas as pd
from sklearn.linear_model import Lasso
import operator

#PARAMETERS
betas = [1e-15, 1e-10, 1e-8, 1e-5,1e-4, 1e-3,1e-2, 1, 5, 10]


class lasso:

    def __init__(self,data,predictors,betas):
        self.data = data
        self.predictors = predictors
        self.betas = betas
        self.model = {}

    def select_model(self):
        #Select alphas such that minimize the mean
        #square errors of the predictions
        dic_alphas = {}
        for i in self.betas:
            dic_alphas[i] = []
            y_pred,coeffs,intercept =self.lasso(i)
            mse = self.mse(self.data,y_pred)
            dic_alphas[i].append(mse) 
            dic_alphas[i].append(y_pred)
            dic_alphas[i].append(coeffs)
            dic_alphas[i].append(intercept)
        #The key is each alpha
        #Get the alpha with the smaller mse (Copy this from Stack Overflow)
        model = min(dic_alphas.items(), key=lambda x: x[1]) 
        self.model = model

    def mse(self,y,y_pred):
        print("y",y)
        print("y_pre",y_pred)
        mse = (sum((y-y_pred)**2)/len(y))
        return mse

    def lasso(self,alpha):
        #Fit the model
        lassoreg = Lasso(alpha=alpha,normalize=True, max_iter=1e5)
        lassoreg.fit(self.predictors,self.data)
        coeffs = lassoreg.coef_
        intercept = lassoreg.intercept_
        y_pred = lassoreg.predict(self.predictors)
        return y_pred,coeffs,intercept

    def lasso_coeffs(self):
        model = self.select_model()
        predictors = list(self.predictors)
        coeffs = model[1][2]
        dic_coeffs = {}
        for i in range(len(coeffs)):
            if i!= 0:
                dic_coeffs[predictors[i]] = [i]
        #This line was copy from Stack Overflo
        dic_coeffs = sorted(dic_coeffs.items(), key=operator.itemgetter(1))
        return dic_coeffs




#Open CSV
df = pd.read_csv("mini_base/df_cov.csv", sep='\t')
#Dependent
df_dep = df["homicides"]
#Independent
indep = list(df.columns)
indep = indep[8:]
df_indep = df[indep]
for i in indep:
    #df_indep[i] = df_indep[i].map(lambda x: x.rstrip('e'))
    df_indep[i] = pd.to_numeric(df_indep[i])
#Final quality checks
df_indep = df_indep.round(decimals=3)
df_indep = df_indep.dropna(axis=1, how='any', thresh=None, subset=None)

#TEST
model1 = lasso(df_dep,df_indep,betas)
model1.select_model()
