import numpy as np
import pandas as pd
from sklearn.linear_model import Lasso
import operator
from dataframe_lasso import df_limited, list_dep, list_lags, list_lags_n 

df = pd.read_csv("mini_base/df_limited.csv", sep='\t')

def front_end(dep,year):
    #PARAMETERS : Don't touch or you died
    betas = [1e-15, 1e-10, 1e-8, 1e-5,1e-4, 1e-3,1e-2, 1, 5, 10]
    #Dependent
    dep = df[dep]
    #Independent
    indep = df[list_lags]
    #Robustness check of non-numeric values, NaN and super-long floats
    for i in list_lags:
        indep[i] = pd.to_numeric(indep[i])
    indep = indep.round(decimals=3)
    indep = indep.dropna(axis=1, how='any', thresh=None, subset=None)
    #Run lasso
    model = lasso(dep,indep,betas)
    model.select_model()
    output = model.model
    #Format results for front-end
    #DF Actual values ()
    df_actual = df[["year","state_key","state_name"]]
    df_actual = df_actual.join(dep)
    df_actual = df_actual[df_actual["year"] == year]
    #DF Predicted values
    df_predicted = output[1][1]
    df_predicted = pd.DataFrame(df_predicted)
    df_aux = df[["year","state_key","state_name"]]
    df_predicted = df_predicted.join(df_aux)
    df_predicted = df_predicted[df_predicted["year"] == year]
    #DF Coeffs 
    coeffs = model.lasso_coeffs()
    df_coeffs = pd.DataFrame(coeffs)
    #DF CORR and MSE
    mse = output[1][0]
    corr = output[1][4]

    return df_actual, df_predicted, df_coeffs, mse, corr


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
            corr = self.corr(self.data,y_pred)
            dic_alphas[i].append(mse) 
            dic_alphas[i].append(y_pred)
            dic_alphas[i].append(coeffs)
            dic_alphas[i].append(intercept)
            dic_alphas[i].append(corr)
        #The key is each alpha
        #Get the alpha with the smaller mse (Copy this from Stack Overflow)
        model = min(dic_alphas.items(), key=lambda x: x[1]) 
        self.model = model

    def mse(self,y,y_pred):
        mse = (sum((y-y_pred)**2)/len(y))
        return mse

    def corr(self,y,y_pred):
        y = pd.DataFrame(y)
        y_pred = pd.DataFrame(y_pred)
        df = y.join(y_pred)
        return df.corr()

    def lasso(self,alpha):
        #Fit the model
        lassoreg = Lasso(alpha=alpha,normalize=True, max_iter=1e5)
        lassoreg.fit(self.predictors,self.data)
        coeffs = lassoreg.coef_
        intercept = lassoreg.intercept_
        y_pred = lassoreg.predict(self.predictors)
        return y_pred,coeffs,intercept

    def lasso_coeffs(self):
        model = self.model
        predictors = list(self.predictors)
        coeffs = model[1][2]
        dic_coeffs = {}
        for i in range(len(coeffs)):
            if i!= 0:
                dic_coeffs[predictors[i]] = coeffs[i]
        #This line was copy from Stack Overflo
        tup_coeffs = sorted(dic_coeffs.items(), key=operator.itemgetter(1))
        return tup_coeffs



'''
betas = [1e-15, 1e-10, 1e-8, 1e-5,1e-4, 1e-3,1e-2, 1, 5, 10]
dep = df["homicides"]
indep = df[list_lags]
for i in list_lags:
    print(i)
    print(indep[i].dtype)
    indep[i] = pd.to_numeric(indep[i])
indep = indep.round(decimals=3)
indep = indep.dropna(axis=1, how='any', thresh=None, subset=None)
model = lasso(dep,indep,betas)
output = model.select_model()
'''


