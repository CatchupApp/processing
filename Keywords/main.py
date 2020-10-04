import os

if 'GOOGLE_APPLICATION_CREDENTIALS' not in os.environ:
    # os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '../../credentials.json'
    pass

from audio_to_text import transcribe_file
from google.cloud import storage
from io import BytesIO
import mongo
import wave

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

    client = storage.Client()

    bucket = client.get_bucket('catchup-app')
    blob = storage.Blob(name, bucket)

    output = BytesIO()

    client.download_blob_to_file(blob, output)
    output.seek(0)

    with wave.open(output) as f:
        channels = f.getnchannels()

    output.seek(0)

    response = transcribe_file(output, channels)
    response = [paragraph.to_json() for paragraph in response]

    mongo.set_keyword_data(file["name"], response)

    print("File {} processed.".format(file["name"]))

# process_audio({"bucket": "catchup-app", "name": "audio/test.wav"}, {})