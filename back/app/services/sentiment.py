from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

_analyzer = SentimentIntensityAnalyzer()

def sentiment_score(text:str) -> float:
    """
    Returns compound score in [-1,1].
    """
    return _analyzer.polarity_scores(text).get("compound", 0.0)
