import streamlit as st
import pickle
import pandas as pd
import requests

st.title("Movie Recommender Sytem")
df= pd.read_csv("tmdb_5000_movies.csv")

a= st.selectbox("Select a Movie", df['title'].values)

#movies_dict= pickle.load(open('movies_dict.pkl','rb'))
#movies= pd.DataFrame(movies_dict)
#st.selectbox("select movie", movies['title'].values)
similarity=pickle.load(open("similarity.pkl",'rb'))

def fetch_poster(movie_id):
    response= requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=9ee973ca141ca9dd6608376c47021493&language=en-US')
    data= response.json()
    
    return "http://image.tmdb.org/t/p/w185/"+data['poster_path']

def recommend(movie):
    
    movie_index=df[df['title']==movie].index[0]
    distance= similarity[movie_index]
    movies_list= sorted(list(enumerate(distance)),reverse=True, key= lambda x:x[1])[1:6]
    
    cols= st.columns(5)
    j=0
    for i in movies_list:
        movie_id= df.iloc[i[0]].id
        #fetch movies poster from api
        with cols[j]:

            
            st.image(fetch_poster(movie_id))
            st.write(df.iloc[i[0]].title)
        j+=1


if st.button("Recommend"):
    (recommend(a))
    