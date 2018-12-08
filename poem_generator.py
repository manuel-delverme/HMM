import numpy as np
import string
import glob

# initial_word = {}  # prob of first word
# second_word = {}  # prob second word
# transitions = {}  # prob transitions



class poems_Generator():

    def __init__(self):
        self.initial_word = dict()
        self.second_word = dict()
        self.transitions = dict()
        self.tokenize()
        self.normalize_distributions()

    def remove_punctuation(self, my_string):
        return my_string.translate(str.maketrans('', '', string.punctuation))

    # create array for all possible combinations
    # key = (the, holidays), value = [with, are, thoughts, with]
    def possibilities(self, dict, key, value):
        if key not in dict:
            dict[key] = []
        dict[key].append(value)

    def possibilities_prob(self, ls):

        """
        :param ls: turn the possible combinatons into probabilities
        :return: value = [with, are, thoughts, with] --> {'with': 0.5, 'are': 0.25, 'thoughts': 0.25}
        """
        dict = {}
        # l = [dict[word] for word in ls (dict.get(word, 0) +1)]
        for word in ls:
            dict[word] = dict.get(word, 0) + 1
        for key, value in dict.items():
            dict[key] = value / len(ls)
        return dict



    def tokenize(self):
        """
        :return:
        """

        for line in open("robert_frost.txt"):
            tokens = self.remove_punctuation(line.rstrip().lower()).split()

            # TODO: revisit this section
            len_token = len(tokens)
            for i in range(len_token):
                word = tokens[i]
                if i == 0:  # first word
                    self.initial_word[word] = self.initial_word.get(word, 0) + 1
                else:
                    t_1 = tokens[i - 1]  # last word and stop
                    if i == len_token - 1:
                        self.possibilities(self.transitions, (t_1, word), "END")
                    if i == 1:  # second word
                        self.possibilities(self.second_word, t_1, word)
                    else:
                        t_2 = tokens[i - 2]  # others word
                        self.possibilities(self.transitions, (t_2, t_1), word)




    def normalize_distributions(self):

        """
        :return: normalize distribution, turn data into prob
        """

        initial_total = sum(self.initial_word.values())  # total starting words

        # prob of first word
        for key, value in self.initial_word.items():
            self.initial_word[key] = value / initial_total

        # normilize distribution of second words
        for key, value in self.second_word.items():
            self.second_word[key] = self.possibilities_prob(value)

        # normalize distribution of transitions words
        for key, value in self.transitions.items():
            self.transitions[key] = self.possibilities_prob(value)

        return initial_total


    def sample_word(self, dict):

        """
        :param dict:
        :return:
        """
        prob = np.random.random()
        cumulative = 0
        for key, value in dict.items():
            cumulative += value
            if prob < cumulative:
                return key
        assert False

    def generator(self):
        """
        :return:
        """
        machine_poem = []

        word0 = self.sample_word(self.initial_word)
        machine_poem.append(word0)

        word1 = self.sample_word(self.second_word[word0])
        machine_poem.append(word1)

        while True:
            word2 = self.sample_word(self.transitions[(word0, word1)])
            if word2 == "END":
                break
            machine_poem.append(word2)
            word0 = word1
            word1 = word2
        return " ".join(machine_poem)


if __name__== "__main__":
    name = poems_Generator()
    print(name.generator())


