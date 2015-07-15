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
            ],
            "wants": [
                "nouns.txt"
            ]
        }

    def strip_special_characters(self, string):
        # strip special characters. Note that ".", "?" and "!" are not removed yet
        return re.sub(ur'[\]\["“„#$%&\\\'()*+,\/:;€<=>@\^_\-–»«]', " ", string)

    def replace_abbreviations(self, string):
        # common abbreviations 
        # from http://www.sekretaerinnen-service.de/newsletterarticle.asp?his=17.42.55.3798&id=6255 (25.06.2015)
        # just treat them all as the same word
        return re.sub(ur"Abs\.|Abschn\.|Abt\.|a\. d\.|Adr\.|allg\.|Anh\.|Anm\.|ao\.|a\. o\.|Art\.|Bd\.|Bez\.|bez\.|bzw\.|dgl\.|d\. h\.|d\. j\.|d\. M\.|dz\.|ev\.|röm-kath\.|evtl\.|f\.|ff\.|gem\.|h\. c\.|i\. allg\.|i\. r\.|Jg\.|Jgg\.|lfd\.|Kap\.|Nr\.|o\. Ä\.|p\. A\.|pp\.|ppa\.|prov\.|tfxu\.|a\.|u\. a\. m\.|u\. a\.|u\. A\.|u\. Ä\.|u\. d\. Ä\.|u\. dgl\.|usf\.|usw\.|z\. t\.|zz\.|z\. B\.", " <abbrevation> ", string)

    def find_sentence_boundaires(self, string):
        string = re.sub(ur"([a-z0-9<abbrevation>])[\.\?!]\s([A-Z0-9<abbrevation>])", r"\1 <S/> \2", string)
        string = re.sub(ur"[\.\?!]$", " <S/> ", string, flags=re.MULTILINE)
        # now remove dots etc.
        return re.sub(ur"[\.\?!]", " ", string)

    def replace_numbers(self, string):
        return re.sub(ur"\d+", " <number> ", string)

    def replace_unkown(self, string):
        res = ""
        words = string.split()
        # replace one letter word with <unkown>
        for i, word in enumerate(words):
            if len(word) <= 1:
                words[i] = " <unkown> "

        res += " ".join(words)
        return res

        
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

            content = self.strip_special_characters(content)
            content = self.replace_abbreviations(content)
            content = self.find_sentence_boundaires(content)
            content = self.find_sentence_boundaires(content)
            content = self.replace_numbers(content)
            content = self.replace_unkown(content)

            res = content.lower()

        token_filepath = path.join(self.dest_file_path, cathegory + ".txt")
        token_file = codecs.open(token_filepath, mode="w", encoding="utf-8")
        token_file.write(res)
        token_file.close()

    def tokenize(self):
        for cathegory_name in self.cathegories:
            files = self.cathegories[cathegory_name]
            self.parse_files(cathegory=cathegory_name, filenames=files)

# If the script is called directly, run it.
print __name__
if __name__ == '__main__':
    t = Tokenizer()
    t.tokenize()
