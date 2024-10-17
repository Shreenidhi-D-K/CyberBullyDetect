from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


import re
import string
import joblib
import nltk
nltk.download('stopwords')
nltk.download('wordnet')

from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
from nltk.stem import WordNetLemmatizer


# Load the logistic regression model

# !!! EDIT YOUR MODEL AND VECTORIZER JOBLIB PATHS HERE
# SVMmodel.joblib and SVMvectorizer.joblib should be available in the same folder
# Search for it and mention their path inside joblib.load() given below
# model = joblib.load(---path to SVMmodel.joblib---)
# vectorizer = joblib.load(---path to SVMvectorizer.joblib---)
# These files are extracted from google colab code
model = joblib.load('C:\\Users\\Shreenidhi\\Desktop\\CyberbullyWebsite\\SVMmodel.joblib')
vectorizer = joblib.load('C:\\Users\\Shreenidhi\\Desktop\\CyberbullyWebsite\\SVMvectorizer.joblib')


emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)

def lem_preprocess_text(text):
    # Convert text to lowercase
    text = text.lower()

    # Remove Twitter user tags
    text = re.sub(r'@[A-Za-z0-9]+', '', text)

    # Remove URLs
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'www.\S+','',text)
    text = re.sub(r'\d+', '', text)
    text = emoji_pattern.sub(r'', text)

    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))

    # Tokenization
    tokenizer = TweetTokenizer()
    tokens = tokenizer.tokenize(text)

    # Remove stopwords
   # tokens = [str(TextBlob(token).correct()) for token in tokens]
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]

    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]

    # Join tokens back into text
    preprocessed_text = ' '.join(tokens)

    return preprocessed_text
# Define a route for classification
@app.route('/')
def HelloWorld():
    return "Hello World"

@app.route('/classify', methods=['POST'])
def classify_text():
    print("Recieved text:")
    # Get the text to classify from the request
    text = request.form['text']
    print(text)

    # Check if text is already a 2D array
    text_vectorized = vectorizer.transform([text])
    if text_vectorized.ndim == 1:
        # Reshape the text to a 2D array
        text_vectorized = text_vectorized.reshape(1, -1)

    # Use the model to classify the text
    result = model.predict(text_vectorized)[0]
    if(result==1):
        return jsonify({'result': 'Cyberbully'})
    else:
        return jsonify({'result': 'Not Cyberbully'})
    # Return the classification result as JSON
    

# def upload_file():
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file part'}), 400

#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({'error': 'No selected file'}), 400

#     data = pd.read_csv(file)
#     # Process the CSV file (e.g., use the trained model to classify data)
#     data['lemText'] = data['textInput'].apply(lem_preprocess_text)

#     lem_X = data['lemText']
#     lem_y = data['CBvalue']

#     newdf = model.predict(df)
#     # For demonstration, save the processed data to a new CSV file
#     newdf.to_csv('processed_data.csv', index=False)

#     # Return the processed CSV file for download
#     return send_file('processed_data.csv', as_attachment=True)

if __name__ == '__main__':
    app.debug=True
    app.run(host='localhost', port=5000)

