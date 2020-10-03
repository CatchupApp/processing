import google.cloud.language_v1

from google.cloud import language_v1
from google.cloud.language_v1 import enums

client = google.cloud.language_v1.LanguageServiceClient.from_service_account_file('../credentials.json')

def get_keywords(text_content):
    """
    Analyzing Entities in a String.

    Args:
      text_content The text content to analyze

    Gets the salience (importance) scores of each entity, the mentions of that entity in the text, and the metadata of each entity
    """

    type_ = enums.Document.Type.PLAIN_TEXT
    language = "en"
    document = {"content": text_content, "type": type_, "language": language}

    encoding_type = enums.EncodingType.UTF8

    response = client.analyze_entities(document, encoding_type=encoding_type)

    entities = {}
    for entity in response.entities:
        entities[entity.name] = {
            'salience': entity.salience,
            'mentions': [],
            'meta': {}
        }

        for metadata_name, metadata_value in entity.metadata.items():
            entities[entity.name]['meta'][metadata_name] = metadata_value

        for mention in entity.mentions:
            entities[entity.name]['mentions'].append(mention.text.content)
    
    return entities
