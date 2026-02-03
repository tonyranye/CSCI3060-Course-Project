class WITHDRAW:
    def __init__(self,curr_amount, with_amount ):
        self.CA = curr_amount
        self.with_amount = with_amount
    
    def withDraw(self):
        if(self.CA<self.with_amount):
            return "Your current amount is less than widthdraw amount"
        return self.CA-self.with_amount


w= WITHDRAW(curr_amount=10, with_amount=20)
print(w.withDraw())