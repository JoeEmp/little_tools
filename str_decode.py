from urllib.parse import unquote
import os

if __name__ == "__main__":
    print('输入quit退出\n输入clear请空屏幕')
    while True:
        try:
            text = input('>')
            if text == 'quit':
                break
            elif text =='clear':
                os.system("clear")
            else:
                print('\n',unquote(text,'utf-8'))
        except Exception as e:
            print(e)