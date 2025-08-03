class Transformator:

    def __init__(self):
        self.sp_numb = []

    def transform(self, nums, spnb1, spnb2):
        biggerbase = {
            '0': "0", "1": "1", '2': '2', '3': '3', '4': '4', '5': '5',
            '6': '6', '7': '7', '8': '8', '9': '9', '10': 'A', '11': 'B',
            '12': 'C', '13': 'D', '14': 'E', '15': 'F', '16': 'G', '17': 'H',
            '18': 'I', '19': 'J', '20': 'K', '21': 'L', '22': 'M', '23': 'N',
            '24': 'O', '25': 'P', '26': 'Q', '27': 'R', '28': 'S', '29':
            'T', '30': 'U', '31': 'V', '32': 'W', '33': 'X', '34': 'Y', '35': 'Z'
        }
        for i in range(len(nums)):
            self.sp_numb.append(int(str(nums[i]), spnb1[i]))
        sp_res = []
        for i in range(len(self.sp_numb)):
            res = ''
            numb = self.sp_numb[i]
            while numb > 0:
                res += biggerbase[str(numb % spnb2[i])]
                numb = numb // spnb2[i]
            sp_res.append(res[::-1])
        return sp_res

    def math_oper(self, numb1, base1, operation, numb2, base2):
        numb1 = str(int(str(numb1), base1))
        numb2 = str(int(str(numb2), base2))
        return round(eval(numb1+operation+numb2), 12) if operation == '/' else eval(numb1+operation+numb2)