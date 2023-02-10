#!/usr/bin/env python
# coding: utf-8

# In[5]:


import numpy as np
import pandas as pd


# In[6]:


movies=pd.read_csv("tmdb_5000_movies.csv")
credits=pd.read_csv("tmdb_5000_credits.csv")


# In[7]:


movies.head(1)


# In[8]:


credits.head(1)


# In[9]:


movies['genres'][0]


# In[10]:


#credits['cast'][0]
#credits['crew'][0]


# In[11]:


movies.shape


# In[12]:


credits.shape


# In[140]:


#merge both dataFrame movies and credits and store into the movie
movies=movies.merge(credits,on='title')


# In[14]:


movies.shape


# In[15]:


movies.info()


# In[16]:


# remove unnessary columns because we need nessary column to give recommendation
# genres
# keywords
# title
# overview
# movie_id
# cast
# crew


# In[142]:


#movies['original_language'].value_counts()


# In[18]:


movies=movies[['movie_id','title','overview','genres','keywords','cast','crew']]


# In[19]:


movies.head(1)


# In[20]:


movies.isnull().sum()


# In[21]:


movies.dropna(inplace=True)


# In[22]:


movies.duplicated().sum()


# In[23]:


movies.iloc[0].genres


# In[24]:


#'[{"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}, {"id": 14, "name": "Fantasy"}, {"id": 878, "name": "Science Fiction"}]'
#['Action','Adventure','Fantasy','SciFi']


# In[25]:


import ast
def convert(obj):
    lis=[]
    for i in ast.literal_eval(obj):
        lis.append(i['name'])
    return lis


# In[26]:


movies['genres']=movies['genres'].apply(convert)


# In[27]:


movies.head(1)


# In[28]:


movies['keywords']=movies['keywords'].apply(convert)


# In[133]:


#movies['cast'][0] https://api.themoviedb.org/3/movie/{movie_id}?api_key=<<api_key>>&language=en-US


# In[30]:


def convert3(obj):
    lis=[]
    counter=0
    for i in ast.literal_eval(obj):
        if counter != 3:
            lis.append(i['name'])
            counter+=1
        else:
            break
    return lis


# In[31]:


movies['cast'] = movies['cast'].apply(convert3)


# In[32]:


movies['crew'][4804]


# In[33]:


def fetch_director(obj):
    lis=[]
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            lis.append(i['name'])
            break
    return lis


# In[34]:


movies['crew']=movies['crew'].apply(fetch_director)


# In[35]:


movies['overview'] = movies['overview'].apply(lambda x: x.split())


# In[36]:


movies.head(1)


# In[37]:


movies['genres'] = movies['genres'].apply(lambda x :[i.replace(" ","") for i in x ])
movies['keywords'] = movies['keywords'].apply(lambda x :[i.replace(" ","") for i in x ])
movies['cast'] = movies['cast'].apply(lambda x :[i.replace(" ","") for i in x ])
movies['crew'] = movies['crew'].apply(lambda x :[i.replace(" ","") for i in x ])


# In[38]:


movies['tags']=movies['overview']+movies['genres']+movies['keywords']+movies['cast']+movies['crew']


# In[39]:


#after tags generated

new_movies=movies[['movie_id', 'title','tags']]


# In[40]:


new_movies['tags'] = new_movies['tags'].apply(lambda x : " ".join(x) )


# In[41]:


new_movies['tags'][0]


# In[42]:


new_movies['tags'] = new_movies['tags'].apply(lambda x : x.lower())


# In[43]:


new_movies.head(1)


# In[65]:


import nltk


# In[67]:


from nltk.stem.porter import PorterStemmer
ps=PorterStemmer()


# In[78]:


ps.stem('loved')


# In[76]:


def stem(text):
    y=[]
    for i in text.split():
        y.append(ps.stem(i))
    convert_in_string = " ".join(y)
    return convert_in_string


# In[77]:


stem('in the 22nd century, a paraplegic marine is dispatched to the moon pandora on a unique mission, but becomes torn between following orders and protecting an alien civilization. action adventure fantasy sciencefiction cultureclash future spacewar spacecolony society spacetravel futuristic romance space alien tribe alienplanet cgi marine soldier battle loveaffair antiwar powerrelations mindandsoul 3d samworthington zoesaldana sigourneyweaver jamescameron')


# In[80]:


new_movies['tags'] = new_movies['tags'].apply(stem)


# In[82]:


new_movies['tags'][0]


# In[83]:


new_movies['tags'][1]


# In[84]:


#compare two tags to find similarity


# In[85]:


from sklearn.feature_extraction.text import CountVectorizer
cv=CountVectorizer(max_features=5000, stop_words='english')


# In[86]:


vectors = cv.fit_transform(new_movies['tags']).toarray()


# In[143]:


vectors


# In[144]:


vectors.shape


# In[88]:


len(cv.get_feature_names_out())


# In[89]:


cv.get_feature_names_out()


# In[ ]:


#5000 dimenssional
# to find the distance between movies 
# we use eculiden distance or cosine distance but I use cosine distance


# In[95]:


from sklearn.metrics.pairwise import cosine_similarity


# In[100]:


similarity = cosine_similarity(vectors)


# In[138]:


new_movies[new_movies['title']=='Avatar'].index[0]


# In[117]:


#sorted(similarity[0],reverse=True)
sorted(list(enumerate(similarity[0])),reverse=True,key= lambda x : x[1])[1:6]


# In[129]:


def recommend(movie):
    movie_index = new_movies[new_movies['title']==movie].index[0]
    distance = similarity[movie_index]
    movie_list = sorted(list(enumerate(distance)),reverse=True,key= lambda x : x[1])[1:6]
    
    for i in movie_list:
        print(new_movies.iloc[i[0]].title)
        


# In[132]:


recommend('Batman Begins')


# In[135]:


import pickle as pk


# In[136]:


pk.dump(new_movies,open('movies.pkl','wb'))


# In[139]:


pk.dump(similarity,open('similarity.pkl','wb'))


# In[ ]:




