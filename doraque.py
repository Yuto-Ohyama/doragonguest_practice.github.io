import random
from input_int import input_int
import json
import os 
from collections import Counter # カジノで使う

class Character:
    def __init__(self, name, job, level, hp, mp, power, guard, speed, intell, 
                 gold, exp, max_hp, max_mp, weapon = None, armor = None, item = None, 
                 casino_coin = 1000, chiisanamedal = 0, bank_gold = 0):
        self.name = name
        self.job = job
        self.level = level
        self.hp = hp
        self.mp = mp
        self.power = power
        self.guard = guard
        self.speed = speed
        self.intell = intell
        self.gold = gold
        self.exp = exp
        self.max_hp = max_hp
        self.max_mp = max_mp
        self.weapon = weapon # 今装備中の武器はなし
        self.armor = armor # 今装備中の防具はなし
        self.item = item
        self.casino_coin = casino_coin
        self.chiisanamedal = chiisanamedal
        self.sugoroku_ticket = 1
        self.bank_gold = bank_gold
        self.bag = [] # ふくろ
        self.defending = False #今ぼうぎょ状態ではない

    def get_power(self): # 何も装備してなければ素のちからやみのまもりを表示
        weapon_power = self.weapon.power if self.weapon else 0
        return self.power + weapon_power

    def get_guard(self):
        armor_guard = self.armor.guard if self.armor else 0
        return self.guard + armor_guard

    def show_parameter(self):
        print(f"{self.name}")
        print(f"職業：{self.job}")
        print(f"Lv：{self.level}")
        print(f"HP：{self.hp} / {self.max_hp}")
        print(f"MP：{self.mp} / {self.max_mp}")
        print(f"攻撃力：{self.get_power()}")
        print(f"守備力：{self.get_guard()}")
        print(f"ちから：{self.power}")
        print(f"みのまもり：{self.guard}")
        print(f"すばやさ：{self.speed}")
        print(f"かしこさ：{self.intell}")
        print(f"所持G：{self.gold}")
        print(f"経験値：{self.exp} / 100")
        print(f"カジノコイン：{self.casino_coin}枚")
        print(f"ちいさなメダル：{self.chiisanamedal}枚")
        print(f"銀行にあずけているゴールド：{self.bank_gold}G")
        print("")
        print("== そうび品 ==")

        if self.weapon:
            print(f"武器：{self.weapon.name} 攻撃力：+ {self.weapon.power}")
        else:
            print("武器：そうびしていない")

        if self.armor:
            print(f"防具：{self.armor.name} 守備力：+ {self.armor.guard}")
        else:
            print("防具：そうびしていない")

        print("")
        input("Enterキーでもどる")


        


    def gain_exp(self, amount_exp, amount_gold):
        self.exp += amount_exp
        self.gold += amount_gold
        print(f"{self.name}は{amount_exp}の経験値と{amount_gold}ゴールドを手に入れた！")

        while self.exp >= 100: # 今のところは次の経験値までは100固定で
            self.exp -= 100
            self.level_up()

    def level_up(self):
        self.level += 1
        self.max_hp += random.randint(2, 7)
        self.max_mp += random.randint(2, 7)
        self.power += random.randint(1, 5)
        self.guard += random.randint(1, 5)
        self.speed += random.randint(1, 5)
        self.intell += random.randint(1, 5)


        print(f"{self.name}はレベル{self.level}に上がった！")
        print(f"最大HP：{self.max_hp}")
        print(f"最大MP：{self.max_mp}")
        print(f"ちから：{self.power}")
        print(f"みのまもり：{self.guard}")
        print(f"すばやさ：{self.speed}")
        print(f"かしこさ：{self.intell}")

    def attack(self, target): #こうげきコマンド
        damage = (self.get_power() / 2) - (target.get_guard() / 4)
        damage = max(1, int(damage))
        if target.defending:
            damage = damage // 2 #ぼうぎょ中の敵へのダメージは半分になる
        target.hp -= damage

        print(f"{self.name}のこうげき！")
        print(f"{target.name}に{damage}のダメージ！")

    def defend(self): #ぼうぎょコマンド
        self.defending = True #このキャラは今ぼうぎょ中という状態
        print(f"{self.name}はぼうぎょしている！")

    # モンスターを倒した時の処理
    def monster_defeated(self, monster):
        print(f"{monster.name}を倒した！")
        self.gain_exp(monster.exp, monster.gold)

    def end_turn(self):
        self.defending = False
        # ターン経過系のものをここに入力

    def to_dict(self):
        if self.weapon:
            weapon_data = {
                "name": self.weapon.name,
                "price": self.weapon.price,
                "power": self.weapon.power,
            }
        else:
            weapon_data = None

        if self.armor:
            armor_data = {
                "name": self.armor.name,
                "price": self.armor.price,
                "guard": self.armor.guard,
            }
        else:
            armor_data = None

        if self.item:
            item_data = {
                "name": self.item.name,
                "price": self.item.price,
                "effect": self.item.effect,
            }
        else:
            item_data = None

        return {
            "name": self.name,
            "job": self.job,
            "level": self.level,
            "hp": self.hp,
            "mp": self.mp,
            "power": self.power,
            "guard": self.guard,
            "speed": self.speed,
            "intell": self.intell,
            "gold": self.gold,
            "exp": self.exp,
            "max_hp": self.max_hp,
            "max_mp": self.max_mp,
            "weapon": weapon_data,
            "armor": armor_data,
            "item": item_data,
            "casino_coin": self.casino_coin,
            "chiisanamedal": self.chiisanamedal,
            "bank_gold": self.bank_gold,
        }

    @classmethod
    def from_dict(cls, data):

        weapon_data = data.get("weapon")

        if weapon_data:
            weapon = Weapon(
                weapon_data["name"],
                weapon_data["price"],
                weapon_data["power"]
            )
        else:
            weapon = None

        armor_data = data.get("armor")

        if armor_data:
            armor = Armor(
                armor_data["name"],
                armor_data["price"],
                armor_data["guard"]
            )
        else:
            armor = None

        item_data = data.get("item")

        if item_data:
            item = Item(
                item_data["name"],
                item_data["price"],
                item_data["effect"]
            )
        else:
            item = None

        return cls(
            data["name"],
            data["job"],
            data["level"],
            data["hp"],
            data["mp"],
            data["power"],
            data["guard"],
            data["speed"],
            data["intell"],
            data["gold"],
            data["exp"],
            data["max_hp"],
            data["max_mp"],
            weapon,
            armor,
            item,
            data["casino_coin"],
            data["chiisanamedal"],
            data["bank_gold"],
        )
    def save_game(self): # セーブ
        with open("boukennosyo1.json", "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=4)

        print("")
        print("ぼうけんのしょをきろくしました！")
        print("")



#class外の処理
#フィールド
def field(character): 
    while True:
        print("")
        print("====================")
        print("      フィールド")
        print("====================")
        print("1. ぼうけんをする")
        print("2. 宿屋")
        print("3. 武器屋")
        print("4. 防具屋")
        print("5. よろず屋")
        print("6. 銀行")
        print("7. カジノ")
        print("8. 錬金")
        print("9. 教会")
        print("10. ステータス表示")
        print("11. ふくろ")
        print("12. じゅもん")
        print("0. ゲーム終了")
        print("====================")

        choice = input("コマンド：")

        if choice == "1":
            encounter(character)

        elif choice == "2":
            inn(character)

        elif choice == "3":
            weapon_shop(character)

        elif choice == "4":
            armor_shop(character)

        elif choice == "5":
            item_shop(character)

        elif choice == "6":
            bank(character)

        elif choice == "7":
            casino(character)

        elif choice == "8":
            alchemy(character)

        elif choice == "9":
            church(character)

        elif choice == "10":
            status(character)

        elif choice == "11":
            inventory(character)

        elif choice == "12":
            local_magic(character)

        elif choice == "0":
            break

        else:
            print("そのコマンドはせんたくできない！")

def encounter(character):
    if random.random() < 1:  # 30%で敵が出現
        enemies = create_enemies()
        for enemy in enemies:
            print("")
            print("====================")
            print(f"{enemy.name}があらわれた！")
            print("====================")

        while True:
            print("1. たたかう")
            print("2. いれかえ")
            print("3. さくせん")
            print("4. にげる")
            print("====================")

            choice = input("コマンド：")

            if choice == "1":
                battle(character, enemies)

                # 戦闘終了後
                if character.hp > 0:
                    return

                return

            elif choice == "2":
                print("いれかえはまだできない！")

            elif choice == "3":
                print("さくせんはまだ使えない！")

            elif choice == "4":
                print(f"{character.name}たちはにげだした！")
                return

            else:
                print("そのコマンドはせんたくできない！")

    else: # 敵とエンカウントしていない状態
        print("勇者が歩く#ここの処理は後程")

# 倒したモンスターもエンカウントで復活する
def create_enemies():
    enemy_count = random.randint(1, 3)

    enemies = []

    for _ in range(enemy_count):
        data = random.choice(monster_data)

        enemy =  Monster(
            data["name"],
            "モンスター",
            data["level"],
            data["hp"],
            data["mp"],
            data["power"],
            data["guard"],
            data["speed"],
            data["intell"],
            data["gold"],
            data["exp"],
            data["max_hp"],
            data["max_mp"]
        )

        enemies.append(enemy)

    return enemies


# playerのターン処理
def player_turn(character, enemies, defeated_enemies): #classの外に出す

    print("")
    print("===== ターン開始 =====")
    print(f"{character.name}")
    print(f"職業：{character.job}")
    print(f"HP：{character.hp} / {character.max_hp}")
    print(f"MP：{character.mp} / {character.max_mp}")
    print("")

    while True:
        choice2 = input("1. こうげき\n2. ぼうぎょ\n3. じゅもん\n4. とくぎ\nコマンド：")

        if choice2 == "1":

            # 攻撃する敵を選ぶ
            while True:
                print("")
                print("===== こうげき =====")

                for i, enemy in enumerate(enemies, 1):
                    print(f"{i}. {enemy. name}")

                print("0. もどる")

                target_choice = input("コマンド：") # 誰をこうげきするか

                if target_choice == "0":
                    break

                if not target_choice.isdigit():
                    print("そのコマンドはせんたくできない！")
                    continue

                target_index = int(target_choice) - 1

                if target_index < 0 or target_index >= len(enemies):
                    print("そのコマンドはせんたくできない！")
                    continue

                target = enemies[target_index]

                character.attack(target)
                # 攻撃後にたおしたか確認
    
                if target.hp > 0:
                    enemy_turn(character, enemies)

                elif target.hp <= 0:
                    print(f"{target.name}をたおした！")

                    defeated_enemies.append(target)
                    enemies.remove(target)

                    return defeated_enemies # 倒した敵をかえす

                break


        elif choice2 == "2":
            character.defend()
            break

        elif choice2 == "3":
            if magic_command(character, enemies, defeated_enemies):
                break

        elif choice2 == "4":
            print("まだとくぎをおぼえていない！")
            break

        else:
            print("そのコマンドはせんたくできない！")

    return defeated_enemies

# enemyのターン処理
def enemy_turn(character, enemies): #classの外に出す
    for enemy in enemies:
        if character.hp <= 0:
            break

        if enemy.hp > 0:
            enemy.attack(character)

# battleのターン進行処理
def battle_turn(character, enemies, defeated_enemies):

    if character.speed >= max(enemy.speed for enemy in enemies):
                #勇者が先
        player_turn(character, enemies, defeated_enemies)
                #敵が生きていたら反撃
        if character.hp > 0 and len(enemies) > 0:
            enemy_turn(character, enemies)
    
        return defeated_enemies

    else:
                #敵が先
        enemy_turn(character, enemies)
                #勇者が生きていたら反撃
        if character.hp > 0 and len(enemies) > 0:
            player_turn(character, enemies, defeated_enemies)
            return defeated_enemies

        return defeated_enemies

#戦闘全体の処理
def battle(character, enemies): 

    total_exp = 0
    total_gold = 0
    defeated_enemies = []

    while character.hp > 0 and len(enemies) > 0:

        battle_turn(character, enemies, defeated_enemies)

        for enemy in defeated_enemies:
            total_exp += enemy.exp
            total_gold += enemy.gold

        # 敵を全員倒した
        if len(enemies) == 0:
            print("まもののむれをたおした！")

            character.gain_exp(total_exp, total_gold) # まとめて経験値とゴールドが入る

            break

        # 味方が倒れた
        if character.hp <= 0:
            print(f"{character.name}は力尽きた！")
            break

        #ターン終了
        character.end_turn() #ターン終了、ぼうぎょ解除

        for enemy in enemies:
            enemy.end_turn()
        
        

# じゅもん処理
def magic_command(character, enemies, defeated_enemies):
    
    magics = [magic1, magic2, magic3, magic4, magic5, magic6, magic7, magic8]
    print("")
    print("== じゅもん ==")

    while True:
        choice3 = input("1. メラ\n2. ホイミ\n3. ギラ\n4. ヒャド\n5. イオナズン\n6. ベホイミ\n"
                        "7. ギガデイン\n8. メラゾーマ.\n0. もどる\nコマンド：")

        if choice3 == "0":
            return False # Falseならターンを経過せずに最初の選択画面にもどる

        if choice3 not in ["0", "1", "2", "3", "4", "5", "6", "7", "8"]:
            print("そのコマンドはせんたくできない！")
            continue # continueならこのコードをスキップして最初に戻る

        magic = magics[int(choice3) - 1] # 1なら0,2なら1が対応するように数字を合わせる

        if character.mp < magic.mp_cost:
            print(f"{character.name}は{magic.name}をとなえようとした！")
            print("しかしMPがたりない！")
            continue

        if magic.range == "mono_enemy": # じゅもんの対象範囲 単体
            target = select_enemy(enemies)
            character.mp -= magic.mp_cost

            if target is None:
                continue

            magic.magic_effect(character, target)

            if target.hp <= 0:
                print(f"{target.name}をたおした！")
                defeated_enemies.append(target)
                enemies.remove(target)

            return True

        elif magic.range == "all_enemy": # じゅもんの対象　全体

            targets = enemies[:]

            for target in targets:
                magic.magic_effect(character, target)

                if target.hp <= 0:
                    print(f"{target.name}をたおした！")

                    defeated_enemies.append(target)

                    enemies.remove(target)

            character.mp -= magic.mp_cost

            return True


        #elif magic.range == "mono_ally": # 味方単体
        #    target = select_ally(characters)

        #elif magic.range == "all_ally": # 味方全体
        #    targets = characters

        #elif magic.range == "self": # 自分自身
        #    targets = [character]


        # 回復じゅもんなら見方を対象にする
        elif magic.category == "heel":

            targets = [character]
            character.mp -= magic.mp_cost

        else:
            print("このじゅもんの対象範囲が設定されていません！")
            continue

        character.mp -= magic.mp_cost

        print(f"{character.name}は{magic.name}のじゅもんをとなえた！")

        

        for target in targets:
            magic.magic_effect(character, target)

            if target.hp <= 0:
                print(f"{target.name}をたおした！")

                defeated_enemies.append(target)
                enemies.remove(target)
              

        return defeated_enemies

# こうげき範囲設定
def select_enemy(enemies):
    print("")
    print("===== たいしょう =====")

    for i, enemy in enumerate(enemies, 1):
        print(f"{i}. {enemy.name}")

    print("0. もどる")

    choice = input("コマンド：")

    if choice == "0":
        return None

    if choice not in [str(i) for i in range(1, len(enemies) + 1)]:
        print("そのコマンドはせんたくできない！")
        return None

    return enemies[int(choice) - 1]

# 宿屋
def inn(character):
    print("宿屋：一晩20ゴールドになります。")

    if character.gold < 20:
        print("宿屋：ざんねんですがお金がたりないようです…")
        print("宿屋：またのおこしをお待ちしております！")
        return False

    character.gold -= 20
    character.hp = character.max_hp
    character.mp = character.max_mp

    print("宿屋：おはようございます。")
    print("宿屋：ゆうべはおたのしみでしたね。")
    print("宿屋：またのおこしをお待ちしております！")

    return True

# 武器屋
def weapon_shop(character):

    weapons = [weapon1, weapon2, weapon3, weapon4, weapon5]

    while True:
        print("")
        print("====================")
        print("       武器屋")
        print("====================")

        for i, weapon in enumerate(weapons, 1):
            print(f"{i}. {weapon.name}　{weapon.price}G　攻撃力+{weapon.power}")

        print("0. 店を出る")
        print("====================")
        print("武器屋：ここは武器屋だ。どの武器がほしいんだ？")
        print(f"所持G：{character.gold}")

        choice = input("コマンド：")

        if choice == "0":
            print("武器屋：またきなよ。")
            break

        if choice not in ["1", "2", "3", "4", "5"]:
            print("そのコマンドはせんたくできない！")
            continue

        weapon = weapons[int(choice) - 1]

        print("")
        print(f"武器屋：{weapon.name}かい？")
        print(f"{weapon.price}Gになるが買うのかい？")
        print(f"現在の所持金：{character.gold}G")

        buy = input("1. はい \n2. いいえ：")

        if buy == "1":

            if character.gold < weapon.price:
                print("武器屋：そいつを買うにはお金がたりないようだぞ")
                continue

            # お金を払う
            character.gold -= weapon.price

            print(f"武器屋：ほらよ。")
            print(f"{character.name}は{weapon.name}を買った！")
            print(f"残りの所持金：{character.gold}G")

            # 装備するか確認
            equip = input("武器屋：そうびするかい？\n1. はい\n2. いいえ：")

            if equip == "1":

                if character.weapon:
                    print(f"{character.name}は{character.weapon.name}をはずした！")

                character.weapon = weapon

                print(f"{character.name}は{weapon.name}をそうびした！")

            elif equip == "2":

                character.bag.append(weapon)

                print(f"武器屋：{weapon.name}はふくろに入れとくよ。")
                
            else:
                print("そのコマンドはせんたくできない！")
                continue


# 防具屋
def armor_shop(character):

    armors = [armor1, armor2, armor3, armor4, armor5, armor6]

    while True:
        print("")
        print("====================")
        print("       防具屋")
        print("====================")

        for i, armor in enumerate(armors, 1):
            print(f"{i}. {armor.name}　{armor.price}G　防御力+{armor.guard}")

        print("0. 店を出る")
        print("====================")
        print("防具屋：ここは防具屋です。どの防具にいたしますか？")
        print(f"所持G：{character.gold}")

        choice = input("コマンド：")

        if choice == "0":
            print("防具屋：今後ともごひいきに！")
            break

        if choice not in ["1", "2", "3", "4", "5", "6"]:
            print("そのコマンドはせんたくできない！")
            continue

        armor = armors[int(choice) - 1]

        print("")
        print(f"防具屋：{armor.name}ですね？")
        print(f"{armor.price}Gになります。")
        print(f"現在の所持金：{character.gold}G")

        buy = input("1. はい \n2. いいえ：")

        if buy == "1":

            if character.gold < armor.price:
                print("防具屋：申し訳ありません。お金が足りないようです…")
                continue

            # お金を払う
            character.gold -= armor.price

            print(f"防具屋：どうぞ。")
            print(f"{character.name}は{armor.name}を買った！")
            print(f"残りの所持金：{character.gold}G")

            # 装備するか確認
            equip = input("防具屋：そうびいたしますか？\n1. はい\n2. いいえ：")

            if equip == "1":

                if character.armor:
                    print(f"{character.name}は{character.armor.name}をはずした！")

                character.armor = armor

                print(f"{character.name}は{armor.name}をそうびした！")

            elif equip == "2":

                character.bag.append(armor)

                print(f"防具屋：{armor.name}はふくろに入れておきますね。")
                
            else:
                print("そのコマンドはせんたくできない！")
                continue

# よろず屋
def item_shop(character):
    items = [item1, item2, item3, item4]

    while True:
        print("")
        print("====================")
        print("       よろず屋")
        print("====================")

        for i, item in enumerate(items, 1):
            print(f"{i}. {item.name}　{item.price}G　効果：{item.expo()}")

        print("0. 店を出る")
        print("====================")
        print("よろず屋：ここはよろず屋です。なににいたしますか？")
        print(f"所持G：{character.gold}")

        choice = input("コマンド：")

        if choice == "0":
            print("よろず屋：今後ともごひいきに！")
            break

        if choice not in ["1", "2", "3", "4"]:
            print("そのコマンドはせんたくできない！")
            continue

        item = items[int(choice) - 1]

        print("")
        print(f"よろず屋：{item.name}ですね？")
        print(f"{item.price}Gになります。")
        print(f"現在の所持金：{character.gold}G")

        buy = input("1. はい \n2. いいえ：")

        if buy == "1":

            if character.gold < item.price:
                print("よろず屋：申し訳ありません。お金が足りないようです…")
                continue

            # お金を払う
            character.gold -= item.price
            character.bag.append(item)
            print(f"よろず屋：どうぞ。")
            print(f"{character.name}は{item.name}を買った！")
            print(f"残りの所持金：{character.gold}G")
                
        else:
            print("そのコマンドはせんたくできない！")
            continue

# 銀行
def bank(character):

    while True:

        print("")
        print("====================")
        print("        銀行")
        print("====================")
        print(f"所持ゴールド：{character.gold}G")
        print(f"預金ゴールド：{character.bank_gold}G")
        print("")
        print("*：信用と信頼のゴールド銀行にようこそ！")
        print("*：手数料などは一切かかりません。1000G単位で預けられます。")
        print(f"*：{character.name}様からは{character.bank_gold}Gお預かりしています。")
        print("")
        print("1. 預ける")
        print("2. 引き出す")
        print("0. 銀行を出る")
        print("====================")

        choice = input("コマンド：")

        # 銀行を出る
        if choice == "0":
            print("*：おやめになるのですね。またのご利用お待ちしております。")
            break

        # 預ける
        elif choice == "1":

            while True:

                print("")
                print(f"所持ゴールド：{character.gold}G")
                print("*：いくらお預けいたしますか？")
                print("")
                print("0. もどる")
                print("")

                amount = input("預けるゴールド：")

                if amount == "0":
                    print("")
                    print("*：おやめになるのですね。")
                    break

                if not amount.isdigit():
                    print("数字を入力してください。")
                    continue

                amount = int(amount)

                if amount % 1000 != 0:
                    print("1000G単位で入力してください。")
                    continue

                if amount <= 0:
                    print("1,000G以上を入力してください。")
                    continue

                if amount > character.gold:
                    print("所持ゴールドがたりません！")
                    continue

                character.gold -= amount
                character.bank_gold += amount

                print(f"{amount}Gお預かりいたします。")
                print(f"預金ゴールド：{character.bank_gold}G")

                break

        # 引き出す
        elif choice == "2":

            while True:

                print("")
                print(f"預金ゴールド：{character.bank_gold}G")
                print("*：いくらお引き出しいたしますか？")
                print("")
                print("0. もどる")
                print("")

                amount = input("引き出すゴールド：")

                if amount == "0":
                    break

                if not amount.isdigit():
                    print("数字を入力してください。")
                    continue

                amount = int(amount)

                if amount % 1000 != 0:
                    print("1000G単位で入力してください。")
                    continue

                if amount <= 0:
                    print("1,000G以上を入力してください。")
                    continue

                if amount > character.bank_gold:
                    print("預金ゴールドがたりません！")
                    continue

                character.bank_gold -= amount
                character.gold += amount

                print(f"{amount}Gを引き出しました。")
                print(f"所持ゴールド：{character.gold}G")

                break

        else:
            print("そのコマンドはせんたくできない！")

# カジノ景品交換所
def casino(character):
    while True:
        print("")
        print("==================")
        print("        カジノ")
        print("==================")
        print(f"所持コイン：{character.casino_coin}枚")
        print("")
        print("1. スロット")
        print("2. ポーカー")
        print("3. すごろく")
        print("4. 景品交換所")
        print("5. カジノコイン購入所")
        print("0. カジノを出る")
        print("=================")

        choice = input("コマンド：")

        if choice == "1":

            while True:
                print("")
                print("===== スロット =====")
                print("1. 10コインスロットで遊ぶ")
                print("2. 100コインスロットで遊ぶ")
                print("3. 10000コインスロットで遊ぶ")
                print("0. もどる")

                choice2 = input("コマンド：")

                if choice2 == "1":
                    slot_machine(character, 10)

                elif choice2 == "2":
                    slot_machine(character, 100)

                elif choice2 == "3":
                    slot_machine(character, 10000)

                elif choice2 == "0":
                    break

                else:
                    print("そのコマンドはせんたくできない！")

        elif choice == "2":
            poker(character)

        elif choice == "3":
            sugoroku(character)

        elif choice == "4":
            casino_prize_shop(character)
            print("まだもうちょっと調整中")

        elif choice == "5":
            casino_coin_shop(character)

        elif choice == "0":
            print("カジノを出ました。")
            break

        else:
            print("そのコマンドはせんたくできない！")

# スロット
def slot_machine(character, bet):

        # 倍率
    payout = {
        "7": {
            3: 100,
            4: 1000,
            5: 10000
        },
        "BAR": {
            3: 20,
            4: 200,
            5: 2000
        },
        "スイカ": {
            3: 10,
            4: 100,
            5: 1000
        },
        "ベル": {
            3: 8,
            4: 50,
            5: 200
        },
        "PLUM": {
            3: 5,
            4: 20,
            5: 100
        },
        "チェリー": {
            3: 3,
            4: 6,
            5: 20
        }
    }

        # 絵柄と出現率
    symbols = [
        ("チェリー", 30),
        ("PLUM", 25),
        ("ベル", 18),
        ("スイカ", 15),
        ("BAR", 7),
        ("7", 5)
    ]

        # symbolsの絵柄と出現率をランダムに選ぶ関数
    def spin_slot():
        names = [symbol[0] for symbol in symbols]
        weights = [symbol[1] for symbol in symbols]

        return random.choices(names, weights=weights, k=1)[0]

    while True:
        print("")
        print(f"===== {bet}コインスロット =====")
        print(f"所持コイン：{character.casino_coin}枚")
        print("")
        print(f"1回{bet}コイン")
        print("1. スタート")
        print("0. やめる")

        choice = input("コマンド：")

        if choice == "0":
            break

        if choice != "1":
            print("そのコマンドはせんたくできない！")
            continue

        if character.casino_coin < bet:
            print("コインがたりない！")
            continue

        # 掛け金
        character.casino_coin -= bet

        # スロット
        slot1 = spin_slot()
        slot2 = spin_slot()
        slot3 = spin_slot()
        slot4 = spin_slot()
        slot5 = spin_slot()

        slots = [slot1, slot2, slot3, slot4, slot5]

        print("")
        print(f"[ {slot1} ][ {slot2} ][ {slot3} ][ {slot4} ][ {slot5} ]")
        print("")

        # 一番長く連続している絵柄を調べる
        symbol, count = get_longest_match(slots)

        # 3個以上連続ならあたり
        if count >= 3:
            multiplier = payout[symbol][count]
            winnings = bet * multiplier

            character.casino_coin += winnings

            print(f"{symbol}が{count}個そろった！")
            print(f"{winnings}コイン獲得！")
        else:
            print("ざんねん……")
            

def get_longest_match(slots):
    longest_symbol = None
    longest_count = 0

    current_symbol = slots[0]
    current_count = 1

    for slot in slots[1:]:
        if slot == current_symbol:
            current_count += 1
        else:
            if current_count > longest_count:
                longest_symbol = current_symbol
                longest_count = current_count

            current_symbol = slot
            current_count = 1

    # 最後の連続も確認
    if current_count > longest_count:
        longest_symbol = current_symbol
        longest_count = current_count

    return longest_symbol, longest_count

# コイン購入   
def casino_coin_shop(character):
    rate = 20 # 1コイン = 20G

    while True:
        print("")
        print("====================")
        print(" カジノコイン購入所")
        print("====================")

        print("0. 店を出る")
        print("")
        print("*：ここはカジノコイン購入所です。お持ちのGをコインに交換できます。")
        print(f"*：カジノコイン1枚につき{rate}Gになりますが何枚交換されますか？")
        print(f"所持G：{character.gold}")
        print(f"所持コイン：{character.casino_coin}枚")
        print("")
        print("0. もどる")
        print("")

        choice = input("交換枚数：")

        if choice == "0":
            print("*：おやめになるのですね。またのおこしをお待ちしております。")
            break

        if not choice.isdigit():
            print("数字を入力してください。")
            continue

        coin_amount = int(choice)

        if coin_amount <= 0:
            print("1枚以上を入力してください。")
            continue

        required_gold = coin_amount * rate

        if character.gold < required_gold:
            print("ゴールドがたりません！")
            print(f"{coin_amount}枚には{required_gold}G必要です。")
            continue

        character.gold -= required_gold

        character.casino_coin += coin_amount

        print("")
        print(f"*：{coin_amount}枚ですね？")
        print(f"{required_gold}Gになります。")
        print(f"現在の所持金：{character.gold}G")
        print(f"所持コイン：{character.casino_coin}枚")
            
# 商品交換所
def casino_prize_shop(character):

    prizes = [
        ("キラーピアス", 10000),
        ("はやぶさのけん", 20000),
        ("メタルキングのけん", 50000),
        ("ドラゴンメイル", 5000),
        ("プラチナメイル", 10000),
        ("メタルキングよろい", 50000),
        ("せかいじゅのしずく", 10000)
    ]

    while True:
        print("")
        print("====================")
        print("  カジノ景品交換所")
        print("====================")
        print(f"所持コイン：{character.casino_coin}枚")
        print("")
        print("*：ここはカジノ景品交換所です。お持ちのコインを景品と交換できます。")
        print(f"*：{character.name}様は現在{character.casino_coin}枚コインをお持ちのようですが、何と交換されますか？")
        print("まだβテスト版ですよん")
        print("")

        for i, (name, price) in enumerate(prizes, 1):
            print(f"{i}. {name}　{price}コイン")

        print("0. 店を出る")
        print("====================")

        choice = input("コマンド：")

        if choice == "0":
            print("*：おやめになるのですね。またのおこしをお待ちしております。")
            break

        if not choice.isdigit():
            print("そのコマンドはせんたくできない！")
            continue

        index = int(choice) - 1

        if index < 0 or index >= len(prizes):
            print("そのコマンドはせんたくできない！")
            continue

        prize_name, prize_price = prizes[index]

        print("")
        print(f"{prize_name}ですね？")
        print(f"{prize_price}コインになります。")
        print(f"所持コイン：{character.casino_coin}枚")

        buy = input("1. はい\n2. いいえ\nコマンド：")

        if buy == "1":

            if character.casino_coin < prize_price:
                print("ざんねんですがコインがたりないようです。")
                continue

            character.casino_coin -= prize_price
            #character.bag.append(prize)

            print("")
            print(f"{prize_name}を手に入れた！")
            print(f"残りのコイン：{character.casino_coin}枚")

        elif buy == "2":
            continue

        else:
            print("そのコマンドはせんたくできない！")


# ポーカー
def create_deck(): # 52枚のトランプ作成

    suits = ["♠", "❤", "♦", "♣"]
    ranks = [
        "2", "3", "4", "5", "6" ,"7", "8", "9", "10",
        "J", "Q", "K", "A"
    ]

    deck = []

    for suit in suits:
        for rank in ranks:
            deck.append((suit, rank))

    return deck

# 役判定
def judge_hand(hand): 

    ranks = [rank for suit, rank in hand]

    counter = Counter(ranks)

    counts = sorted(counter.values(), reverse=True)

    # フォーカード
    if counts == [4, 1]:
        return "フォーカード", 30

    # フルハウス
    if counts == [3, 2]:
        return "フルハウス", 15

    # スリーカード
    if counts == [3, 1, 1]:
        return "スリーカード", 4

    # ツーペア
    if counts == [2, 2, 1]:
        return "ツーペア", 2

    # ワンペア
    if counts == [2, 1, 1, 1]:
        return "ワンペア", 1

    return "ハイカード", 0

# ストレート
def is_straight(hand): 

    rank_values = {
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "10": 10,
        "J": 11,
        "Q": 12,
        "K": 13,
        "A": 14
    }

    values = sorted(
        rank_values[rank]
        for suit, rank in hand
    )

    # A,2,3,4,5
    if values == [2, 3, 4, 5, 14]:
        return True

    return all(
        values[i] + 1 == values[i + 1]
        for i in range(4)
    )

# フラッシュ
def is_flush(hand):

    suits = [suit for suit, rank in hand]

    return len(set(suits)) == 1

# ポーカー本体
def poker(character):

    poker_payout = {
        "ロイヤルストレート": 200,
        "ストレートフラッシュ": 100,
        "フォーカード": 30,
        "フルハウス": 15,
        "フラッシュ": 10,
        "ストレート": 8,
        "スリーカード": 4,
        "ツーペア": 2,
        "ワンペア": 1,
        "ハイカード": 0
        }

    bet = 10

    while True:

        print("")
        print("===== ポーカー =====")
        print("まだβテスト版ですよん")
        print(f"所持コイン：{character.casino_coin}枚")
        print(f"1回{bet}コイン")
        print("1. ポーカーをする")
        print("2. 役の説明を見る")
        print("0. やめる")
        print("===================")

        choice = input("コマンド：")

        # やめる
        if choice == "0":
            break

        # 役の説明を見る
        elif choice == "2":
            print("")
            print("==============================")
            print("        ポーカーの役")
            print("==============================")

            for name, multiplier in poker_payout.items():
                print(f"{name:<20} {multiplier}倍")

            print("==============================")

            input("Enterキーで戻る")

        # ポーカーをする
        elif choice == "1":

            if character.casino_coin < bet:
                print("コインがたりない！")
                continue

            character.casino_coin -= bet

            deck = create_deck()
            random.shuffle(deck)

            hand = deck[:5]

            print("")
            print("あなたのカード")

            for i, (suit, rank) in enumerate(hand, 1):
                print(f"{i}. [{suit}{rank}]")

            print("")

            # ここでカード交換処理を後から追加

            hand_name, multiplier = judge_hand(hand)

            print("")
            print(f"役：{hand_name}")

            winnings = bet * multiplier

            if winnings > 0:
                character.casino_coin += winnings
                print(f"{winnings}コイン獲得！")
            else:
                print("ざんねん……")

        # その他
        else:
            print("そのコマンドはせんたくできない！")

# すごろく
def sugoroku(character):

    if character.sugoroku_ticket <= 0:
        print("すごろく券を持っていない！")
        return

    print("")
    print("====================")
    print("      すごろく")
    print("まだβテスト版ですよん")
    print("====================")
    print(f"すごろく券：{character.sugoroku_ticket}枚")
    print("")
    print("すごろく券を1枚使って、すごろくを始めますか？")
    print("1. はい")
    print("0. いいえ")

    choice = input("コマンド： ")

    if choice == "0":
        return

    if choice != "1":
        print("そのコマンドはせんたくできない！")
        return

    # すごろく券を1枚消費
    character.sugoroku_ticket -= 1

    # ここからすごろく本体
    sugoroku_game(character)

# すごろく関数
def sugoroku_game(character):

    position = 0
    goal = 40
    dice_count = 0
    max_dice_count = 10
    reward = 10000

    while position < goal and dice_count < max_dice_count:

        print("")
        print("====================")
        print(f"現在位置：{position} / {goal}")
        print(f"残り回数：{max_dice_count - dice_count}回")
        print("====================")
        print("1. サイコロを振る")
        print("0. やめる")

        choice = input("コマンド：")

        if choice == "0":
            print("すごろくを中断した！")
            return

        if choice != "1":
            print("そのコマンドはせんたくできない！")
            continue

        # サイコロを振った回数を増やす
        dice_count += 1

        dice = random.randint(1, 6)

        print(f"サイコロの目は{dice}！")

        position += dice
        print(f"{dice}マス進んだ！")

        if position >= goal:
            position = goal
            print("ゴール！！")
            print("すごろくをクリアした！")
            print(f"{character.name}はカジノコインを{reward}枚獲得した！")

            character.casino_coin += reward

            return

    # 10回振ってもゴールできなかった
    if position < goal:
        print("")
        print("====================")
        print("     ゲームオーバー")
        print("====================")
        print("*：またのご利用お待ちしております。")        

        

# 錬金釜
def alchemy(character):
    print("")
    print("===== 錬金 =====")
    print("まだ錬金はできません。")

# 教会
def church(character):
    print("")
    print("===== 教会 =====")
    print("1. おいのりをする")
    print("2. おつげをきく")
    print("3. どくのちりょう")
    print("4. いきかえらせる")
    print("5. のろいをとく")
    print("0. もどる")

    choice_church = input("コマンド：")

    if choice_church == "1":
        character.save_game()

# ステータス表示
def status(character):
    print("")
    print("==== ステータス ====")
    character.show_parameter()
    
# ふくろ、そうび品
def inventory(character):
    print("")
    print("===== ふくろ =====")
    while True:
        for i, item in enumerate(character.bag, 1):
            print(f"{i}. {item.name}")

        print("0. もどる")

        choice = input("コマンド：")
        if choice == "0":
            break
        if choice not in ["1", "2", "3", "4", "5", "6", "7", "8"]:
            print("そのコマンドはせんたくできない！") #8個まで
            continue
    
        item = character.bag[int(choice) - 1]

        if item.category == "weapon":
            if character.weapon:
                character.bag.append(character.weapon) # 武器があるなら、ふくろにそうびしていた武器を追加
            character.weapon = item # item(weapon)新しい武器をそうび
            print("")
            print(f"{item.name}をそうびした！")
            print("")
            character.bag.remove(item) # ふくろからそうびした新しい武器を削除

        elif item.category == "armor":
            if character.armor:
                character.bag.append(character.armor)
            character.armor = item
            print("")
            print(f"{item.name}をそうびした！")
            print("")
            character.bag.remove(item)

        elif item.category == "item":
            print("")
            choice2 = input("1. つかう \n2. すてる \n3. インパス \n0. もどる \nコマンド：")
            if choice2 == "0":
                break
            if choice2 not in ["1", "2", "3"]:
                print("そのコマンドはせんたくできない！")
                continue
            if choice2 == "1":
                if item.use(character):
                    character.bag.remove(item)
                print("")
                print(f"{character.hp} / {character.max_hp}")
                print("")
            elif choice2 == "2":
                character.bag.remove(item)
                print("")
                print(f"{item.name}をすてました！")
                print("")
            elif choice2 == "3":
                print("")
                print(item.expo())
                print("")


# 移動中じゅもん
def local_magic(character):
    magics = [magic2, magic6]
    print("")
    print(f"{character.name}")
    print(f"職業：{character.job}")
    print(f"HP：{character.hp} / {character.max_hp}")
    print(f"MP：{character.mp} / {character.max_mp}")
    print("")
    print("== じゅもん ==")

    while True:
        choice3 = input("1. ホイミ\n2. ベホイミ\n0. もどる\nコマンド：")

        if choice3 == "0":
            return False # Falseならターンを経過せずに最初の選択画面にもどる

        if choice3 not in ["0", "1", "2"]:
            print("そのコマンドはせんたくできない！")
            continue # continueならこのコードをスキップして最初に戻る

        magic = magics[int(choice3) - 1] # 1なら0,2なら1が対応するように数字を合わせる

        if character.mp < magic.mp_cost:
            print(f"{character.name}は{magic.name}をとなえようとした！")
            print("しかしMPがたりない！")
            continue

        #elif magic.range == "mono_ally": # 味方単体
        #    target = select_ally(characters)

        #elif magic.range == "all_ally": # 味方全体
        #    targets = characters

        #elif magic.range == "self": # 自分自身
        #    targets = [character]


        # 回復じゅもんなら見方を対象にする
        if magic.category == "heel":

            targets = [character]
            character.mp -= magic.mp_cost

        else:
            print("このじゅもんの対象範囲が設定されていません！")
            continue

        print(f"{character.name}は{magic.name}のじゅもんをとなえた！")

        for target in targets:
            magic.magic_effect(character, target)
              
        return 

class Monster(Character):
    def __init__(self, name, job, level, hp, mp, power, guard, speed, intell, gold, exp, max_hp, max_mp):
        super().__init__(name, job, level, hp, mp, power, guard, speed, intell, gold, exp, max_hp, max_mp)

class Magic:
    def __init__(self, name, mp_cost, base_might, category, range):
        self.name = name
        self.mp_cost = mp_cost
        self.base_might = base_might
        self.category = category #こうげきじゅもんは"attack",回復じゅもんは"heel"に分類
        self.range = range

    def magic_effect(self, character, target): #じゅもんコマンド
        might = self.base_might ** (1 + (character.intell / 10000)) 

        if self.category == "at":
            target.hp -= int(might)

            print(f"{target.name}に{int(might)}のダメージ！")

        elif self.category == "heel":
            before_hp = character.hp
            
            character.hp = min(character.max_hp, character.hp + int(might))
            
            recovery = character.hp - before_hp

            print(f"{character.name}のHPが{recovery}かいふくした！")



class Weapon:
    def __init__(self, name, price, power):
        self.name = name
        self.price = price
        self.power = power
        self.category = "weapon"
        
class Armor:
    def __init__(self, name, price, guard):
        self.name = name
        self.price = price
        self.guard = guard
        self.category = "armor"

class Item:
    def __init__(self, name, price, effect):
        self.name = name
        self.price = price
        self.effect = effect
        self.category = "item"


    def use(self, character):
        if character.hp >= character.max_hp:
            print(f"{character.name}のHPはまんたんだ！")
            return False # HPがまんたんならやくそうを消費しない

        character.hp = min(character.max_hp, character.hp + self.effect)
        # 最大HPを超えて回復しない

        print(f"{character.name}は{self.name}をつかった！")
        print(f"HPが{self.effect}かいふくした！")
        return True # かいふくしたならやくそうを消費する
    
    def expo(self):
        return f"味方のHPを{self.effect}かいふくさせる。\n一度つかうとなくなる。"
        

character1 = Character("よしひこ", "勇者", 1, 40, 5, 10, 5, 10, 10, 10, 0, 40, 5)

monster_data = [
    {
        "name": "スライム",
        "level": 1,
        "hp": 6,
        "mp": 0,
        "power": 5,
        "guard": 2,
        "speed": 3,
        "intell": 1,
        "gold": 5,
        "exp": 10,
        "max_hp": 6,
        "max_mp": 0
    },
    {
        "name": "ドラキー",
        "level": 1,
        "hp": 8,
        "mp": 0,
        "power": 6,
        "guard": 3,
        "speed": 5,
        "intell": 2,
        "gold": 8,
        "exp": 15,
        "max_hp": 8,
        "max_mp": 0
    },
    {
        "name": "おおきづち",
        "level": 1,
        "hp": 12,
        "mp": 0,
        "power": 8,
        "guard": 2,
        "speed": 2,
        "intell": 1,
        "gold": 12,
        "exp": 20,
        "max_hp": 12,
        "max_mp": 0
    },
    {
        "name": "さまようよろい",
        "level": 3,
        "hp": 60,
        "mp": 0,
        "power": 50,
        "guard": 30,
        "speed": 10,
        "intell": 1,
        "gold": 100,
        "exp": 50,
        "max_hp": 60,
        "max_mp": 0
    },
    {
        "name": "キラーマシン",
        "level": 10,
        "hp": 400,
        "mp": 0,
        "power": 200,
        "guard": 180,
        "speed": 50,
        "intell": 50,
        "gold": 1000,
        "exp": 500,
        "max_hp": 400,
        "max_mp": 0
    },

]

magic1 = Magic("メラ", 2, 10, "at", "mono_enemy")
magic2 = Magic("ホイミ", 3, 20, "heel", "mono_ally")
magic3 = Magic("ギラ", 4, 20, "at", "all_enemy")
magic4 = Magic("ヒャド", 3, 30, "at", "mono_enemy")
magic5 = Magic("イオナズン", 15, 150, "at", "all_enemy")
magic6 = Magic("ベホイミ", 5, 75, "heel", "mono_ally")
magic7 = Magic("ギガデイン", 15, 250, "at", "all_enemy")
magic8 = Magic("メラゾーマ", 10, 180, "at", "mono_enemy")

weapon1 = Weapon("ひのきのぼう", 10, 2)
weapon2 = Weapon("どうのつるぎ", 270, 8)
weapon3 = Weapon("てつのつるぎ", 1000, 18)
weapon4 = Weapon("はがねのつるぎ", 2000, 36)
weapon5 = Weapon("ほのおのつるぎ", 23000, 88)

armor1 = Armor("ぬののふく", 30, 2)
armor2 = Armor("たびびとのふく", 100, 5)
armor3 = Armor("かわのよろい", 180, 8)
armor4 = Armor("てつのよろい", 1200, 20)
armor5 = Armor("はがねのよろい", 3000, 30)
armor6 = Armor("まほうのよろい", 4200, 40)

item1 = Item("やくそう", 8, 30)
item2 = Item("上やくそう", 20, 50)
item3 = Item("特やくそう", 100, 120)
item4 = Item("特上やくそう", 500, 240)


#jsonファイルを読み込み(アプリ起動)
if os.path.exists("boukennosyo1.json"):
    with open("boukennosyo1.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    character1 = Character.from_dict(data)

else: # ぼうけんのしょが空っぽでもエラーが出ない、初期ステータスが入力される
    character1 = Character(
        "よしひこ", "勇者", 1,
        40, 5, 10, 5, 10, 10,
        10, 0, 40, 5
    )

#ここからゲーム本体

field(character1)        

print("ゲームを終了します。")



# 追加予定
# ダーマ神殿、仲間増やす、特殊イベントボス戦など、
# フィールドの位置情報　右に何歩、上に何歩などで街に入るとか
# 何歩歩けたら次のエリアに進んで、より強い敵、より強い武器防具が手に入る
# ルイーダの酒場
# 船、乗り物
# すごろくなどのミニゲーム
# 宝箱
# 小さなメダル
# 2回行動
# 特殊効果　はやぶさのけん、ほのおのつるぎ、みずのはごろもなど
# 種などのドーピングアイテム
# 自動回復系
# バイキルト、スカラ、ルカニ、ピオリム、などの補助じゅもん
# 状態異常
# ゾーン、必殺、テンション
# 難易度調節、ちゃんと難しいところをつくる
# 音楽
# マップなどドット絵で
# 不思議な鍛冶→錬金の応用
# 伝説装備
# トラップ、毒の沼地など
# 畑など育成系との合わせ技
# 恋愛シミュレーション
# リアル時間経過で種が作れるなど
# モンスター配合
# 今のはメラゾーマではない、メラだ

# 何日以内に(ターン制を広げる)この敵を倒せるように成長させる　最初はこんなのどうやって倒すの？くらいの強さにする
# 例　100日（ターン）以内に主人公を様々な要素で強化していき、ボス（ゾーマ）を倒すなど
# A.種で強化(種を作る) B.経験値を手に入れる(効率よく敵を倒す) C.呪文や特技を覚える D.武器を強力なものにする
# それぞれ時間（ターン）がかかるから、どれからやってどう効率を上げるのかがカギ
# それぞれの効率を上げるための仲間を得るミニクエストがある
# より短いターンで倒す
# 頑張ればゲームの腕でごり押すことも可能