# coding=utf-8
from os import path
import codecs, re
# from models.brownCluster import BrownCluster

class Learner():
    """docstring for Learner"""

    def __init__(self):
        self.train_file_path = path.join(path.dirname(__file__), "../data/training/")
        self.training_files  = [
            "alice_im_wunderland.txt", 
            "briefe_an_eine_freundin.txt", 
            "mann_im_mond.txt", 
            "peterchens_mondfahrt.txt"
        ]
        
    def parse_file(self, filenames):
        """loops through the given file paths and creates a clean tokeniced file from them

        - When sentence boundaries are found they are stored as a '<S/>' Symbol
        - Numbers are stores as <number>
        - one letter words become <unkown>

        the resulting string is written to tokens.txt in the same directory 
        """
        res = ""
        for filename in filenames:
            filepath = path.join(self.train_file_path, filename)

            f = codecs.open(filepath, mode="r", encoding="utf-8")
            content = f.read()
            f.close()

            # strip special characters. Note that "." is not removed yet
            content = re.sub(u'[\]\[!"“„#$%&\\\'()*+,\/:;<=>-?@\^_`{|}~-»«]', "", content)

            # find boundaries of sentences
            content = re.sub(ur"([a-z])\.\s([A-Z0-9])", r"\1 <S/> \2", content)
            content = re.sub(ur"\.$", " <S/> ", content, flags=re.MULTILINE)

            # TO DO:
            # maybe add a list of common abbrevations to remove spaces from them here
            # remove dots
            # replace numbers with <number>
            # replace one letter word with <unkown>

            words = content.split()
            res += " ".join(words)

        print len(res)
        token_filepath = path.join(self.train_file_path, "tokens.txt")
        token_file = codecs.open(token_filepath, mode="w", encoding="utf-8")
        token_file.write(res)
        token_file.close()

    def learn(self):
        self.parse_file(self.training_files)

l = Learner()
l.learn()