import re
import csv
import sys
import sre_yield
import string

def read_crossword_file():
    crossword_data = []
    connected_words = []
    with open(sys.argv[1],"r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            # make crosswordData list
            line = []
            line.append(int(row[0]))
            line.append(row[1])
            crossword_data.append(line)

            # make connectedWords list
            connected = []
            connected.append(line[0])
            for i in row[2:]:
                connected.append(int(i))
            connected_words.append(connected)
        crossword_data.sort()
        connected_words.sort()
        return crossword_data, connected_words

def read_regular_expressions_file():
    with open(sys.argv[2],"r") as txt_file:
        regular_expressions = txt_file.readlines()
        regular_expressions = [ex.strip() for ex in regular_expressions]
    return regular_expressions

def make_crossword(all_words):
    crossword = []
    for word in all_words:
        line = []
        for letter in word[1]:
            if letter == '.':
                line.append('')
            else:
                line.append(letter)
        crossword.append(line)
    return crossword

def find_word_to_fill(crossword):
    filled_rate = []
    for word in crossword:
        counter = 0
        for letter in word:
            if letter != '':
                counter += 1
        if counter == len(word):
            counter = 0
        filled_rate.append(counter/len(word))
    next_word = filled_rate.index(max(filled_rate))
    return next_word

def words_from_remaining_regex(reg_ex_remaining, length):
    produced_words = []
    for expression in reg_ex_remaining:
        lst = list(set(sre_yield.AllStrings(expression, max_count=5, charset=string.ascii_uppercase)))
        for word in lst:
            if len(word) == length:
                produced_words.append((word, expression))
    return produced_words

def re_match(word, reg_ex):
    matched_expression = []
    for expression in reg_ex:
        if word in sre_yield.AllStrings(expression, max_count=5, charset=string.ascii_uppercase):
           matched_expression.append(expression)
    return matched_expression

def fill_crossword(crossword, the_all_words, word_found):
    lst = crossword.copy()
    for i, letter in enumerate(the_all_words[word_found][1]):
        lst[word_found][i] = letter
    for place, wordId in enumerate(the_all_words[word_found][2]):
        word_to_fill = the_all_words[wordId]
        lst[word_to_fill[0]][the_all_words[word_found][3][place]] = the_all_words[word_found][1][place_of_connection(word_found, word_to_fill)]
    return lst

def place_of_connection(word_id, con_word):
    place = None
    for i in range(len(con_word[2])):
        if con_word[2][i] == word_id:
            place = con_word[3][i]
            break
    return place

def check_fit(word, produced_words):
    word_to_fill = word 
    words_that_fit = []
    for prod_word in produced_words:
        word_to_check = []
        for space in range(len(word_to_fill)):
            if word_to_fill[space] == '':
                word_to_check.append(prod_word[0][space])
            else:
                word_to_check.append(word_to_fill[space])
        final = ''
        if final.join(word_to_check) == prod_word[0]:
            words_that_fit.append(prod_word)
    return words_that_fit

def recursion(cw_state, regex_remaining, all_words_list):
    tmp_all_words = []
    for counter in range(len(all_words_list)):
        tmp_all_words.append([])
        tmp_all_words[counter] = all_words_list[counter][:]
    tmp_crossword_state = []
    for counter in range(len(cw_state)):
        tmp_crossword_state.append([])
        tmp_crossword_state[counter] = cw_state[counter][:]
    tmp_regex_remaining = []
    for counter in range(len(regex_remaining)):
        tmp_regex_remaining.append([])
        tmp_regex_remaining[counter] = regex_remaining[counter]
    next_word = find_word_to_fill(tmp_crossword_state)
    produced_words = words_from_remaining_regex(tmp_regex_remaining, len(tmp_all_words[next_word][1]))
    words_that_fit = check_fit(tmp_crossword_state[next_word], produced_words)
    if len(words_that_fit) == 0:
        if len(tmp_regex_remaining) == 0:
            return tmp_crossword_state
        else:
            return False
    for item in words_that_fit:
        tmp_all_words[next_word][1] = item[0]
        tmp_all_words[next_word][5] = item[1]
        tmp_all_words[next_word][4] = True
        tmp = tmp_regex_remaining.pop(tmp_regex_remaining.index(item[1]))
        crossword_states = fill_crossword(tmp_crossword_state, tmp_all_words, next_word)
        result = recursion(crossword_states, tmp_regex_remaining, tmp_all_words)
        if result is not False:
            return result
        tmp_regex_remaining.append(tmp)
    return False


crossword_data, connected_words = read_crossword_file()
regular_expressions = read_regular_expressions_file()

regex = []
for i, expression in enumerate(regular_expressions):
    regex.append(regular_expressions[i])

all_words = []
for i in range(len(crossword_data)):
    total_con_words = []
    total_places = []
    con = connected_words[i]
    for j in range(1, len(con) - 1, 2):
        total_con_words.append(con[j])
        total_places.append(con[j + 1])
    expression_used = None
    found = False
    word = [crossword_data[i][0], crossword_data[i][1], total_con_words, total_places, expression_used, found]
    all_words.append(word)

crossword_state = make_crossword(all_words)

for word in all_words:
    expression_used = None
    if '.' not in word[1]:
        expressions_id = re_match(word[1], regular_expressions)
        expression_used = expressions_id[0]
        word[4] = True
        word[5] = expression_used
        regex.pop(regex.index(expression_used))
        crossword_state = fill_crossword(crossword_state, all_words, word[0])
regex_remaining = regex
result = recursion(crossword_state, regex_remaining, all_words)

if result is not False:
    for i in range(len(result)):
        line = ''
        final_word = line.join(result[i])
        expressions_id = re_match(final_word, regular_expressions)
        expression_used = expressions_id[0]
        all_words[i][1] = final_word
        all_words[i][5] = expression_used
        all_words[i][4] = True
        print(i, all_words[i][5], all_words[i][1])
else:
    print(result)