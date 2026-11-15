import tkinter as tk
from doraque_gui_command import Character
from doraque_gui_command import encounter

window = tk.Tk()

window.title("ドラゴンクエスト")
window.geometry("800x600")

# ==============
# キャラクター
# ==============
character1 = Character("よしひこ", "勇者", 1, 40, 5, 10, 5, 10, 10, 10, 0, 40, 5)
character = character1

# ==============
# フィールド画面
# ==============

field_frame = tk.Frame(window)
field_frame.pack(fill="both", expand=True)

# タイトル

field_label = tk.Label(
    field_frame,
    text="===== フィールド =====",
    font=("Arial", 24)
)

field_label.pack(pady=20)

# 所持金

gold_label = tk.Label(
    field_frame,
    text=f"ゴールド：{character.gold}",
    font=("Arial", 16)
)
gold_label.pack(pady=10)

# メッセージ表示欄

message_label = tk.Label(
    field_frame,
    text="ボタンを押してスタート！",
    font=("Arial", 16)
)

message_label.pack(pady=20)

# ================
# コマンド
# ================

command_frame = tk.Frame(field_frame)
command_frame.pack()

battle_frame = tk.Frame(window)

battle_label = tk.Label(
    battle_frame,
    text="===== たたかい =====",
    font=("Arial", 24)
)
battle_label.pack(pady=30)

def back_field():
    battle_frame.pack_forget()
    field_frame.pack(fill="both", expand=True)

back_button = tk.Button(
    battle_frame,
    text="フィールドへもどる",
    width=15,
    height=2,
    command=back_field
)

back_button.pack()

def bouken():
    field_frame.pack_forget()
    battle_frame.pack(fill="both", expand=True)

    message_label.config(
        text="ドラゴンクエスト"
    ) # label.config(text="新しい文章") で文章を新しく変更して出力される。

def go_inn():
    print("宿屋")

def go_weapon_shop():
    print("武器屋")

def go_armor_shop():
    print("防具屋")

def go_item_shop():
    print("よろず屋")

def go_bank():
    print("銀行")

def go_alchemy():
    print("錬金")

def go_church():
    print("教会")

def show_status():
    print(character.name)
    print(character.hp)
    print(character.mp)

def show_items():
    print("ふくろ")

def show_magic():
    print("じゅもん")

# =============
# ボタン
# =============

bouken_button = tk.Button(
    command_frame,
    text="ぼうけん",
    width=15,
    height=2,
    command=bouken
)

bouken_button.grid(row=0, column=0, padx=10, pady=10)

inn_button = tk.Button(
    command_frame,
    text="宿屋",
    width=15,
    height=2,
    command=go_inn
)

inn_button.grid(row=0, column=1, padx=10, pady=10)


weapon_button = tk.Button(
    command_frame,
    text="武器屋",
    width=15,
    height=2,
    command=go_weapon_shop
)

weapon_button.grid(row=1, column=0, padx=10, pady=10)


armor_button = tk.Button(
    command_frame,
    text="防具屋",
    width=15,
    height=2,
    command=go_armor_shop
)

armor_button.grid(row=1, column=1, padx=10, pady=10)


item_shop_button = tk.Button(
    command_frame,
    text="よろず屋",
    width=15,
    height=2,
    command=go_item_shop
)

item_shop_button.grid(row=2, column=0, padx=10, pady=10)


bank_button = tk.Button(
    command_frame,
    text="銀行",
    width=15,
    height=2,
    command=go_bank
)

bank_button.grid(row=2, column=1, padx=10, pady=10)


alchemy_button = tk.Button(
    command_frame,
    text="錬金",
    width=15,
    height=2,
    command=go_alchemy
)

alchemy_button.grid(row=3, column=0, padx=10, pady=10)


church_button = tk.Button(
    command_frame,
    text="教会",
    width=15,
    height=2,
    command=go_church
)

church_button.grid(row=3, column=1, padx=10, pady=10)


status_button = tk.Button(
    command_frame,
    text="ステータス",
    width=15,
    height=2,
    command=show_status
)

status_button.grid(row=4, column=0, padx=10, pady=10)


items_button = tk.Button(
    command_frame,
    text="ふくろ",
    width=15,
    height=2,
    command=show_items
)

items_button.grid(row=4, column=1, padx=10, pady=10)


magic_button = tk.Button(
    command_frame,
    text="じゅもん",
    width=15,
    height=2,
    command=show_magic
)

magic_button.grid(row=5, column=0, padx=10, pady=10)

window.mainloop()

