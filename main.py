import random
import re
import time
import pickle

from xpinyin import Pinyin

from alg import DFAFilter, NaiveFilter


def expand_corpus(keywords):
      # length: n, n, 2^n
    def is_all_chinese(s):
        for char in s:
            if not '\u4e00' <= char <= '\u9fa5':
                return False
        return True

    zp_list = []
    for kw in keywords.split("\n"):
        chi_list, pin_list = [], []
        if not is_all_chinese(kw):
            continue
        for wi in kw:
            chi_list.append(wi)
            pinyin = get_pinyin(wi)
            pin_list.append(pinyin)

        combs = []
        while len(combs) < 2 ** len(kw):
            # TODO: 不用随机的形式生成
            gen_word = " ".join([random.sample([chi_list[i], pin_list[i]], 1)[0] for i in range(len(kw))])
            if gen_word not in combs:
                combs.append(gen_word)
        zp_list.extend(combs)
    return zp_list


def remove_others(message):
    msg_strip = ''.join(re.findall('[\u4e00-\u9fa5A-Za-z0-9]', message))
    return msg_strip


def get_pinyin(s):
    # TODO: uv不分
    py = Pinyin()
    s_pinyin = py.get_pinyin(s, " ")
    return s_pinyin


def main(messages, user_input=False):
    with open('sensitive_words.pkl', 'rb') as f:
        sensitive_words = pickle.load(f)
    with open('zz_sensitive_words.pkl', 'rb') as f:
        zz_sensitive_words = pickle.load(f)
    with open('sq_sensitive_words.pkl', 'rb') as f:
        sq_sensitive_words = pickle.load(f)
    # TODO: 获取敏感词词组
    word_combs = [["天安门", "事件"], ["澳门", "博彩"]]

    sensitive_words_with_pinyin = expand_corpus(zz_sensitive_words)
    dfa_filter = DFAFilter(word_combs)
    dfa_filter.parse(sensitive_words_with_pinyin)

    if user_input:
        inputs = ''
        ri = ''
        while ri != 'quit':
            ri = input("Enter: ")
            inputs += ri
            st3 = time.time()
            _, result = dfa_filter.filter_sw(inputs, cont_flag=True)
            print(result, "耗时：", time.time() - st3)
            if result:
                inputs = ''
    else:
        for i, msg in enumerate(messages):
            print("当前输入：", msg)
            st3 = time.time()
            # TODO: 正则化
            prc_msg = remove_others(msg)
            # TODO: 汉字拼音分割
            cont_flag = False if i == 0 else True
            detected, result = dfa_filter.filter_sw(msg, cont_flag)
            print(result, "耗时：", time.time() - st3)
            print("发现敏感词：", detected)


if __name__ == '__main__':
    messages = ["啊我爱学习", "明泽同志好", "澳门环境好", "有博彩网站"]
    main(messages)
