#!/usr/bin/env python3

import sys
import os.path
import random

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
        
    def create_test(self, create_recordings):
        self.load()
        self.__shuffle()

        self.__create_text_test()
        
        if not create_recordings:
            return

        self.__create_rec_test()

    # return tuple (list of max_cnt translations shuffled, word_idx)
    def get_translations(self, max_cnt=1):
        word_idx =random.randint(0, len(self.words))

        if max_cnt == -1:
            traslations_idicies = range(len(self.words[word_idx].translations)+1)
            random.shuffle(traslations_idicies)
        else:
            traslations_idicies = random.sample(range(len(self.words[word_idx].translations)+1), max_cnt)
        translations = [self.words[word_idx].translations[idx] for idx in traslations_idicies]

        return (translations, word_idx)

    def get_result(self, idx):
        return self.words[idx].word

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

    def __create_text_test(self):
        # creates 3 files - words.txt, translations.txt and result.txt
        with open('words.txt', 'w') as f:
            pass

        words = [w.word+'\n' for w in self.words]
        with open('result.txt', 'w') as f:
            f.writelines(words)

        translations = [t+'\n' for t in [';'.join(w.translations) for w in self.words]]
        with open('translations.txt', 'w') as f:
            f.writelines(translations)


    def __create_rec_test(self):
        # remove directory 'rec' with content if it exists

        # create 'rec' directory

        # copy files as 1.mp3, 2.mp3, ...

        # create files rec_words.txt and rec_result.txt
        pass
        
    def __shuffle(self):
        random.shuffle(self.words)
        
    def __get_rec_path(self, word):
        word_rec_path = os.path.join(self.dir_path, word + '.mp3')
        if not os.path.isfile(word_rec_path):
            return None
        return word_rec_path

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Welcome to interactive mode, type q for exit\n')
        print("Use create_test.py DICT_DIR_PATH [rec]")
        print('For example:')
        print('\tcreate_test.py ../dict1')
        print('\tcreate_test.py ../dict1 rec')

        print('Enter dictionary directory:')
        dict_dir = sys.stdin.readline()
        dict_dir = dict_dir.strip()
        
        dict = Dictionary(dict_dir)
        dict.load()

        while True:
            data = dict.get_translations(1)

            for t in data[0]:
                print(t)
            print('')

            answer = sys.stdin.readline()
            answer = answer.strip()
            if answer == 'q':
                sys.exit()

            result = dict.get_result(data[1])
            if answer == result:
                print('YES\n')
            else:
                print('NO, {0}\n'.format(result))

    
    rec = False
    if len(sys.argv) >= 3:
        rec = True
        
    dict_dir_path = sys.argv[1]

    dict = Dictionary(dict_dir_path)
    dict.create_test(False)

    