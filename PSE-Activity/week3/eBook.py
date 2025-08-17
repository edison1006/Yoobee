class eBook:

    def __init__(self,name):
        self.name = name

    def eBook_read(self):
         with open(self.name,"r") as data:
            lines = data.readlines()
            for line in lines:
                print(line[0:])

    def eBook_write(self, content):
        with open(self.name, "a") as data:
            data.write(content + "\n")

def main():
    path = "/Users/zhangxiaoyu/Desktop/Yoobee/PSE/week3/Activity/eBook.txt"
    file = eBook(path)
    file.eBook_read()
    file.eBook_write("content")

if __name__ == "__main__":
    main()