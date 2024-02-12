import random
# this function makes an anagram if the word length >= 2
# it takes a string and returns its anagram
def anagraming(string):
    length = len(string)
    if length < 2:
        raise ValueError("The word should contain at least 2 characters")
    new = string
    while new == string:
        decreasing_string = string
        new = ""
        for x in string:
            length = len(decreasing_string)
            index = random.randint(0, length - 1)
            new += decreasing_string[index]
            decreasing_string = decreasing_string[:index] + decreasing_string[index + 1:]
    return new


