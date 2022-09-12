from flask import Flask,render_template,request
import pickle
import numpy as np
popular_df=pickle.load(open('popular.pkl','rb'))
pt=pickle.load(open('pt.pkl','rb'))
df_books=pickle.load(open('df_books.pkl','rb'))
similarity_scores=pickle.load(open('similarity_scores.pkl','rb'))
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df["Book-Title"].values),
                           author = list(popular_df["Book-Author"].values),
                           image =list(popular_df["Image-URL-L"].values),
                           rating =list(popular_df["avg_ratings"].values),
                           votes =list(popular_df["num_ratings"].values)
                           )
@app.route('/recommend')
def recommend_ui():
    return render_template("recommend.html")

@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input=request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similarity_items = sorted(list(enumerate(similarity_scores[index])), key=lambda X: X[1], reverse=True)[1:10]
    data = []
    for i in similarity_items:
        item = []
        temp_df = df_books[df_books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')["Book-Title"].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')["Book-Author"].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')["Image-URL-L"].values))
        data.append(item)

    print(data)
    return render_template('recommend.html',data=data)
if __name__ == "__main__":
    app.run(debug=True)