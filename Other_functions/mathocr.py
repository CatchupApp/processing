import requests
import base64
import wolframalpha
import wikipedia

appId = 'APER4E-58XJGHAVAK'
client = wolframalpha.Client(appId)

def eq_from_str(imgstr, token="solve"):
    """Args:
            imgstr: an image in b64 string form
            token: the wolframalpha query (e.g. solve, derivative, limit, etc.)

        returns the result of the wolframalpha query

        e.g. 'derivative y=x^2' returns 'y=2x'
    """

    eq = get_eq(imgstr)
    return search(token+" "+eq)

def eq_from_img(path, token="solve"):
    """Args:
            path: path to image
            token: the wolframalpha query (e.g. solve, derivative, limit, etc.)

        returns the result of the wolframalpha query

        e.g. 'derivative y=x^2' returns 'y=2x'
    """

    imgstr = get_str_from_img(path)
    return eq_from_str(imgstr, token)

    

def get_str_from_img(path):
    return base64.b64encode(open(path, "rb").read())

def get_eq(imgstr):

    headers = {
          "content-type": "application/json",
          "app_id": "YOUR_APP_ID",
          "app_key": "YOUR_APP_KEY"
        }

    data = {
            "src": "data:image/jpeg;base64,"+imgstr,
            "formats": ["text", "data", "html"],
            "data_options": {
                "include_asciimath": True,
                "include_latex": True
            }
        }




    r = requests.post('https://api.mathpix.com/v3/text', data=data, headers=headers)

    response = r.json()

    eq = response["data"][0]["value"]

    return eq

def search_wiki(keyword=''):
    searchResults = wikipedia.search(keyword)
    if not searchResults:
        return
    try:
        page = wikipedia.page(searchResults[0])
    except wikipedia.DisambiguationError as err:
        page = wikipedia.page(err.options[0])

    wikiTitle = str(page.title.encode('utf-8'))
    wikiSummary = str(page.summary.encode('utf-8'))
    return wikiSummary

def search(text=''):
    res = client.query(text)
    if res['@success'] == 'false':
        print("Try Again")
    else:
        result = ''
        pod0 = res['pod'][0]
        pod1 = res['pod'][1]
        if (('definition' in pod1['@title'].lower()) or ('result' in  pod1['@title'].lower()) or (pod1.get('@primary','false') == 'true')):
            result = resolveListOrDict(pod1['subpod'])
            result = result.replace('Wolfram|Alpha', 'Ingram')
            question = resolveListOrDict(pod0['subpod'])
            question = removeBrackets(question)
            primaryImage(question)
        else:
            question = resolveListOrDict(pod0['subpod'])
            question = removeBrackets(question)
            search_wiki(question)
            primaryImage(question)
    return result

def removeBrackets(variable):
    return variable.split('(')[0]

def resolveListOrDict(variable):
    if isinstance(variable, list):
        return variable[0]['plaintext']
    else:
        return variable['plaintext']

def primaryImage(title=''):
    url = 'http://en.wikipedia.org/w/api.php'
    data = {'action':'query', 'prop':'pageimages','format':'json','piprop':'original','titles':title}
    try:
        res = requests.get(url, params=data)
        key = res.json()['query']['pages'].keys()[0]
        imageUrl = res.json()['query']['pages'][key]['original']['source']
        return imageUrl
    except Exception as err:
        print('')
        return ''

#print(search('solve y=x^2'))
