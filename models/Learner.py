# coding=utf-8
import codecs
import re

class Learner():
  '''Parses text files to generate n-grams and cathegories

    detailed info here
    '''

  def __init__(self):
    self.parse_file('wiki_00')

  def parse_file(self, file_path):
    f = codecs.open(file_path, mode='r', encoding='utf-8')
    content = f.read()

    # strip xml <doc> tags
    content = re.sub(r'<doc.*>|<\/doc>', '', content)

    # strip special characters note "." is not removed yet
    content = re.sub(u'[\]\[!"“„#$%&\\\'()*+,\/:;<=>?@\^_`{|}~-]', '', content)

    # find boundaries of sentences
    content = re.sub(ur'([a-z])\.\s([A-Z0-9])', r'\1 <S/> \2', content)
    content = re.sub(ur'\.$|^\b', ' <S/> ', content, flags=re.MULTILINE)

    # TO DO:
    # maybe add a list of common abbrevations to remove socres from them here

    words = content.split()

    # TO DO:
    # implement algorythm thoughts

    print words

Learner()