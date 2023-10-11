class SeparatePinyin:
    def __init__(self):
        sheng_mu = 'b,p,m,f,d,t,n,l,g,k,h,j,q,x,z,c,s,zh,ch,sh,r,y,w'.split(',')
        yun_mu = 'a,o,e,i,u,v,ai,ei,ui,ao,ou,iu,ie,ue,er,an,en,ia,in,iao,ian,un,vn,ang,eng,ing,ong'.split(',')
        extra_list = 'a,an,ang,ai,e,ei,en,er'.split(',')

        self.py_list = []
        for s in sheng_mu:
            for y in yun_mu:
                tmp = s + y
                if tmp not in self.py_list:
                    self.py_list.append(tmp)
        for z in extra_list:
            if z not in self.py_list:
                self.py_list.append(z)

        self.res_list = []

    def reset(self):
        self.res_list = []

    def separate_pinyin(self, word, py_str=''):
        word_len = len(word)
        for i in range(0, word_len + 1):
            p_list = py_str.split(',')
            if word[0:i] in self.py_list:
                if i == word_len:
                    p_list.append(word[0:i])
                    self.res_list = p_list[1:]
                else:
                    p_list.append(word[0:i])
                    self.separate_pinyin(word[i:], ','.join(p_list))


if __name__ == '__main__':
    spy = SeparatePinyin()
    spy.separate_pinyin('xijinping')
    print(spy.res_list)
    spy.reset()
    spy.separate_pinyin('xianzaine')
    print(spy.res_list)
