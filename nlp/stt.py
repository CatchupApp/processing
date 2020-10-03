import os
from pydub.utils import mediainfo

credential_path = os.environ["HOME"] + "/google-config/catchup.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path


class SpeechWord:
    def __init__(self, word, start, end):
        self.word = word
        self.start = start
        self.end = end


class SpeechParagraph:
    def __init__(self, transcript, confidence, words):
        self.text = transcript
        self.confidence = confidence
        self.words = words


def transcribe_file(speech_file):
    """
    Transcribe the given audio file.

    """
    from google.cloud import speech
    import io

    client = speech.SpeechClient()

    with io.open(speech_file, "rb") as audio_file:
        content = audio_file.read()

    minfo = mediainfo(speech_file)
    sample_rate = int(minfo['sample_rate'])
    num_channels = int(minfo['channels'])

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        language_code="en-US",
        enable_word_time_offsets=True,
        enable_automatic_punctuation=True,
        sample_rate_hertz=sample_rate,
        audio_channel_count=num_channels
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


if __name__ == "__main__":
    file_transcription = transcribe_file("test_files/test_2.wav")
    print(file_transcription)
