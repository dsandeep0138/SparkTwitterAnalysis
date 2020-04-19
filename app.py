from flask import Flask, render_template, request
import sys, ast, os
from wordcloud import WordCloud

app = Flask(__name__)
app.config['IMAGES_PATH'] = os.path.join('static', 'images')

tweets = {'users': [], 'text': []}
word_counts = {'words': [], 'counts': []}

@app.route("/")
def home_page():
    global tweets
    global word_counts
    
    print(word_counts['words'], file=sys.stderr)
    img_path = os.path.join(app.config['IMAGES_PATH'], 'wordcloud.jpg')
    
    wc = dict(zip(word_counts['words'], word_counts['counts']))
    
    wordcloud = WordCloud()
    wordcloud.generate_from_frequencies(frequencies = wc)
    wordcloud.to_file(img_path)

    return render_template(
            'hello.html',
            tweets=tweets['text'],
            words=word_counts['words'],
            img_path=img_path)

@app.route('/update_tweets', methods=['POST'])
def update_tweet_data():
    global tweets
    
    print(request.form)
    
    tweets['users'] = ast.literal_eval(request.form['user'])
    tweets['text'] = ast.literal_eval(request.form['text'])
    
    return "success", 200

@app.route('/update_counts', methods=['POST'])
def update_counts():
    global word_counts
    
    print(request.form)
    
    word_counts['words'] = ast.literal_eval(request.form['words'])
    word_counts['counts'] = ast.literal_eval(request.form['counts'])
    
    return "success", 200
    
@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response
    
if __name__ == "__main__":
    app.run(debug = True)