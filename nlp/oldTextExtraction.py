from summa import summarizer, keyword

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