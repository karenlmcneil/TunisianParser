import nltk

from aeb_parser import parse_string


def make_binary(parse):
    """
    turn parse into string of zeros and ones showing boundaries
    for example: 'w+al+byt'  ->  '10100'
    :param parse: a string of morphemes separated by '+'
    :return: string of zeros and ones
    """
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


def calculate_segment_accuracy(gold_parse_list, test_parse_list):
    """
    Calculates accuracy, precision and recall of word segmentation.
    :param gold_parse_list: a list of correct segments, separated by spaces (['w al byt', 'altqy t'])
    :param test_parse_list: a list of parser-produced segments (['w al byt', 'al tqyt'])
    :return: 3 floats: accuracy, precision and recall
    """
    recall_num, recall_denom, precision_num, precision_denom, accuracy = 0, 0, 0, 0, 0
    wrong_list = []

    for test_parse, gold_parse in zip(test_parse_list, gold_parse_list):
        if test_parse==gold_parse:
            accuracy+=1
        else:
            wrong_list.append(test_parse + " " + gold_parse)

        #turn parses into strings of zeros and ones showing boundries
        gold_strings = make_binary(gold_parse)
        test_strings = make_binary(test_parse)

        # compute precision and recall
        recall_denom += len([l for l in gold_strings if l=='1'])
        precision_denom += len([l for l in gold_strings if l=='0'])
        r_num, p_num, i = 0, 0, 0
        for i, test_string in enumerate(test_strings):
            try:  # why am I getting an IndexError sometimes here?
                if test_string == '1' and test_string == gold_strings[i]:
                    r_num += 1
                if test_string == '0' and test_string == gold_strings[i]:
                    p_num += 1
            except IndexError: continue
        recall_num += r_num
        precision_num += p_num
        if wrong_list:
            log_incorrect_parses(wrong_list)
        try:
            recall = recall_num/recall_denom
        except ZeroDivisionError:
            recall = 0
        try:
            precision = precision_num/precision_denom
        except ZeroDivisionError:
            precision = 0
        try:
            acc = accuracy/len(test_parse_list)
        except ZeroDivisionError:
            acc = 0
    return acc, precision, recall


def evaluate_parser_segmentation(filename='data/segmentation_gold.txt'):
    """
    Evaluates results of word segmentation.
    :param filename: A txt file with arabic text with morphologic boundaries marked with '+'
    :return: Three floats, for accuracy, precision and recall. Accuracy is word-level; precision
    and recall are character level.
    """
    gold_parse_list = []
    test_parse_list = []
    gold_lines = open(filename,'r', encoding='utf-8').readlines()
    for line in gold_lines:
        for gold_token in line.split():
            gold_parse_list.append(gold_token)
            joined_token = gold_token.replace('+', '')
            test_token = '+'.join([w for w,t in parse_string(joined_token)])
            test_parse_list.append(test_token)
    accuracy, precision, recall = calculate_segment_accuracy(gold_parse_list, test_parse_list)
    return accuracy, precision, recall


def evaluate_pos_tagging(goldfile, testfile):
    """
    Evaluates the results of part of speech tagging. Word segmentation in test file and gold
    standard file must be the same.
    :param goldfile: A tsv file of the format "word \t tag \n" with the correct pos
    :param testfile: A tsv file of the format "word \t tag \n" with the pos produced by parser
    :return:
    """
    acc = 0
    acc_denom = 0
    with open(goldfile, 'r') as gf, open(testfile, 'r') as tf:
        goldlines = gf.readlines()
        testlines = tf.readlines()
        for i, line in enumerate(goldlines):
            acc_denom += 1
            gold_word, gold_tag = line.strip().split('\t')
            test_word, test_tag = testlines[i].strip().split('\t')
            if test_tag == gold_tag:
                acc += 1
    return acc / acc_denom


if __name__ == '__main__':
    # seg_acc, seg_prec, seg_rec = evaluate_parser_segmentation()
    seg_acc, seg_prec, seg_rec = evaluate_parser_segmentation()
    print("\nWord-level segmentation accuracy is {:2.2%}".format(seg_acc),
          "\nCharacter-level segmentation precision is {:2.2%}".format(seg_prec),
          "\nCharacter-level segmentation recall is {:2.2%}".format(seg_rec))
