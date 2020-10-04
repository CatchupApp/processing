import requests
import base64
import wolframalpha
import wikipedia
import os
import json
import pyscreenshot as ps
import keyboard
from pynput import mouse
import sys

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

    #imgstr = get_str_from_img(path)
    #return eq_from_str(imgstr, token)
    eq = get_eq_os(str(get_str_from_img(path))[2:][:-1])
    return search(token + ' ' + eq)


def get_str_from_img(path):
    return base64.b64encode(open(path, "rb").read())



def get_eq_os(imgstr):

    data = ' \'{ "src": "data:image/jpeg;base64,' + imgstr + '" , "data_options" : {"include_asciimath" : true}, "formats" : ["text", "data", "html"] }\' '

    oscmd = 'curl -X POST https://api.mathpix.com/v3/text -H "appId: APP_ID" -H "app_key: APP_KEY" -H "Content-Type: application/json" --data '+data
    result = os.popen(oscmd).read()

    res = json.loads(result)

    return res['data'][0]['value']


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

class MyException(Exception):pass

global clicks
global numclicks

numclicks=0

clicks = {}

def capture_eq(TopLeft, TopRight):
    im=ps.grab(bbox=(TopLeft[0], TopLeft[1], TopRight[0], TopRight[1]))
    return im

def run_local():
    while True:
        if keyboard.is_pressed("c"):
            print("Click image bounds")

            with mouse.Listener(on_click=on_click) as listener:
                try:
                    listener.join()
                except MyException as e:
                    pass

def on_click(x, y, button, pressed):
    global clicks
    global numclicks

    numclicks+=0.5

    clicks[numclicks] = [x, y]


    if (numclicks >= 2):
        im = capture_eq(clicks[1.0], clicks[2.0])
        im = im.convert("RGB")
        im.save("equation.jpeg")
        print(eq_from_img("equation.jpeg"))
        sys.exit(0)




print(eq_from_img("blackeq.jpeg"))

#run_local()
