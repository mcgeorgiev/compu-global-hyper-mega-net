#import pywikibot
# from pywikibot import pagegenerators
#
# site = pywikibot.Site()
# cat = pywikibot.Category(site,'Category:American_male_film_actors')
# gen = pagegenerators.CategorizedPageGenerator(cat)
# for page in gen:
#     print page.txt
#  # text = page.text
import requests

r = requests.get('https://en.wikipedia.org/wiki/Category:American_male_film_actors')
print r.content
