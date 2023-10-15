import random
import time
import pickle

from xpinyin import Pinyin

from alg import DFAFilter, NaiveFilter
from utils import remove_others


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


def get_pinyin(s):
    # TODO: uv不分
    py = Pinyin()
    s_pinyin = py.get_pinyin(s, " ")
    return s_pinyin


def main(messages, user_input=False):
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


def test():
    with open('test_file.pkl', 'rb') as f:
        input_text = pickle.load(f)
    token_len = [5, 10, 1000]
    for tl in token_len:
        dfa_filter = DFAFilter(word_combs, token_len=tl)
        dfa_filter.parse(sensitive_words_with_pinyin)
        input_str = ""
        total_time = 0
        for i in range(len(input_text) // tl):
            cur_str = input_text[i * tl:(i + 1) * tl]
            input_str += cur_str
            cont_flag = False if i == 0 else True
            print("当前输入", cur_str)
            # print("当前已遍历：", input_str)
            st1 = time.time()
            detected, result = dfa_filter.filter_sw(input_str, cont_flag)
            round_time = time.time() - st1
            total_time += round_time
            print("耗时：", round_time)
            if result:
                print("发现敏感词：", detected)
                input_str = ""
            print("")


if __name__ == '__main__':
    with open('sensitive_words.pkl', 'rb') as f:
        sensitive_words = pickle.load(f)
    with open('zz_sensitive_words.pkl', 'rb') as f:
        zz_sensitive_words = pickle.load(f)
    with open('sq_sensitive_words.pkl', 'rb') as f:
        sq_sensitive_words = pickle.load(f)
    # TODO: 获取敏感词词组
    word_combs = [["天安门", "事件"], ["澳门", "博彩", "网站"], ["加拿大", "总理"], ["香港", "苹果日报"], ["新闻", "自由", "香港"]]

    sensitive_words_with_pinyin = expand_corpus(zz_sensitive_words)

    # messages = ["啊我爱学习", "明泽同志好", "澳门环境好", "有博彩网站"]
    # main(messages)
    test()
