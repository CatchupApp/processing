from google.cloud import speech
import os
import wave

import text_to_keywords

# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '../../credentials.json'
client = speech.SpeechClient()

class SpeechWord:
    def __init__(self, word, start, end):
        self.word = word
        self.start = start
        self.end = end

    def to_json(self):
        return {
            "word": self.word,
            "start": self.start,
            "end": self.end
        }

class SpeechParagraph:
    def __init__(self, transcript, confidence, words):
        self.text = transcript
        self.confidence = confidence
        self.words = words
        self.keywords = text_to_keywords.get_keywords(self.text)

    def to_json(self):
        return {
            "text": self.text,
            "confidence": self.confidence,
            "words": [word.to_json() for word in self.words],
            "keywords": self.keywords
        }

def transcribe_file(content, channels=2):
    """
    Transcribe the given audio file.
    """

    audio = speech.RecognitionAudio(content=content.read())
    config = speech.RecognitionConfig(
        language_code="en-US",
        enable_word_time_offsets=True,
        enable_automatic_punctuation=True,
        # sample_rate_hertz=sample_rate,
        audio_channel_count=channels
    )

    response = client.recognize(request={"config": config, "audio": audio})

    res = []
    for result in response.results:
        alternative = result.alternatives[0]
        transcript = alternative.transcript
        confidence = alternative.confidence

        words = []

        for word_info in alternative.words:
            word = word_info.word
            start = word_info.start_time.total_seconds()
            end = word_info.end_time.total_seconds()

            words.append(SpeechWord(word, start, end))

        res.append(SpeechParagraph(transcript, confidence, words))
        
    return res
