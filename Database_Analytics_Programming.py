#!/usr/bin/env python
# coding: utf-8

# # __DAP Final Project Code__

# In[263]:


#packages needed.

import kaggle
import json
import csv
import pandas as pd
import numpy as np
import zipfile
import seaborn as sns
from pymongo import MongoClient
import pymongo as pm
import psycopg2
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import joypy


# In[2]:


#Using Kaggle-API for downloading the required 4 datasets.

get_ipython().system('kaggle datasets download datasnaek/youtube-new -f USvideos.csv --force')
get_ipython().system('kaggle datasets download datasnaek/youtube-new -f INvideos.csv --force')
get_ipython().system('kaggle datasets download datasnaek/youtube-new -f RUvideos.csv --force')
get_ipython().system('kaggle datasets download datasnaek/youtube-new -f JPvideos.csv --force')


# In[3]:


#Unzipping the downloaded datasets.

zip1 = zipfile.ZipFile('USvideos.csv.zip')
zip1.extractall()
zip2 = zipfile.ZipFile('INvideos.csv.zip')
zip2.extractall()
zip3 = zipfile.ZipFile('RUvideos.csv.zip')
zip3.extractall()
zip4 = zipfile.ZipFile('JPvideos.csv.zip')
zip4.extractall()


# In[6]:


#Creating a JSON data file for downloaded USvideos dataset.

with open("USvideos.csv", "r", encoding="ISO-8859-1") as f:
    reader = csv.reader(f)
    next(reader)
    dataUS = []
    for row in reader:
        dataUS.append({"VideoID":row[0],"TrendingDate":row[1],"Title":row[2],"ChannelTitle":row[3],"CategoryID":row[4],"PublishedID":row[5],"Tags":row[6],"Views":row[7],"Likes":row[8],"Dislikes":row[9],"CommentCount":row[10],"ThumbnailLink":row[11],"CommentsDisabled":row[12],"Ratings":row[13],"VideoError":row[14],"Desciption":row[15]})


# In[7]:


dataUS


# In[8]:


#Creating a JSON data file for downloaded INvideos dataset.

with open("INvideos.csv", "r", encoding="ISO-8859-1") as f:
    reader = csv.reader(f)
    next(reader)
    dataIN = []
    for row in reader:
        dataIN.append({"VideoID":row[0],"TrendingDate":row[1],"Title":row[2],"ChannelTitle":row[3],"CategoryID":row[4],"PublishedID":row[5],"Tags":row[6],"Views":row[7],"Likes":row[8],"Dislikes":row[9],"CommentCount":row[10],"ThumbnailLink":row[11],"CommentsDisabled":row[12],"Ratings":row[13],"VideoError":row[14],"Desciption":row[15]})


# In[9]:


dataIN


# In[10]:


#Creating a JSON data file for downloaded RUvideos dataset.

with open("RUvideos.csv", "r", encoding="ISO-8859-1") as f:
    reader = csv.reader(f)
    next(reader)
    dataRU = []
    for row in reader:
        dataRU.append({"VideoID":row[0],"TrendingDate":row[1],"Title":row[2],"ChannelTitle":row[3],"CategoryID":row[4],"PublishedID":row[5],"Tags":row[6],"Views":row[7],"Likes":row[8],"Dislikes":row[9],"CommentCount":row[10],"ThumbnailLink":row[11],"CommentsDisabled":row[12],"Ratings":row[13],"VideoError":row[14],"Desciption":row[15]})


# In[11]:


dataRU


# In[12]:


#Creating a JSON data file for downloaded JPvideos dataset.

with open("JPvideos.csv", "r", encoding="ISO-8859-1") as f:
    reader = csv.reader(f)
    next(reader)
    dataJP = []
    for row in reader:
        dataJP.append({"VideoID":row[0],"TrendingDate":row[1],"Title":row[2],"ChannelTitle":row[3],"CategoryID":row[4],"PublishedID":row[5],"Tags":row[6],"Views":row[7],"Likes":row[8],"Dislikes":row[9],"CommentCount":row[10],"ThumbnailLink":row[11],"CommentsDisabled":row[12],"Ratings":row[13],"VideoError":row[14],"Desciption":row[15]})


# In[13]:


dataJP


# In[14]:


len(dataUS)


# In[15]:


len(dataIN)


# In[16]:


len(dataRU)


# In[17]:


len(dataJP)


# ## __Connecting to MondoDB and populating the semi-structured data.__

# In[ ]:


#For US

client = MongoClient('localhost', 27017)
db = client["YT"]
yt_colus = db["ytus"]
if isinstance(dataUS, list): 
    yt_colus.insert_many(dataUS)   
else: 
    yt_colus.insert_one(dataUS) 


# In[24]:


#For India

client = MongoClient('localhost', 27017)
db = client["YT"]
yt_colin = db["ytin"]
if isinstance(dataIN, list): 
    yt_colin.insert_many(dataIN)   
else: 
    yt_colin.insert_one(dataIN)


# In[25]:


#For Russia

client = MongoClient('localhost', 27017)
db = client["YT"]
yt_colru = db["ytru"]
if isinstance(dataRU, list): 
    yt_colru.insert_many(dataRU)   
else: 
    yt_colru.insert_one(dataRU)


# In[26]:


#For Japan

client = MongoClient('localhost', 27017)
db = client["YT"]
yt_coljp = db["ytjp"]
if isinstance(dataJP, list): 
    yt_coljp.insert_many(dataJP)   
else: 
    yt_coljp.insert_one(dataJP)


# In[27]:


#creating a DataFrame for US dataset using Pandas.

us_data = yt_colus.find()
us_dlist = list(us_data)
us_df = pd.DataFrame(us_dlist)


# In[28]:


#creating a DataFrame for IN dataset using Pandas.

in_data = yt_colin.find()
in_dlist = list(in_data)
in_df = pd.DataFrame(in_dlist)


# In[29]:


#creating a DataFrame for RU dataset using Pandas.

ru_data = yt_colru.find()
ru_dlist = list(ru_data)
ru_df = pd.DataFrame(ru_dlist)


# In[30]:


#creating a DataFrame for JP dataset using Pandas.

jp_data = yt_coljp.find()
jp_dlist = list(jp_data)
jp_df = pd.DataFrame(jp_dlist)


# In[35]:


us_df.head(1)


# ## __Data Cleaning.__

# In[ ]:


#Keeping the columns we want for further processing.

us_df1 = pd.DataFrame(us_df, columns = ["TrendingDate", "Views", "Likes", "Dislikes", "CommentCount"])
in_df1 = pd.DataFrame(in_df, columns = ["TrendingDate", "Views", "Likes", "Dislikes", "CommentCount"])
ru_df1 = pd.DataFrame(ru_df, columns = ["TrendingDate", "Views", "Likes", "Dislikes", "CommentCount"])
jp_df1 = pd.DataFrame(jp_df, columns = ["TrendingDate", "Views", "Likes", "Dislikes", "CommentCount"])


# In[80]:


us_df1


# In[42]:


in_df1


# In[44]:


ru_df1


# In[46]:


jp_df1


# In[82]:


#Extracting the Year and Month column from TrendingDate.

us_df1['Year'] = pd.to_datetime(us_df1['TrendingDate'], format='%y.%d.%m').dt.strftime('%B %Y')
jp_df1['Year'] = pd.to_datetime(jp_df1['TrendingDate'], format='%y.%d.%m').dt.strftime('%B %Y')
ru_df1['Year'] = pd.to_datetime(ru_df1['TrendingDate'], format='%y.%d.%m').dt.strftime('%B %Y')
in_df1['Year'] = pd.to_datetime(in_df1['TrendingDate'], format='%y.%d.%m').dt.strftime('%B %Y')


# In[87]:


#Removing the records for 2017, only used 2018 records in all the datasets.

us_df2 = us_df1[~us_df1.Year.str.contains("2017")]
ru_df2 = ru_df1[~ru_df1.Year.str.contains("2017")]
in_df2 = in_df1[~in_df1.Year.str.contains("2017")]


# In[88]:


us_df2


# In[92]:


jp_df1


# In[91]:


ru_df1


# In[95]:


ru_df2


# In[98]:


in_df2


# In[250]:


#Adding the Country column in each dataset with respective country names. 

in_df2["Country"] = "India"
ru_df2["Country"] = "Russia"
jp_df1["Country"] = "Japan"
us_df2["Country"] = "US"


# In[104]:


#Final DataFrame for Japan.

jp_df1


# In[105]:


#Final DataFrame for US.

us_df2


# In[106]:


#Final DataFrame for India.

ru_df2


# In[107]:


#Final DataFrame for India.

in_df2


# ## __Connecting to PostgreSQL and Objects Creation.__

# In[110]:


#Establishing a connection to PostgreSQL and creating a dataBase named "YouTube".

try:
    dbConnection = psycopg2.connect(user = "dap", password = "dap", host = "192.168.56.30", port = "5432", database = "postgres")
    dbConnection.set_isolation_level(0) # AUTOCOMMIT
    dbCursor = dbConnection.cursor()
    dbCursor.execute('CREATE DATABASE YouTube;')
    dbCursor.close()
except (Exception , psycopg2.Error) as dbError :
    print ("Error while connecting to PostgreSQL", dbError)
finally:
    if(dbConnection): dbConnection.close()


# In[111]:


#Creating a table for India Dataset in the YouTube DataBase.

createString = """
CREATE TABLE YTIndia(
TrendingDate date,
Views integer,
Likes integer,
Dislikes integer,
CommentCount integer,
Year varchar(20),
Country text
);
"""
try:
    dbConnection = psycopg2.connect(user = "dap", password = "dap", host = "192.168.56.30", port = "5432", database = "youtube")
    dbConnection.set_isolation_level(0) # AUTOCOMMIT
    dbCursor = dbConnection.cursor()
    dbCursor.execute(createString)
    dbCursor.close()
except (Exception , psycopg2.Error) as dbError :
    print ("Error while connecting to PostgreSQL", dbError)
finally:
    if(dbConnection): dbConnection.close()


# In[112]:


#Creating a table for US Dataset in the YouTube DataBase.

createString = """
CREATE TABLE YT(
TrendingDate date,
Views integer,
Likes integer,
Dislikes integer,
CommentCount integer,
Year varchar(20),
Country text
);
"""
try:
    dbConnection = psycopg2.connect(user = "dap", password = "dap", host = "192.168.56.30", port = "5432", database = "youtube")
    dbConnection.set_isolation_level(0) # AUTOCOMMIT
    dbCursor = dbConnection.cursor()
    dbCursor.execute(createString)
    dbCursor.close()
except (Exception , psycopg2.Error) as dbError :
    print ("Error while connecting to PostgreSQL", dbError)
finally:
    if(dbConnection): dbConnection.close()


# In[113]:


#Creating a table for Russia Dataset in the YouTube DataBase.

createString = """
CREATE TABLE YTRussia
(TrendingDate date,
Views integer,
Likes integer,
Dislikes integer,
CommentCount integer,
Year varchar(20),
Country text
);
"""
try:
    dbConnection = psycopg2.connect(user = "dap", password = "dap", host = "192.168.56.30", port = "5432", database = "youtube")
    dbConnection.set_isolation_level(0) # AUTOCOMMIT
    dbCursor = dbConnection.cursor()
    dbCursor.execute(createString)
    dbCursor.close()
except (Exception , psycopg2.Error) as dbError :
    print ("Error while connecting to PostgreSQL", dbError)
finally:
    if(dbConnection): dbConnection.close()


# In[114]:


#Creating a table for Japan Dataset in the YouTube DataBase.

createString = """
CREATE TABLE YTJapan(
TrendingDate date,
Views integer,
Likes integer,
Dislikes integer,
CommentCount integer,
Year varchar(20),
Country text
);
"""
try:
    dbConnection = psycopg2.connect(user = "dap", password = "dap", host = "192.168.56.30", port = "5432", database = "youtube")
    dbConnection.set_isolation_level(0) # AUTOCOMMIT
    dbCursor = dbConnection.cursor()
    dbCursor.execute(createString)
    dbCursor.close()
except (Exception , psycopg2.Error) as dbError :
    print ("Error while connecting to PostgreSQL", dbError)
finally:
    if(dbConnection): dbConnection.close()


# In[118]:


#Populating the tables in PostgreSQL for all 4 countries using SQLAlchemy.

engine = create_engine('postgresql://dap:dap@192.168.56.30:5432/youtube')
in_df2.to_sql('ytindia_final', engine)

engine = create_engine('postgresql://dap:dap@192.168.56.30:5432/youtube')
us_df2.to_sql('ytus_final', engine)

engine = create_engine('postgresql://dap:dap@192.168.56.30:5432/youtube')
jp_df1.to_sql('ytjp_final', engine)

engine = create_engine('postgresql://dap:dap@192.168.56.30:5432/youtube')
ru_df2.to_sql('ytru_final', engine)


# In[130]:


#Joined the 4 tables for 4 countries in one table named "youtube_merged_final".

createString = """
CREATE TABLE youtube_merged_final
AS SELECT * FROM ytindia_final 
UNION 
SELECT * FROM ytus_final 
UNION 
SELECT * FROM ytru_final 
UNION 
SELECT * FROM ytjp_final;
"""
try:
    dbConnection = psycopg2.connect(user = "dap", password = "dap", host = "192.168.56.30", port = "5432", database = "youtube")
    dbConnection.set_isolation_level(0) # AUTOCOMMIT
    dbCursor = dbConnection.cursor()
    dbCursor.execute(createString)
    dbCursor.close()
except (Exception , psycopg2.Error) as dbError :
    print ("Error while connecting to PostgreSQL", dbError)
finally:
    if(dbConnection): dbConnection.close()


# In[137]:


#Retrieving the final joined table from PostgreSQL using Pandas.

try:
    dbConnection = psycopg2.connect(user = "dap", password = "dap", host = "192.168.56.30", port = "5432", database = "youtube")
    dbConnection.set_isolation_level(0) # AUTOCOMMIT
    dbCursor = dbConnection.cursor()
    #ytmerged = dbCursor.execute(createString)
    ytmerged = pd.read_sql("select * from \"youtube_merged_final\"", dbConnection);
    dbCursor.close()
except (Exception , psycopg2.Error) as dbError :
    print ("Error while connecting to PostgreSQL", dbError)
finally:
    if(dbConnection): dbConnection.close()


# In[138]:


ytmerged


# In[159]:


#Converting the columns to the numeric data type.

ytmerged['CommentCount'] = pd.to_numeric(ytmerged['CommentCount'])
ytmerged['Likes'] = pd.to_numeric(ytmerged['Likes'])
ytmerged['Dislikes'] = pd.to_numeric(ytmerged['Dislikes'])
ytmerged['Views'] = pd.to_numeric(ytmerged['Views'])


# In[307]:


#Final Joined Table.

ytmerged


# ## __Data Visualization.__

# ### 1. Bar Plots.

# In[255]:


ytmerged.groupby("Country").Likes.mean().sort_values(ascending=False)[:4].plot.bar(title = "Average number of Likes - Countrywise")


# In[257]:


ytmerged.groupby("Country").Views.mean().sort_values(ascending=False)[:4].plot.bar(title = "Average number of Views - Countrywise")


# In[256]:


ytmerged.groupby("Country").Dislikes.mean().sort_values(ascending=False)[:4].plot.bar(title = "Average number of Dislikes - Countrywise")


# In[258]:


ytmerged.groupby("Country").CommentCount.mean().sort_values(ascending=False)[:500].plot.bar(title = "Average number of Comment Counts - Countrywise")


# In[259]:


ytmerged.groupby("Country").CommentCount.mean().sort_values(ascending=False)[:4].plot.barh(title = "Average number of Comment Counts - Countrywise")


# In[308]:


ytmerged.groupby("Year").Likes.mean().sort_values(ascending=False)[:12].plot.bar(title='Average number of Likes - Year wise')


# ### 2. Scatter Plot.

# In[169]:


ytmerged.plot.scatter(x='Country', y='Likes', title='Country wise Likes')


# In[206]:


# Calculated mean of Likes, Dislikes, Views and Comment Counts Country wise.

likes_mean_c = ytmerged.groupby("Country")['Likes'].mean()
dislikes_mean_c = ytmerged.groupby("Country")['Dislikes'].mean()
views_mean_c = ytmerged.groupby("Country")['Views'].mean()
comment_mean_c = ytmerged.groupby("Country")['CommentCount'].mean()


# In[210]:


# Calculated mean of Likes, Dislikes, Views and Comment Counts Year wise.

likes_mean_y = ytmerged.groupby("Year")['Likes'].mean()
dislikes_mean_y = ytmerged.groupby("Year")['Dislikes'].mean()
views_mean_y = ytmerged.groupby("Year")['Views'].mean()
comment_mean_y = ytmerged.groupby("Year")['CommentCount'].mean()


# In[199]:


likes_mean_c


# In[200]:


dislikes_mean_c


# In[201]:


views_mean_c


# In[202]:


comment_mean_c


# In[208]:


likes_mean_y


# In[211]:


views_mean_y


# In[212]:


dislikes_mean_y


# In[213]:


comment_mean_y


# In[290]:


# Created a DataFrame and added all the means year wise and country wise.


Country = ['India', 'Japan', 'Russia', 'US']
mean_df = pd.DataFrame(list(zip(likes_mean_y, dislikes_mean_y, views_mean_y, comment_mean_y, likes_mean_c, dislikes_mean_c, views_mean_c, comment_mean_c, Country)), columns = ['likes_mean_y','dislikes_mean_y','views_mean_y','comment_mean_y','likes_mean_c','dislikes_mean_c','views_mean_c','comment_mean_c', 'Country'])
mean_df['Year'] = 2018
mean_df


# ### 3. Strip Plots.

# In[226]:


fig, ax = plt.subplots(figsize=(16,10), dpi= 80)    
sns.stripplot(ytmerged.Country, ytmerged.Likes, jitter=0.25, size=8, ax=ax, linewidth=.5)

# Decorations
plt.title('Country vs Likes', fontsize=22)
plt.show()


# In[227]:


fig, ax = plt.subplots(figsize=(16,10), dpi= 80)    
sns.stripplot(ytmerged.Country, ytmerged.Views, jitter=0.25, size=8, ax=ax, linewidth=.5)

# Decorations
plt.title('Country vs Views', fontsize=22)
plt.show()


# ### 4. Heat Map.

# In[233]:


plt.figure(figsize=(12,10), dpi= 80)
sns.heatmap(ytmerged.corr(), xticklabels=ytmerged.corr().columns, yticklabels=ytmerged.corr().columns, cmap='RdYlGn', center=0, annot=True)

# Decorations
plt.title('Correlogram of YouTube Statistics ', fontsize=22)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.show()


# ### 5. Pair Plots. 

# In[235]:


plt.figure(figsize=(10,8), dpi= 80)
sns.pairplot(ytmerged, kind="scatter", hue="Year", plot_kws=dict(s=80, edgecolor="white", linewidth=2.5))
plt.show()


# In[236]:


plt.figure(figsize=(10,8), dpi= 80)
sns.pairplot(ytmerged, kind="scatter", hue="Country", plot_kws=dict(s=80, edgecolor="white", linewidth=2.5))
plt.show()


# ### 6. Density Plot.

# In[306]:


plt.figure(figsize=(16,10), dpi= 80)
sns.kdeplot(ytmerged.loc[ytmerged['Country'] == 'India', "Likes"], shade=True, color="g", label="India", alpha=.5)
sns.kdeplot(ytmerged.loc[ytmerged['Country'] == 'Japan', "Likes"], shade=True, color="deeppink", label="Japan", alpha=.5)
sns.kdeplot(ytmerged.loc[ytmerged['Country'] == 'Russia', "Likes"], shade=True, color="dodgerblue", label="Russia", alpha=.5)
sns.kdeplot(ytmerged.loc[ytmerged['Country'] == 'US', "Likes"], shade=True, color="orange", label="US", alpha=.5)
plt.title('Density Plot of likes by Countries', fontsize=22)
plt.legend()
plt.show()


# In[ ]:




