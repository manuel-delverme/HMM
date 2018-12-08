import numpy as np
import string

initial_word = {} # prob of first word
second_word = {} # prob second word
transitions = {}

def remove_punctuation(s):
    return s.translate(str.maketrans('', '', string.punctuation))


# create array for all possible combinations
# key = (the, holidays), value = [with, are, thoughts, with]
def possibilities(dict, key, value):
    if key not in dict:
        dict[key] = []
    dict[key].append(value)

# tokenize
for line in open("robert_frost.txt"):
    tokens = remove_punctuation(line.rstrip().lower()).split()

    # revisit this section
    len_token = len(tokens)
    for i in range(len_token):
        word = tokens[i]
        if i == 0: # first word
            initial_word[word] = initial_word.get(word, 0) + 1
        else:
            t_1 = tokens[i-1] # last word and stop
            if i == len_token - 1:
                possibilities(transitions, (t_1, word), "END")
            if i == 1: # second word
                possibilities(second_word, t_1, word)
            else:
                t_2 = tokens[i-2] # others word
                possibilities(transitions, (t_2, t_1), word)

# normalize distribution, turn data into prob
initial_total = sum(initial_word.values()) # total starting words

for key, value in initial_word.items(): # prob of first word
    initial_word[key] = value / initial_total

maximum = sorted(initial_word.items(), key=lambda k: k[1], reverse=True)
# print(maximum[:10])

# turn the possible combinatons into probabilities
# value = [with, are, thoughts, with] --> {'with': 0.5, 'are': 0.25, 'thoughts': 0.25}
def possibilities_prob(ls):
    dict = {}
    # l = [dict[word] for word in ls (dict.get(word, 0) +1)]
    for word in ls:
        dict[word] = dict.get(word, 0) + 1
    for key, value in dict.items():
        dict[key] = value / len(ls)
    return dict

# normilize distribution of second words
for key, value in second_word.items():
    second_word[key] = possibilities_prob(value)

# normalize distribution of transitions words
for key, value in transitions.items():
    transitions[key] = possibilities_prob(value)


def sample_word(dict):
    prob = np.random.random()
    cumulative = 0
    for key, value in dict.items():
        cumulative += value
        if prob < cumulative:
            return key
    assert(False)

def generator():

    machine_poem = []

    word0 = sample_word(initial_word)
    machine_poem.append(word0)

    word1 = sample_word(second_word[word0])
    machine_poem.append(word1)

    while True:
        word2 = sample_word(transitions[(word0, word1)])
        if word2 == "END":
            break
        machine_poem.append(word2)
        word0 = word1
        word1 = word2
    print(" ".join(machine_poem))

if __name__=="__main__":
    for i in range(5):
        generator()
