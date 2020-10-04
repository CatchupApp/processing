import os

if 'GOOGLE_APPLICATION_CREDENTIALS' not in os.environ:
    # os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '../../credentials.json'
    pass

# from audio_to_text import transcribe_file
# from google.cloud import storage
from google.cloud import videointelligence
# from io import BytesIO
import mongo
import text_to_keywords
# import wave

def validate_message(message, param):
    var = message.get(param)
    if not var:
        raise ValueError(
            "{} is not provided. Make sure you have \
                          property {} in the request".format(
                param, param
            )
        )
    return var

def process_audio(file, context):
    bucket = validate_message(file, "bucket")
    name = validate_message(file, "name")

    print("Starting transcription for", bucket, " / " , name)

    video_client = videointelligence.VideoIntelligenceServiceClient()
    
    # maybe add other features here?
    features = [videointelligence.enums.Feature.SPEECH_TRANSCRIPTION]

    config = videointelligence.types.SpeechTranscriptionConfig(
        language_code="en-US", enable_automatic_punctuation=True
    )

    video_context = videointelligence.types.VideoContext(
        speech_transcription_config=config
    )

    operation = video_client.annotate_video(
        input_uri=f"gs://{bucket}/{name}", features=features, video_context=video_context
    )

    transcriptions = []

    annotation_results = operation.result(timeout=600)
    first_result = annotation_results.annotation_results[0]
    speech_transcriptions_raw = first_result.speech_transcriptions

    for result in speech_transcriptions_raw:
        alternative = result.alternatives[0]
        transcript = alternative.transcript
        confidence = alternative.confidence

        words = []
        for word_info in alternative.words:
            word = word_info.word
            start = word_info.start_time.seconds + 1e-9 * word_info.start_time.nanos
            end = word_info.end_time.seconds + 1e-9 * word_info.end_time.nanos

            words.append({"word": word, "start": start, "end": end})

        keywords = text_to_keywords.get_keywords(transcript)

        transcriptions.append({
            "transcript": transcript,
            "confidence": confidence,
            "words": words,
            "keywords": keywords
        })

    # response = transcribe_file(output, channels)
    # response = [paragraph.to_json() for paragraph in response]

    mongo.set_keyword_data(file["name"], transcriptions)

    print("File {} processed.".format(file["name"]))

    return transcriptions

# process_audio({"bucket": "catchup-app", "name": "test_video.mp4"}, {})