 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import joblib
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import string
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
import json
import sklearn 
from django.conf import settings
# Initialize the PorterStemmer
stemmer = PorterStemmer()

class _PassthroughScorer:
    pass

sklearn.metrics._scorer._PassthroughScorer = _PassthroughScorer

# Load the trained model
model_path = settings.MODEL_PATH
predictor = joblib.load(model_path)

# Define stop words and punctuation
stop_words = ENGLISH_STOP_WORDS
punctuation_chars = string.punctuation + '-'
table = str.maketrans('', '', punctuation_chars)

class SentimentAnalysisView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        try:
            data = json.loads(request.body)
            sentence = data.get('sentence', '')
            
            if not sentence.strip():
                return JsonResponse({'error': 'The sentence cannot be empty.'}, status=400)
            
            if isinstance(sentence, str):
                soup = BeautifulSoup(sentence, 'html.parser')
                sentence = soup.get_text()
                words = word_tokenize(sentence)
                words = [word for word in words if word.lower() not in stop_words]
                filtered_sentence = " ".join([stemmer.stem(word).translate(table) for word in words])
            else:
                filtered_sentence = ""
            
            prediction = predictor.predict([filtered_sentence])
            sentiment = 'positive' if prediction[0] == 1 else 'negative'
            
            return JsonResponse({'sentiment': sentiment})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

