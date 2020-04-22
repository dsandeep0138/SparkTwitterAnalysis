from flask import Flask, render_template, request
import sys, ast, os
from wordcloud import WordCloud

app = Flask(__name__)
app.config['IMAGES_PATH'] = os.path.join('static', 'images')

tweets = {'users': ['RchavezRuben'], 'text': ['RT @KenDilanianNBC: Imagine if, two months ago, a competent federal government had led a World War II-level effort to ramp up production of…']}
word_counts = {'words': ['#SocialDistancing'], 'counts': [16]}
img_path = os.path.join(app.config['IMAGES_PATH'], 'wordcloud.jpg')
jqCloud_word_count = []

@app.route("/")
def home_page():
    global tweets
    global word_counts
    global img_path
    global jqCloud_word_count

    print("Tweets variable", file=sys.stderr)
    print(tweets , file=sys.stderr)
    print("word count variable", file=sys.stderr)
    print(word_counts , file=sys.stderr)
	
    print(word_counts['words'], file=sys.stderr)
    img_path = os.path.join(app.config['IMAGES_PATH'], 'wordcloud.jpg')
    
    wc = dict(zip(word_counts['words'], word_counts['counts']))
    
    wordcloud = WordCloud()
    wordcloud.generate_from_frequencies(frequencies = wc)
    wordcloud.to_file(img_path)

    jqCloud_word_count = [{'text': word, 'weight': count} for word, count in wc.items()]

    return render_template(
            'hello.html',
            tweets=tweets['text'],
            words=word_counts['words'],
            img_path=img_path,
            jqCloud_word_count=jqCloud_word_count)

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
    print("Updated word counts - ",  word_counts)
    return "success", 200


@app.route('/refresh_counts', methods=['Get'])
def refresh_counts():
    global word_counts
    global img_path
    wc = dict(zip(word_counts['words'], word_counts['counts']))
    wordcloud = WordCloud()
    wordcloud.generate_from_frequencies(frequencies = wc)
    wordcloud.to_file(img_path)
    return "success", 200

@app.route('/word_cloud', methods=['GET'])
def word_cloud():
    import json
    global jqCloud_word_count
    global word_counts
    wc = dict(zip(word_counts['words'], word_counts['counts']))
    jqCloud_word_count = [{'text': word, 'weight': count} for word, count in wc.items()]
    output = json.dumps(jqCloud_word_count)
    print(output)
    return output

@app.route('/tweets', methods=['GET'])
def tweets_refresh():
    import json
    global tweets
    output = json.dumps(tweets['text'])
    print(output)
    return output

@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response
    
if __name__ == "__main__":
    app.run(debug = True)