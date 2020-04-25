from flask import Flask, render_template, request
import sys, ast, os, json
from wordcloud import WordCloud
import plotly
import plotly.graph_objects as go

app = Flask(__name__)
app.config['IMAGES_PATH'] = os.path.join('static', 'images')

tweets = {'users': ['RchavezRuben'], 'text': ['RT @KenDilanianNBC: Imagine if, two months ago, a competent federal government had led a World War II-level effort to ramp up production of…']}
sentiments = {'positive': 23, 'neutral': 23, 'negative': 4, 'total': 50}
hashtag_counts = {'words': ['#SocialDistancing'], 'counts': [16]}
word_counts = {'words': ['COVID19'], 'counts': [16]}
geodata = {'longitude': [], 'latitude': []}
img_path = os.path.join(app.config['IMAGES_PATH'], 'wordcloud.jpg')
jqCloud_word_count = []
graphJSON = {}


@app.route("/")
def home_page():
    global tweets
    global sentiments
    global hashtag_counts
    global word_counts
    global geodata
    global graphJSON
    global img_path
    global jqCloud_word_count

    print("Tweets variable", file=sys.stderr)
    print(tweets, file=sys.stderr)
    print("word count variable", file=sys.stderr)
    print(word_counts, file=sys.stderr)
    print("hashtag variable", file=sys.stderr)
    print(hashtag_counts, file=sys.stderr)
	
    print(hashtag_counts['words'], file=sys.stderr)
    img_path = os.path.join(app.config['IMAGES_PATH'], 'wordcloud.jpg')
    
    wc = dict(zip(hashtag_counts['words'], hashtag_counts['counts']))
    
    wordcloud = WordCloud()
    wordcloud.generate_from_frequencies(frequencies = wc)
    wordcloud.to_file(img_path)

    jqCloud_word_count = [{'text': word, 'weight': count} for word, count in wc.items()]

    trace = go.Scattergeo(lon = geodata['longitude'],
                          lat = geodata['latitude'],
                          mode = 'markers')
    data = [trace]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template(
            'hello.html',
            tweets=tweets['text'],
            sentiments=sentiments,
            words=word_counts['words'],
            img_path=img_path,
            jqCloud_word_count=jqCloud_word_count,
            graphJSON=graphJSON)


@app.route('/update_geodata', methods=['POST'])
def update_geodata():
    global geodata

    geodata['longitude'] = ast.literal_eval(request.form['longitude'])
    geodata['latitude'] = ast.literal_eval(request.form['latitude'])
    
    return "success", 200


@app.route('/update_tweets', methods=['POST'])
def update_tweet_data():
    global tweets
    
    print(request.form)
    
    tweets['users'] = ast.literal_eval(request.form['user'])
    tweets['text'] = ast.literal_eval(request.form['text'])
    
    return "success", 200


@app.route('/update_sentiments', methods=['POST'])
def update_sentiments():
    global sentiments

    print(request.form)

    sentiments['positive'] = ast.literal_eval(request.form['positive'])
    sentiments['neutral'] = ast.literal_eval(request.form['neutral'])
    sentiments['negative'] = ast.literal_eval(request.form['negative'])
    sentiments['total'] = ast.literal_eval(request.form['total'])

    if sentiments['total'] > 0:
        sentiments['positive'] = round(sentiments['positive'] / sentiments['total'], 2)
        sentiments['neutral'] = round(sentiments['neutral'] / sentiments['total'], 2)
        sentiments['negative'] = round(sentiments['negative'] / sentiments['total'], 2)

    return "success", 200


@app.route('/update_counts', methods=['POST'])
def update_counts():
    global word_counts
    
    print(request.form)
    
    word_counts['words'] = ast.literal_eval(request.form['words'])
    word_counts['counts'] = ast.literal_eval(request.form['counts'])
    print("Updated word counts - ",  word_counts)
    return "success", 200


@app.route('/update_hashtagcounts', methods=['POST'])
def update_hashtagcounts():
    global hashtag_counts
    
    print(request.form)
    
    hashtag_counts['words'] = ast.literal_eval(request.form['words'])
    hashtag_counts['counts'] = ast.literal_eval(request.form['counts'])
    print("Updated hashtag counts - ",  hashtag_counts)
    return "success", 200


@app.route('/refresh_hashtagcounts', methods=['GET'])
def refresh_hashtagcounts():
    global hashtag_counts
    global img_path
    wc = dict(zip(hashtag_counts['words'], hashtag_counts['counts']))
    wordcloud = WordCloud()
    wordcloud.generate_from_frequencies(frequencies = wc)
    wordcloud.to_file(img_path)
    return "success", 200


@app.route('/word_cloud', methods=['GET'])
def word_cloud():
    global jqCloud_word_count
    global hashtag_counts
    wc = dict(zip(hashtag_counts['words'], hashtag_counts['counts']))
    jqCloud_word_count = [{'text': word, 'weight': count} for word, count in wc.items()]
    output = json.dumps(jqCloud_word_count)
    print(output)
    return output


@app.route('/tweets', methods=['GET'])
def tweets_refresh():
    global tweets
    output = json.dumps(tweets['text'])
    print(output)
    return output


@app.route('/word_counts', methods=['GET'])
def refresh_counts():
    global word_counts
    output = json.dumps(word_counts['words'])
    print(output)
    return output


@app.route('/sentiments', methods=['GET'])
def refresh_sentiments():
    global sentiments
    print(sentiments)
    return sentiments


@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


if __name__ == "__main__":
    app.run(debug = True)
