class Shifrator:
    def __init__(self, text, key):
        self.alfavit = ['e', 'u', 'Z', 'з', '9', '-', '^', 'Е', 'S', '"', 'Б', 'В', 'v', 'ю', 'М', 'q', 'P', 'j', ')', 'r', ']',
                        '|', '3', '.', 'ш', 'V', 'К', 'h', 'i', 'z', 'N', 'X', 'Л', 'д', '0', 'y', 'ч', 'ф', 'M', 'А', 'ж', '╕',
                        'Р', 'И', '?', 'У', 'Ч', '/', 'p', '4', 'n', 'w', '&', "'", 'З', 'Ь', 'э', 'a', 'I', 'я', 'Ж', 'Ы', '#',
                        '5', 'Q', '}', 'f', 'ы', 'g', 'b', 'F', 'г', 'Ф', 'м', 's', '$', '>', 'х', 'т', '<', 'Ц', 'l', 'П', '=',
                        'Т', 'Г', 'О', '!', '\t', 'н', 'ъ', 'Ш', 'ц', 'o', 'Ю', 'H', 'O', ':', 'K', 'в', 'x', 'U', 'Ё', 'к', 'с', '8', ' ',
                        '2', 'W', 'R', 'E', ',', 'Э', 'L', 'Я', 'J', 'k', 'щ', '1', 'р', '7', 'm', 'е', '6', '%', 'c', '[', 'D',
                        'Д', 'ё', '(', 'и', '@', 'й', 'Щ', 'б', 'у', 'T', 'Ъ', '{', '+', 'а', 'C', 'B', 'о', 'С', 'd', 't', '_',
                        'ь', '*', 'Й', 'Н', 'A', 'G', 'Y', '\\', 'п', 'Х', 'л', '\n']
        self.text = text
        self.key = key

    def deshifrv(self, text, key):
        result = ''
        for i, k in enumerate(text):
            ind = self.alfavit.index(k)
            ind_cur = self.alfavit.index(key[i % len(key)])
            y = self.alfavit[(ind - ind_cur) % len(self.alfavit)]
            result += y
        return result

    def shifrv(self, text, key):
        result = ''
        for i, h in enumerate(text):
            ind = self.alfavit.index(h)
            key_ind = self.alfavit.index(key[i % len(key)])
            y = self.alfavit[(ind + key_ind) % len(self.alfavit)]
            result += y
        return result

    def deshifrc(self, text, key):
        result = ''
        for k in text:
            cur = self.alfavit.index(k)
            y = self.alfavit[(cur - key) % len(self.alfavit)]
            result += y
        return result

    def shifrc(self, text, key):

        result = ''
        for h in text:
            ind = self.alfavit.index(h)
            y = self.alfavit[(ind + key) % len(self.alfavit)]
            result += y
        return result

    def opred(self, stor, tip):
        res = 'Ошибка'
        if stor == 'Дешифровать':
            if tip == 'Цезарь':
                res = self.deshifrc(self.text, int(self.key))
            if tip == 'Виженер':
                res = self.deshifrv(self.text, self.key)
        if stor == 'Шифровать':
            if tip == 'Цезарь':
                res = self.shifrc(self.text, int(self.key))
            if tip == 'Виженер':
                res = self.shifrv(self.text, self.key)
        return res
