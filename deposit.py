

class DEPOSITE:
    def __init__(self, curr_money, amount_d):
        self.CM = curr_money
        self.amount_d = amount_d
    
    def depo(self):
        if(self.CM<0):
            self.CM=0
        if(self.amount_d<0):
            return self.CM
        return self.CM+self.amount_d


d = DEPOSITE(curr_money=500, amount_d=-10)
print(d.depo())