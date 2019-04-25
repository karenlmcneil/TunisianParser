import nltk

from preprocessing.uni2buck import transString
from parser import parse


# #**********************************************#
# #             TESTING PARSER                   #
# #**********************************************#

#def make_parse_string(top_parse):
#     parse_string = '+'.join(top_parse.asList())
#     # kludge to fix cases where I have an empty '' prefix or suffix
# #    if parse_string.startswith('+'): parse_string = parse_string[1:]
# #    if parse_string.endswith('+'): parse_string = parse_string[:-1]
#     return parse_string


def make_binary(parse):
    '''
    turn parse into string of zeros and ones showing boundaries
    ie: 'w+al+byt'  ->  '10100'
    arg is a string of morphemes separated by '+'
    returns a string of zeros and ones
    '''
    string = ''
    i=0
    while i < len(parse)-1:
        if parse[i] != '+':
            try:
                if parse[i+1] == '+':
                    string = string+'1'
                else:
                    string = string+'0'
            except:
                #if it's on the last letter and there is no parse[i+1]
                pass
        i+=1
    return string


def log_incorrect_parses(wrong_list):
    wrong_fd = nltk.FreqDist(wrong_list)
    wrong_string = ''
    for k,v in wrong_fd.items():
        wrong_string += k + '\t' + str(v) + '\n'
    outfile = open('data/incorrect_parses_log.txt','w', encoding='utf-8')
    outfile.write(wrong_string)
    outfile.close()
    return


def parse_eval(test_parse_list, gold_parse_list):
    '''
    Calculate precision and recall
    Returns recall, precision, accuracy
    '''
    recall_num, recall_denom, precision_num, precision_denom, accuracy = 0, 0, 0, 0, 0
    wrong_list = []

    for test_parse, gold_parse in zip(test_parse_list, gold_parse_list):
        if test_parse==gold_parse:
            accuracy+=1
        else:
            wrong_list.append(test_parse + " " + gold_parse)

        #turn parses into strings of zeros and ones showing boundries
        gold_str = make_binary(gold_parse)
        test_str = make_binary(test_parse)

        # compute precision and recall
        recall_denom += len([l for l in gold_str if l=='1'])
        precision_denom += len([l for l in gold_str if l=='0'])
        r_num, p_num, i = 0, 0, 0
        while i < len(test_str):
            if test_str[i]=='1' and test_str[i]==gold_str[i]:
                r_num+=1
            if test_str[i]=='0' and test_str[i]==gold_str[i]:
                p_num+=1
            i+=1
        recall_num += r_num
        precision_num += p_num
        if wrong_list:
            log_incorrect_parses(wrong_list)
    return accuracy/len(test_parse_list), precision_num/precision_denom, \
        recall_num/recall_denom


def evaluate_parser(data_length=2000):
    gold_string = transString(open('data/arabic_testing.txt','r', encoding='utf-8').read())
    gold_parses = gold_string.split()
    test_tokens = gold_string.replace('+','').split()
    test_parses = []
    for word in test_tokens[:data_length]:
        parsed_word = parse(word)[0][0]
        test_parses.append(parsed_word.replace(' ', '+'))
    accuracy, precision, recall = parse_eval(test_parses, gold_parses[:data_length])
    return accuracy, precision, recall


def evaluate_parser_stem(data_length=2000):
    gl = open('data/arabic_stem_testing.txt', 'r', encoding='utf-8').readlines()
    tl = open('data/arabic_test_string.txt', 'r', encoding='utf-8').readlines()
    log = open('data/parse_test_log.txt', 'w', encoding='utf-8')
    total_tokens = 0
    for line in gl:
        total_tokens += len(line.split())
    correct = 0
    parse_pairs = []
    for i, line in enumerate(gl):
        for j, word in enumerate(line.split()):
            test_word = tl[i].split()[j]
            parsed_word = parse(test_word)[0][0]
            parse_pairs.append([word, parsed_word])
    for correct_parse, test_parse in parse_pairs:
        log.write("%s \t %s - " % (correct_parse, test_parse))
        if correct_parse == test_parse:
            correct += 1
            log.write("right \n")
        else:
            log.write("wrong \n")
    accuracy = correct/total_tokens
    log.close()
    return accuracy
