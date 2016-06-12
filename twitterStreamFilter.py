import oauth2 as oauth
import urllib2 as urllib

# See assignment1.html instructions or README for how to get these credentials

api_key = "changeit"
api_secret = "changeit"
access_token_key = "changeit"
access_token_secret = "changeit"

_debug = 0

oauth_token = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=api_key, secret=api_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"


http_handler = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)

'''
Construct, sign, and open a twitter request
using the hard-coded credentials above.
'''
def twitterreq(url, method, parameters):
    req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                               token=oauth_token,
                                               http_method=http_method,
                                               http_url=url,
                                               parameters=parameters)
    
    req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)
    
    headers = req.to_header()
    
    if http_method == "POST":
        encoded_post_data = req.to_postdata()
    else:
        encoded_post_data = None
        url = req.to_url()


    opener = urllib.build_opener(
                                 urllib.HTTPHandler(),
                                 urllib.HTTPSHandler()
								 )

    urllib.install_opener(opener)

    
    response = opener.open(url, encoded_post_data)

    
    return response

def fetchsamples():

    url = "https://stream.twitter.com/1.1/statuses/filter.json"
    
    #flight
    parameters = {'track':' flight '}
    
    #car
    #parameters = {'track':' car '}

    response = twitterreq(url, "POST", parameters)
    #print "{'results': ["
    for line in response:
        print line.strip() + ","

    #TODO Nota: el json final se consigue tratandolo de la siguiente forma: 
    #1.- Se eliminan los tweets sin geolocalizacion y nos quedamos con los de EEUU (utilizando el notepad++ y su utilidad de marcar lineas y borrar lineas no marcadas)
    #2.- Se anade la cabecera para tener un array: <<{"results": [>>
    #3.- Se elimina la ultima coma de la ultima linea
    #4.- Se anade el cierre del array: <<]}>> en la ultima fila 
    
if __name__ == '__main__':  
    fetchsamples()
