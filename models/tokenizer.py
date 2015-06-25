# coding=utf-8
from os import path
import codecs, re

class Tokenizer():
    """creates one tokenized file for all the texts assigend to a cathegory"""

    def __init__(self):
        self.src_file_path = path.join(path.dirname(__file__), "../data/training/raw/")
        self.dest_file_path = path.join(path.dirname(__file__), "../data/training/")
        self.cathegories  = {
            "fairytales": [
                "alice_im_wunderland.txt", 
                "mann_im_mond.txt", 
                "peterchens_mondfahrt.txt"
            ],
            "prosa": [
                "briefe_an_eine_freundin.txt"
            ]
        }
        
    def parse_files(self, cathegory, filenames):
        """loops through the given file paths and creates a clean tokeniced file from them

        - When sentence boundaries are found they are stored as a '<S/>' Symbol
        - Numbers are stores as <number>
        - abbreviations become <abbrevation>
        - one letter words become <unkown>

        the resulting string is written to a file with the given cathegory name 
        """
        res = ""
        for filename in filenames:
            filepath = path.join(self.src_file_path, filename)

            f = codecs.open(filepath, mode="r", encoding="utf-8")
            content = f.read()
            f.close()

            # strip special characters. Note that "." is not removed yet
            content = re.sub(ur'[\]\[!"“„#$%&\\\'()*+,\/:;<=>?@\^_\-–»«]', "", content).lower()

            # common abbreviations 
            # from http://www.sekretaerinnen-service.de/newsletterarticle.asp?his=17.42.55.3798&id=6255 (25.06.2015)
            # just treat them all as the same word
            content = re.sub(ur"abs\.|abschn\.|abt\.|a\. d\.|adr\.|allg\.|anh\.|anm\.|ao\.|a\. o\.|art\.|bd\.|bez\.|bzw\.|dgl\.|d\. h\.|d\. j\.|d\. m\.|dz\.|ev\.|röm-kath\.|evtl\.|f\.|ff\.|gem\.|h\. c\.|i\. allg\.|i\. r\.|jg\.|Jgg\.|lfd\.|kap\.|nr\.|o\. ä\.|p\. a\.|pp\.|ppa\.|prov\.|tfxu\.|a\.|u\. a\.|u\. a\. m\.|u\. ä\.|u\. d\. ä\.|u\. dgl\.|usf\.|usw\.|z\. t\.|zz\.", " <abbrevation> ", content)

            # find boundaries of sentences
            content = re.sub(ur"([a-z])\.\s([A-Z0-9])", r"\1 <S/> \2", content)
            content = re.sub(ur"\.$", " <S/> ", content, flags=re.MULTILINE)

            # now remove dots
            content = re.sub(ur"\.", " ", content)

            # replace numbers with <number>
            content = re.sub(ur"\d+", " <number> ", content)
            
            words = content.split()
            # replace one letter word with <unkown>
            for i, word in enumerate(words):
                if len(word) <= 1:
                    words[i] = " <unkown> "

            res += " ".join(words)

        print cathegory + ":", len(res), "words"
        token_filepath = path.join(self.dest_file_path, cathegory + ".txt")
        token_file = codecs.open(token_filepath, mode="w", encoding="utf-8")
        token_file.write(res)
        token_file.close()

    def tokenize(self):
        for cathegory_name in self.cathegories:
            files = self.cathegories[cathegory_name]
            self.parse_files(cathegory=cathegory_name, filenames=files)

t = Tokenizer()
t.tokenize()
