import sys
import os.path
from random import shuffle

class DictionaryException(Exception):
    pass
    
class Word(object):
    def __init__(self, word, translations, rec_file_path):
        self.word = word
        self.translations = translations
        self.rec_file_path = rec_file_path

class Dictionary:
    def __init__(self, dir_path):
        self.dir_path = dir_path
        self.words_file_name = 'words.txt'
        self.test_file_path = os.path.join(self.dir_path, self.words_file_name)
        self.words = []
        
    def load(self):
        with open(self.test_file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    print('Warning: {0} contains empty string'.format(self.words_file_name))
                    continue

                parts = line.split(';')
                if len(parts) < 2:
                    raise DictionaryException('Invalid words file line format - shortage of parts')
                
                word = parts[0].strip()
                translations = [t.strip() for t in parts[1:]]
                word_rec_path = self.__get_rec_path(word)
                self.words.append(Word(word, translations, word_rec_path))
                
        
    def create_test(self, create_recordings):
        self.__shuffle()
        # creates 3 files - words.txt, translations.txt and result.txt
        
        if not create_recordings:
            return
            
        # remove directory 'rec' with content if it exists
        
        # create 'rec' directory
        
        # copy files as 1.mp3, 2.mp3, ...
   
        # create files rec_words.txt and rec_result.txt
        
    def __shuffle(self):
        shuffle(self.words)
        
    def __get_rec_path(self, word):
        word_rec_path = os.path.join(self.dir_path, word + '.mp3')
        if not os.path.isfile(word_rec_path)
            return None
        return word_rec_path

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Use create_test.py DICT_DIR_PATH [rec]")
        print('For example:')
        print('\tcreate_test.py ../dict1')
        print('\tcreate_test.py ../dict1 rec')
        sys.exit()
    
    rec = False
    if len(sys.argv) >= 3:
        rec = True
        
    dict_dir_path = sys.argv[1]
    