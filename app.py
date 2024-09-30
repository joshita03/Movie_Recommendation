'''from flask import Flask, render_template,request
import pickle

with open('tfidf_vectorizer2.pkl', 'rb') as f:
    tfidf_vectorizer = pickle.load(f)

with open('cosine_sim2.pkl', 'rb') as f:
    cosine_sim = pickle.load(f)

with open('movies_df.pkl', 'rb') as f:
    movies_df = pickle.load(f)

movies = movies_df['original_title'].tolist()


app=Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    recommendations = None
    if request.method == 'POST':
        movie_name = request.form['movie_name']
        recommendations = get_recommendations(movie_name, tfidf_vectorizer, cosine_sim)

    return render_template('home.html', recommendations=recommendations)

def get_recommendations(movie_name, tfidf_vectorizer, cosine_sim):
    # Transform input using TF-IDF vectorizer
    movie_tfidf = tfidf_vectorizer.transform([movie_name])

    # Ensure the shape of the TF-IDF vector matches the cosine similarity matrix
    if movie_tfidf.shape[1] != cosine_sim.shape[0]:
        raise ValueError("The dimensions of the TF-IDF vector do not match the cosine similarity matrix.")

    # Compute cosine similarities
    cosine_scores = cosine_sim.dot(movie_tfidf.T).flatten()

    # Get indices of top 10 similar movies
    similar_indices = cosine_scores.argsort()[:-11:-1]

    # Return list of top 10 similar movie names
    recommendations = [movies[i] for i in similar_indices]
    return recommendations'''


'''def get_recommendations(movie_name, tfidf_vectorizer, cosine_sim):
    movie_tfidf = tfidf_vectorizer.transform([movie_name])

    cosine_scores = cosine_sim.dot(movie_tfidf.T).toarray().flatten()

    similar_indices = cosine_scores.argsort()[:-11:-1]

    recommendations = [movies[i] for i in similar_indices]
    return recommendations'''





'''if __name__=="__main__":
    app.run(debug=True)'''

from flask import Flask, render_template, request
import pickle

with open('tfidf_vectorizer2.pkl', 'rb') as f:
    tfidf_vectorizer = pickle.load(f)

with open('cosine_sim2.pkl', 'rb') as f:
    cosine_sim = pickle.load(f)

with open('movies_df.pkl', 'rb') as f:
    movies_df = pickle.load(f)

movies = movies_df['original_title'].tolist()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    recommendations = None
    if request.method == 'POST':
        movie_name = request.form['movie_name']
        recommendations = get_recommendations(movie_name, tfidf_vectorizer, cosine_sim, movies_df)
    return render_template('home.html', recommendations=recommendations)

def get_recommendations(title, tfidf_vectorizer, cosine_sim, df):
    if title not in df['original_title'].values:
        return ["Movie title not found."]

    idx = df[df['original_title'] == title].index[0] #index in dataframe 
    sim_scores = list(enumerate(cosine_sim[idx])) #row in c matrix corresponding to idx
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    return df['original_title'].iloc[movie_indices].tolist()

if __name__ == "__main__":
    app.run(debug=True)
