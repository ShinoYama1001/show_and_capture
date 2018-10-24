#encoding:UTF-8
import practice_2 #クラスをインポート

class Class(object):
    classhennsuu = 0 #クラス変数を定義　クラスで共通して使用

    def __init__(self):
        self.instancehensuu = 1 #インスタンス変数を定義

    def prpr(self):
        print(self.classhennsuu, self.instancehensuu) #どちらの変数の使用にもselfはいるらしい


def main():
    c = Class()
    c2 = practice_2.clacla() #ファイル名.クラス名でインスタンス作れた

    c.prpr()
    print(c.classhennsuu, c.instancehensuu)
    print(Class.classhennsuu) #クラス変数はクラス名.でアクセスできるらしい

    print()

    c2.pripri() #インスタンスさえ作れば普通に使える

if __name__ == "__main__":
    main()