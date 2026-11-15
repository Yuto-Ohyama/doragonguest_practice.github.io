def input_int(message):

    while True:

        try:
            return int(input(message))

        except ValueError:
            print("")
            print("半角数字を入力してください！")
            print("")
#半角数字じゃないとエラーメッセージが表示される。
#エラーで強制終了せずに、もう一度入力できる関数。