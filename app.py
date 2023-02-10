import streamlit as st
import pickle
import requests
st.title('Move Suggestion')
movies_list=pickle.load(open('movies.pkl','rb'))

similarity = pickle.load(open('similarity.pkl','rb'))

def fetch_image(movie_id):
    respose = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=9b310881dbc58d1bcf7e390a4e4ea014&language=en-US'.format(movie_id))
    data = respose.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
#print(movies_list)


def suggestion(movie):
    movie_index=movies_list[movies_list['title']== movie].index[0]
    distance = similarity[movie_index]
    movie_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]
    suggested_movie=[]
    suggested_movie_poster=[]
    for i in movie_list:
        movie_id=movies_list.iloc[i[0]].movie_id
        suggested_movie.append(movies_list.iloc[i[0]].title)
        suggested_movie_poster.append(fetch_image(movie_id))
        print("movie id : ",i[0])
    return suggested_movie, suggested_movie_poster


movie_option=st.selectbox(
        "Select Movie Name",
        (movies_list['title'].values))


if st.button('Suggestion'):
    suggested_movie, suggested_movie_poster= suggestion(movie_option)
    col1, col2, col3, col4,col5 = st.columns(5)

    with col1:
            st.text(suggested_movie[0])
            st.image(suggested_movie_poster[0])

    with col2:
        st.text(suggested_movie[1])
        st.image(suggested_movie_poster[1])

    with col3:
        st.text(suggested_movie[2])
        st.image(suggested_movie_poster[2])
    with col4:
        st.text(suggested_movie[3])
        st.image(suggested_movie_poster[3])
    with col5:
        st.text(suggested_movie[4])
        st.image(suggested_movie_poster[4])

