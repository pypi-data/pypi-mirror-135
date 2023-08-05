author = "SeongheeChoi"

class Captain:
    def Captain(self, in_par:str="SeongheeChoi") -> str:
        """Captain"""

        return "Captain - " + in_par

class Member:
    def members(self, n):
        """Members name"""
        if n == 1:
            return 'member : 정영수'
        elif n == 2:
            return 'member : 박선화'
        elif n == 3:
            return 'member : 이윤곤'
        elif n == 4:
            return 'member : 신미정'
        else:
            return '멤버 아님'

if __name__ == "__main__":
    print(author)

    print("#"*30)
    cap = Captain()

    print(cap.Captain())
    print(cap.Captain("정영수"))

    mem = Member()
    print(mem.members(1))
    print(mem.members(2))
    print(mem.members(3))
    print(mem.members(4))
    print(mem.members(5))