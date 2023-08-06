import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

url1 = 'https://raw.githubusercontent.com/JIAN-JUNYANG/-AI-/main/t01.csv'
df1 = pd.read_csv(url1)
#df1=pd.read_csv('/Users/jjy/downloads/t01.csv')
df2=df1[["Country Name",
"2000","2001","2002","2003","2004",
"2005","2006","2007","2008","2009",
"2010","2011","2012","2013","2014",
"2015","2016","2017","2018","2019"]]
df3=df2.loc[df2["Country Name"].isin(["Mexico","India","Brazil","China",
"Thailand","Japan","Australia","France","Israel","Canada"])]
df3.index=["0","1","2","3","4","5","6","7","8","9"]

url2 = 'https://raw.githubusercontent.com/JIAN-JUNYANG/-AI-/main/t02.csv'
df4= pd.read_csv(url2)
#df4=pd.read_csv('/Users/jjy/downloads/t02.csv')
df5=df4[["Country Name",
"2000","2001","2002","2003","2004",
"2005","2006","2007","2008","2009",
"2010","2011","2012","2013","2014",
"2015","2016","2017","2018","2019"]]
df6=df5.loc[df5["Country Name"].isin(["Mexico","India","Brazil","China","Thailand","Japan","Australia","France","Israel","Canada"])]
df6.index=["0","1","2","3","4","5","6","7","8","9"]

country=["Australia","Brazil","Canada","China","France","India","Israel","Japan","Mexico","Thailand"]
years=[]
for i in range(2000,2020):
    years.append(i)

v1=str(input("input one country :"))
v2=str(input("input the other one country:"))

def find_index(x):
    for i in country:
        if i == x:
            return country.index(i)

def get_income(x):
    income=[]
    for i in df3.iloc[find_index(x),1:]:
        income.append(i)
    return income

def get_life_span(x):
    life_span=[]
    for i in df6.iloc[find_index(x),1:]:
        life_span.append(i)
    return life_span


def compare_income(x,y):
    plt.title("Average income in " +v1+" and " +v2)
    #plt.xticks(np.arange(0,20,1))
    #plt.plot(np.arange(0,20,1),get_income(v1),color="r",marker='o',label=v1)
    #plt.plot(np.arange(0,20,1),get_income(v2),color="b",marker='o',label=v2)
    plt.xticks(years,fontsize=5)
    plt.plot(years,get_income(v1),color="r",marker='o',label=v1)
    plt.plot(years,get_income(v2),color="b",marker='o',label=v2)
    plt.xlabel("year")
    plt.ylabel("income($)")
    plt.legend()
    plt.show()

def compare_life_span(x,y):
    plt.title("Average life span in " +v1+" and " +v2)
   # plt.xticks(np.arange(0,20,1))
    #plt.plot(np.arange(0,20,1),get_life_span(v1),color="r",marker='o',label=v1)
    #plt.plot(np.arange(0,20,1),get_life_span(v2),color="b",marker='o',label=v2)
    plt.xticks(years,fontsize=5)
    plt.plot(years,get_life_span(v1),color="r",marker='o',label=v1)
    plt.plot(years,get_life_span(v2),color="b",marker='o',label=v2)
    plt.xlabel("year")
    plt.ylabel("age")
    plt.legend()
    plt.show()

compare_income(v1,v2)
compare_life_span(v1,v2)