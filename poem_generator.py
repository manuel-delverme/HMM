import random
import string


class PoemsGenerator(object):
    def __init__(self):
        self.initial_word = dict()
        self.second_word = dict()
        self.transition_probabilities = dict()
        # self.tokenize_corpora()
        self.fancy_tokenize_corpora()
        self.normalize_distributions()

    @staticmethod
    def remove_punctuation(my_string):
        return my_string.translate(str.maketrans('', '', string.punctuation))

    @staticmethod
    def possibilities(transitions, key, value):
        """
            Creates an array for all possible combinations.
            key = (the, holidays), value = [with, are, thoughts, with]
        """
        if key not in transitions:
            transitions[key] = []
        transitions[key].append(value)

    @staticmethod
    def list_to_prob_distribution(ls):
        """
        :param ls: turn the possible combinations into probabilities
        :return: value = [with, are, thoughts, with] --> {'with': 0.5, 'are': 0.25, 'thoughts': 0.25}
        """
        transitions = {}
        # l = [dict[word] for word in ls (dict.get(word, 0) +1)]
        for word in ls:
            transitions[word] = transitions.get(word, 0) + 1
        for key, value in transitions.items():
            transitions[key] = value / len(ls)
        return transitions

    def fancy_tokenize_corpora(self):
        import collections
        history = collections.deque(maxlen=2)
        skipped = []

        for line_nr, line in enumerate(open("robert_frost.txt")):
            line_formatted = line.rstrip().lower()
            line_nopunct = self.remove_punctuation(line_formatted)

            tokens = line_nopunct.split()
            if len(tokens) == 0:
                skipped.append(line_nr)
                continue

            tokens.append("END")

            first_word = tokens.pop(0)
            self.initial_word[first_word] = self.initial_word.get(first_word, 0) + 1
            history.append(first_word)

            second_word = tokens.pop(0)
            self.possibilities(self.second_word, first_word, second_word)
            history.append(second_word)

            for word in tokens:
                self.possibilities(self.transition_probabilities, tuple(history), word)
                history.append(word)

        print('Skipped loading the following lines', skipped)

    def tokenize_corpora(self):
        for line in open("robert_frost.txt"):
            line = line.rstrip().lower()
            line = self.remove_punctuation(line)
            tokens = line.split()

            # TODO: revisit this section
            first_word = tokens.pop(0)
            second_word = tokens.pop(0)

            self.initial_word[first_word] = self.initial_word.get(first_word, 0) + 1
            self.possibilities(self.second_word, first_word, second_word)

            previous_previous_word = first_word
            previous_word = second_word

            for word in tokens[:-1]:
                self.possibilities(self.transition_probabilities, (previous_previous_word, previous_word), word)

                previous_previous_word = previous_word
                previous_word = word

            last_word = tokens[-1]
            self.possibilities(self.transition_probabilities, (previous_word, last_word), "END")

    def normalize_distributions(self):
        """Normalizes distribution, turns data into prob"""

        initial_total = sum(self.initial_word.values())  # total starting words

        # prob of first word
        for key, value in self.initial_word.items():
            self.initial_word[key] = value / initial_total

        # normalize distribution of second words
        for key, value in self.second_word.items():
            self.second_word[key] = self.list_to_prob_distribution(value)

        # normalize distribution of transitions words
        for key, value in self.transition_probabilities.items():
            self.transition_probabilities[key] = self.list_to_prob_distribution(value)

        return initial_total

    def sample_word(self, transition_probabilities):
        words, probs = zip(*list(transition_probabilities.items()))
        word, = random.choices(words, probs, k=1)
        return word

    def generator(self):
        machine_poem = []

        word0 = self.sample_word(self.initial_word)
        machine_poem.append(word0)

        word1 = self.sample_word(self.second_word[word0])
        machine_poem.append(word1)

        while True:
            word2 = self.sample_word(self.transition_probabilities[(word0, word1)])
            if word2 == "END":
                break
            machine_poem.append(word2)
            word0 = word1
            word1 = word2
        return " ".join(machine_poem)


if __name__ == "__main__":
    random.seed(714)
    name = PoemsGenerator()
    print(name.generator())
