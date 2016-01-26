import requests
import codecs
import os

url_translate = 'https://www.googleapis.com/language/translate/v2'  # Google Translate URL
url_languages = 'https://www.googleapis.com/language/translate/v2/languages' # Google supported languages JSON 

payload = {
    'key':      None
,   'q':        'We are what we repeatedly do; excellence, then, is not an act but a habit.'
,   'format':   'text'
,   'source':   'en'
,   'target':   'en'
}  # Params passed to the URL

google_api_key = ''  # Store the Google Translate API here
with open('google_api_key', 'r') as key_file:
    payload['key'] = key_file.read()
    
# Get the list of supported languages
response = requests.get(url=url_languages, params={'key': payload['key']}).json()

# PART 1: Translate to every language available, using the previous translation as source
if not os.path.isfile('output_pass_1.txt'):
    with codecs.open("output_pass_1.txt", "w", "utf-8") as out_file_1:
        for lang in response['data']['languages']:
            payload['target'] = lang['language']  # translate to this language
            # payload['q'] = urllib.parse.quote_plus(payload['q'])
            translation_response = requests.get(url=url_translate, params=payload).json()
            payload['source'] = lang['language']  # set the new language as the new string language
            payload['q'] = translation_response['data']['translations'][0]['translatedText'] # set the translation as the source text
            out_file_1.write("%s:%s\n" % (lang['language'], payload['q'])) # write the results to the file
            print(payload['q'])
else:
    print('Part 1 already performed. Skipping...')

# PART 2: For every translation, translate back to English! See how the meaning get's altered after every translation

payload['target'] = 'en'

with codecs.open("output_pass_1.txt", "r", "utf-8") as out_file_1:
    content = out_file_1.readlines()  # Convert all the translations to a list

out_file_2 = codecs.open("output_pass_2.txt", "w", "utf-8")
for line in content:
    line=line.replace('\n', '')  # remove newlines
    payload['source'], payload['q'] = line.split(':')
    if payload['source'] == 'en':  # skip translating to English
        continue
    translation_response = requests.get(url=url_translate, params=payload).json()
    translated_text = translation_response['data']['translations'][0]['translatedText']
    out_file_2.write("%s:%s\n" % (payload['source'], translated_text)) # write the results to the file
    print(translated_text)
out_file_2.close()
