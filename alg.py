import jieba


class DFAFilter:
    def __init__(self, word_combs, token_len=5):
        self.keyword_chains = {}
        self.delimit = '\x00'
        self.word_combs = word_combs
        self.token_len = token_len
        # TODO: 或分割组合敏感词
        self.flat_wordlist = []
        for wc in self.word_combs:
            self.flat_wordlist.extend(wc)

        self.prev_level = None
        self.prev_sent = ""
        self.part_word = ""
        self.detected_words = []

    def add(self, keyword):
        if not isinstance(keyword, str):
            keyword = keyword.decode('utf-8')
        keyword = keyword.lower()
        # chars = keyword.strip()
        chars = keyword.split(" ")
        if not chars:
            return
        level = self.keyword_chains
        for i in range(len(chars)):
            if chars[i] in level:
                level = level[chars[i]]
            else:
                if not isinstance(level, dict):
                    break
                for j in range(i, len(chars)):
                    level[chars[j]] = {}
                    last_level, last_char = level, chars[j]
                    level = level[chars[j]]
                last_level[last_char] = {self.delimit: 0}
                break
        if i == len(chars) - 1:
            level[self.delimit] = 0

    def parse(self, keywords):
        for keyword in keywords:
            self.add(keyword.strip())

    def is_comb_sensitive(self):
        # 分割输入的句子
        segments = jieba.cut(self.prev_sent)
        seg_list = ' '.join(segments).split(" ")
        if not any([w in self.flat_wordlist for w in seg_list]) and len(self.prev_sent) > self.token_len:
            self.prev_sent = self.prev_sent[self.token_len:]
        return any([set(wc) < set(seg_list) for wc in self.word_combs])

    def filter_sw(self, message, cont_flag, repl="*"):
        if not isinstance(message, str):
            message = message.decode('utf-8')
        message = message.lower()
        self.prev_sent += message
        # 组合词检测
        if self.is_comb_sensitive():
            return "组合敏感词", True

        # 词库检测
        ret = []
        sen_flag = False
        start = 0

        # TODO: 自动分割中英文输入，拼音按一个character算
        while start < len(message):
            if self.prev_level is None or not cont_flag:
                level = self.keyword_chains
                candidates = ""
            else:
                level = self.prev_level
                candidates = self.part_word
            step_ins = 0
            for char in message[start:]:
                if char in level:
                    step_ins += 1
                    candidates += char
                    if self.delimit not in level[char]:
                        level = level[char]
                        self.prev_level = level
                        self.part_word = candidates
                    else:
                        ret.append(repl * step_ins)
                        start += step_ins - 1
                        sen_flag = True
                        self.prev_level = None
                        self.part_word = ""
                        self.detected_words.append(candidates)
                        break
                else:
                    ret.append(message[start])
                    break
            else:
                ret.append(message[start])
            start += 1

        return self.detected_words, sen_flag


class NaiveFilter:
    def __init__(self):
        self.keywords = set([])

    def parse(self, file):
        for keyword in file:
            self.keywords.add(keyword.strip().lower())

    def filter_sw(self, message, repl="*"):
        message = message.lower()
        sen_flag = False
        for kw in self.keywords:
            if kw in message:
                sen_flag = True
                message = message.replace(kw, repl)
        return message, sen_flag
