class Ab:
    data = 'ss'

    def p(self):
        Ab.data = Ab.data + 's'
        print(Ab.data)

s = Ab()
f = Ab()
s.p()
f.p()