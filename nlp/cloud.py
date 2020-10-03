from audio_to_text import transcribe_file

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

def process_image(file, context):
    bucket = validate_message(file, "bucket")
    name = validate_message(file, "name")

    transcribe_file(f"g://{bucket}/{name}")

    print("File {} processed.".format(file["name"]))