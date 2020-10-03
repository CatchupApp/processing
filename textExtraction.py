#SUMMA SUCKS ASS USE THE GOOGLE ClOUD EQUIVALENT FOR ALL FUNCTIONS

from summa import summarizer, keyword
from google.cloud import language_v1
from google.cloud.language_v1 import enums


def format_paragraphs_gc(text):
    """Formats paragraphs based on google cloud automatic formatting"""
    return text.split("\n")

def format_paragraphs(text, max_keys=8):
    """Formats paragraphs based on summa keywords"""
    text = text.replace("\n", "").replace("\t", " ").split()
    paragraphs = []
    paragraph = ""
    for i in range(len(text)):
        paragraph+=text[i]
        if len(keywords.keywords(paragraph).split("\n")) >= 8 :
            paragraphs.append(paragraph)
            paragraph=""
        return paragraphs

def get_text_extraction(text):
    """gets text extraction of each paragraph and makes them a bullet"""
    bullets = []
    for i in format_paragraphs_gc(text):
        bullets.append(summarizer.summarize(i, ratio=0.4))

    return {"bullets" : bullets}

def get_text_extraction_indiv(text):
    """gets text extraction of any individual block of text"""
    return {"bullet" : summarizer.summarize(text, ratio=0.4).replace("\n", "").replace("\t", " ")}

def get_salient_entities(text, top_n=5):
    """Gets all entities and sorts them in order of salience. returns a list of the top n salient entities. Uses google cloud"""
    pass

def get_text_extraction_gc(text, max_per_para = 2):
    """Gets text extraction using google cloud salience"""

    entities = set(get_salient_entities(text))
    bullets = []
    ranks = []
    for i in format_paragraphs_gc(text):

        ranker = {}
        for j in i.split("."):
            score = 0
            for k in j.split():
                if k in entities:
                    score+=1
            ranker.update({score: j})

        ranks.append(ranker)

    for i in ranks:
        bullet = ""
        for j in sorted(i.keys()[-max_per_para:]):
            bullet+=i[j]+"\t"

        bullets.append(bullet)

    return {"bullets" : bullets}

def get_keywords_mentions_scores(text_content):
    """
    Analyzing Entities in a String.

    Args:
      text_content The text content to analyze

    Gets the salience (importance) scores of each entity, the mentions of that entity in the text, and the metadata of each entity
    """

    client = language_v1.LanguageServiceClient()

    type_ = enums.Document.Type.PLAIN_TEXT

    language = "en"
    document = {"content": text_content, "type": type_, "language": language}

    encoding_type = enums.EncodingType.UTF8

    response = client.analyze_entities(document, encoding_type=encoding_type)

    scores = {}
    mentions = {}
    meta = {}

    for entity in response.entities:
        #print(u"Representative name for the entity: {}".format(entity.name))

        #print(u"Entity type: {}".format(enums.Entity.Type(entity.type).name))

        #print(u"Salience score: {}".format(entity.salience))

        scores[entity.name] = entity.salience
        mentions[entity.name] = []
        meta[entity.name] = {}

        for metadata_name, metadata_value in entity.metadata.items():
            #print(u"{}: {}".format(metadata_name, metadata_value))
            meta[entity.name][metadata_name] = metadata_value

        for mention in entity.mentions:
            #print(u"Mention text: {}".format(mention.text.content))

            #print(
            #    u"Mention type: {}".format(enums.EntityMention.Type(mention.type).name)
            #)

            mentions[entity.name].append(mention.text.content)

    #print(u"Language of the text: {}".format(response.language))

    return {"Scores" : scores, "Mentions" : mentions, "Metadata" : meta}
