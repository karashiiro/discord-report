import flair

flair_sentiment = flair.models.TextClassifier.load("sentiment")

def get_sentiment(text: str) -> float:
	s = flair.data.Sentence(text)
	flair_sentiment.predict(s)
	total_sentiment = s.labels
	if total_sentiment[0]._value == "POSITIVE":
		return total_sentiment[0]._score
	else:
		return total_sentiment[0]._score * -1
