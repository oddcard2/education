#!/usr/bin/env python3

import sys
import os
import os.path
import random
from enum import Enum


class TestType(Enum):
    translation = 1
    transcription = 2
    audio = 3

class DictionaryException(Exception):
    pass
    
class Word(object):
    def __init__(self, word, translations, transcriptions, rec_file_path, score):
        self.word = word
        self.translations = translations
        self.rec_file_path = rec_file_path
        self.transcriptions = transcriptions
        self.score = score

class Question(object):
    def __init__(self, index):
        self.help_done = False
        self.index = index

class Dictionary:
    def __init__(self, dir_path):
        self.dir_path = dir_path
        self.words_file_name = 'words.txt'
        self.test_file_path = os.path.join(self.dir_path, self.words_file_name)
        self.words = []
        self.init_score = 3
        self.test_type = TestType.translation

    def set_test_type(self, type):
        self.test_type = type

    def remove_word(self, index):
        del self.words[index]

    def clear_stat(self, index):
        self.words[index].score = self.init_score

    def decrease_score(self, index, val = 1):
        self.words[index].score -= val
        if self.words[index].score == 0:
            self.remove_word(index)

    def increase_index(self, index, val =  2):
        self.words[index].score += val

    def get_word_score(self, idx):
        if idx >= len(self.words):
            return 0
        return self.words[idx].score

    def create_test(self, create_recordings):
        self.load()
        self.__shuffle()

        self.__create_text_test()
        
        if not create_recordings:
            return

        self.__create_rec_test()

    # return tuple (list of max_cnt translations shuffled, word_idx)
    def get_translations(self, max_cnt=1):
        word_idx = random.randint(0, len(self.words)-1)

        if max_cnt == -1:
            traslations_idicies = range(len(self.words[word_idx].translations))
            random.shuffle(traslations_idicies)
        else:
            traslations_idicies = random.sample(range(len(self.words[word_idx].translations)), max_cnt)
        translations = [self.words[word_idx].translations[idx] for idx in traslations_idicies]

        return (translations, word_idx)

    def get_transcriptions(self, max_cnt=1):
        word_idx = random.randint(0, len(self.words)-1)

        if max_cnt == -1:
            transcriptions_idicies = range(len(self.words[word_idx].transcriptions))
            random.shuffle(transcriptions_idicies)
        else:
            transcriptions_idicies = random.sample(range(len(self.words[word_idx].transcriptions)), max_cnt)
        transcriptions = [self.words[word_idx].translations[idx] for idx in transcriptions_idicies]

        return (transcriptions, word_idx)

    def get_question(self, max_cnt=1):
        if len(self.words) == 0:
            return ([], -1)

        if self.test_type == TestType.translation:
            return self.get_translations(max_cnt)
        else:
            return self.get_transcriptions(max_cnt)

    def get_result(self, idx):
        return self.words[idx].word

    def __filter_words(self, only_with_transcriptions=False, only_with_audio=False):
        return [w for w in self.words if (not only_with_transcriptions or w.transcriptions) and (not only_with_audio or w.rec_file_path)]

    def get_words_count(self, only_with_transcriptions=False, only_with_audio=False):
        return sum([1 for w in self.words if (not only_with_transcriptions or w.transcriptions) and (not only_with_audio or w.rec_file_path)])

    def limit_words(self, limit, only_with_transcriptions=False, only_with_audio=False):
        words = self.__filter_words(only_with_transcriptions, only_with_audio)
        random.shuffle(words)
        if len(words) < limit:
            limit = len(words)
        self.words = words[:limit]

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
                translations = [t.strip() for t in parts[1:] if not t.startswith('/')]
                transcriptions = [t.strip() for t in parts[1:] if t.startswith('/')]
                word_rec_path = self.__get_rec_path(word)
                self.words.append(Word(word, translations, transcriptions, word_rec_path, self.init_score))

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

# Start:
# 1. enter directory path (TODO: store last directory and use it if input is empty, also output last 9 directories and use them if input is a digit)
#   number of words, transcriptions and audio recordings output
# 2. enter number of questions (all if input is empty)
# 3. see available test types (digits) and enter enter test type
# 4. enter the stat limit

# after each answer you will see the question stat and information about word elimination if it were

# Commands:
#   q - quit
#   d - delete word
#   r -repeat the question (useful for audio, but stat won't be changed)
#   c - clear stat for the question
#   h - print the help
#   ? - show the first letter and * then (the word stat won't be changed)
#   ?? - shows the first and the last letters with * in the middle

def load_last_directories(file_path):
    res = []
    try:
        with open(file_path, 'r') as f:
            for l in f:
                res.append(l.strip())
    except:
        pass
    return res

def add_last_directory(last_dirs, d, limit):
    res = last_dirs.copy()
    try:
        idx = last_dirs.index(d)
        elem = res[idx]
    except ValueError:
        elem = d
        idx = -1

    if idx != 0:
        for i in range(idx-1, -1, -1): # shifts to right up to found elem
            res[i+1] = res[i]
        if not len(res):
            res = [elem]
        else:
            res[0] = elem

    if idx == -1 and len(last_dirs) > limit and limit > 0:
        del res[-1]
    return res

def save_last_directories(file_path, last_dirs):
    dirs = [d + '\n' for d in last_dirs]
    with open(file_path, 'w') as f:
        f.writelines(dirs)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Welcome to interactive mode, type q for exit\n')
        print("Use create_test.py DICT_DIR_PATH [rec]")
        print('For example:')
        print('\tcreate_test.py ../dict1')
        print('\tcreate_test.py ../dict1 rec')

        script_dir = os.path.dirname(os.path.realpath(__file__))
        os.chdir(script_dir)

        last_dirs_file = 'last_dirs.txt'
        # cwd = os.getcwd()
        # print('Script directory: {0}, current directory = {1}'.format(script_dir, cwd))

        while True:
            last_dirs = load_last_directories(last_dirs_file)
            print('Enter dictionary directory (empty = last directory if exists, \'q\' for exit):\n')
            if len(last_dirs):
                print('Last directories:\n')
                for i, d in enumerate(last_dirs):
                    print('\t{0} [{1}]\n'.format(d, i))
            dict_dir = sys.stdin.readline().strip()

            if dict_dir == 'q':
                break
            elif dict_dir == '':
                if len(last_dirs):
                    dict_dir = last_dirs[0]
                else:
                    print('Error: empty input but no last directories, try again\n')
                    continue
            elif len(last_dirs) and dict_dir.isdigit():
                idx = int(dict_dir)
                if idx >= len(last_dirs):
                    print('Error: index is out of range [0-{0}], try again\n'.format(len(last_dirs)-1))
                    continue
                else:
                    dict_dir = last_dirs[idx]

            dict = Dictionary(dict_dir)
            try:
                dict.load()
            except Exception as e:
                print('Error during loading: {0}'.format(e))
                continue

            last_dirs = add_last_directory(last_dirs, dict_dir, 9)
            save_last_directories(last_dirs_file, last_dirs)

            # prints number of words, transcriptions and audio files
            print('LOADED: {0} words, {1} with transcriptions, {2} with audio'.format(
                dict.get_words_count(),
                dict.get_words_count(True),
                dict.get_words_count(False, True),
            ))

            print('Enter number of words\n')
            num_of_words = dict.get_words_count()
            num_of_words_str = sys.stdin.readline().strip()
            if num_of_words_str and num_of_words_str.isnumeric():
                num_of_words = int(num_of_words_str)

            print('Enter type of test\n')
            print('\t1 - translations (= empty input)\n')
            print('\t2 - transcriptions\n')

            only_with_transcriptions = False
            type = TestType.translation
            test_type = sys.stdin.readline().strip()
            if test_type == '2':
                only_with_transcriptions = True
                type = TestType.transcription

            dict.set_test_type(type)
            dict.limit_words(num_of_words, only_with_transcriptions)

            while True:
                data, idx = dict.get_question(1) # TODO: get_question

                if idx == -1:
                    print('Test is ended!\n')
                    break

                for t in data:
                    print(t)
                print('Score = {0}'.format(dict.get_word_score(idx)))

                answer = sys.stdin.readline().strip()

                hint_used = False
                if answer == 'q':
                    break
                elif answer == 'd':
                    dict.remove_word(idx)
                    continue
                elif answer == 'c':
                    dict.clear_stat(idx)
                    print('Stat cleared, enter answer:\n')
                    answer = sys.stdin.readline().strip()
                elif answer.startswith('?'):
                    hint_used = True
                    res = dict.get_result(idx)
                    res = ''.join([l if i == 0 or (len(answer)>1 and i == len(res)-1) else '*' for i, l in enumerate(res)])

                    if hint_used:
                        print('Hint: "{0}", enter your answer:\n'.format(res))
                        answer = sys.stdin.readline().strip()
                    else:
                        print('Hint is unavailable, enter your answer:\n'.format(res))

                result = dict.get_result(idx)
                if answer == result:
                    if not hint_used:
                        dict.decrease_score(idx)
                    print('RIGHT! Score = {0}\n'.format(dict.get_word_score(idx)))
                else:
                    dict.increase_index(idx, 2)
                    print('WRONG, correct = "{0}", score = {1}\n'.format(result, dict.get_word_score(idx)))

    else:
        rec = False
        if len(sys.argv) >= 3:
            rec = True

        dict_dir_path = sys.argv[1]

        dict = Dictionary(dict_dir_path)
        dict.create_test(False)

    