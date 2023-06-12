from flask import Flask,render_template,request
import pickle
import numpy as np
import pandas as pd
import bz2file as bz2

# Reading the compressed data 
 
ifile = bz2.BZ2File("URL.pkl",'rb')
URL = pickle.load(ifile)
ifile.close()

sfile = bz2.BZ2File("similar_URL_score.pkl",'rb')
similar_URL_score = pickle.load(sfile)
sfile.close()

top_ids = pickle.load(open("top_ids.pkl",'rb'))
df = pickle.load(open('df.pkl','rb'))


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           category = list(top_ids['Category'].values),
                           product_id=list(top_ids['Product ID'].values),
                           num_ratings=list(top_ids['No. of Ratings'].values),
                           rating_per=list(top_ids['% Ratings'].values),
                           link=list(top_ids['URL'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_product',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(URL.index == user_input)[0][0]
    similar_url = sorted(list(enumerate(similar_URL_score[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_url:         
        item = []
        temp_df = df[df['URL'] == URL.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('URL')['Category'].values))    #recommend category 
        item.extend(list(temp_df.drop_duplicates('URL')['Product ID'].values)) #recommend id
        item.extend(list(temp_df.drop_duplicates('URL')['URL'].values))        #recommend url
        
        data.append(item)
    
    print(data)

    return render_template('recommend.html',data=data)

if __name__ == '__main__':
    app.run(debug=True)