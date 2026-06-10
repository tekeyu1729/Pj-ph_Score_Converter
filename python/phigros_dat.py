import PySimpleGUI as sg
import math
import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
data_path = os.path.join(BASE_DIR, "data.dat")

if not os.path.exists(data_path):
    sg.popup_error("data.datがありません")
    sys.exit()

KEY = 172

def load_data():
    with open(data_path, "rb") as f:
        encrypted = f.read()
    text = bytes(b ^ KEY for b in encrypted).decode("utf-8")
    return json.loads(text)

data = load_data()

def save_data(data):
    text = json.dumps(data,ensure_ascii=False,indent=4)
    encrypted = bytes(b ^ KEY for b in text.encode("utf-8"))
    with open(data_path, "wb") as f:
        f.write(encrypted)

def level_load():
    for j in range(3):
        level_load_2=[i[0] for i in data[j]]
        level_load_0=[i[1] for i in data[j]]
        if [] in level_load_0 :
            del data[j][level_load_0.index([])]

def add_level():
    for i in range(3):
        diff_level.append(f"{diff[i]} {data[i][1][0]}~{data[i][-1][0]}")

level=[""]
music=[""]
diff_level=[]
diff=[i[0][0] for i in data[:-1]]
for i in range(3):
    data[i][0].insert(1,len(data[i])-1)

level_load()
add_level()
    
layout_main = [
    [sg.Listbox(values=diff, size=(10, 4),default_values=[],key='-diff-'), sg.Listbox(values=level, size=(10, 4),default_values=[],key='-level-'), sg.Listbox(values=music, size=(20, 4),default_values=[],key='-music-'), sg.Button('リセット')],
    [sg.Button("決定"),sg.Text("", size=(33, 1), key="-OUTPUT-"),sg.Button("設定"),sg.Button("閉じる")],
]

def make_layout_sub():
    return [
        [sg.Text("", size=(40, 1), key="-kyokumei-")],
        [sg.Text("Max Combo", size=(13,1)),sg.Input(size=(15,1), key='-combo-')],
        [sg.Text("Parfect", size=(13,1)),sg.Input(size=(15,1), key='-parfect-')],
        [sg.Text("Great", size=(13,1)),sg.Input(size=(15,1), key='-great-')],
        [sg.Button('計算', key="-keisan-"),sg.Button("戻る", key="-modoru_1-"),sg.Text("", size=(35,1), key="-kekka-")]
    ]

def make_layout_add():
    return [
        [sg.Text("難易度", size=(13,1)), sg.Listbox(values=diff_level, size=(15, 3),default_values=[],key="-ADD_DIFF-")],
        [sg.Text("レベル", size=(13,1)), sg.Input(size=(15,1),key="-ADD_LEVEL-")],
        [sg.Text("曲名", size=(13,1)), sg.Input(size=(15,1),key="-ADD_MUSIC-")],
        [sg.Text("コンボ", size=(13,1)), sg.Input(size=(15,1),key="-ADD_COMBO-")],
        [sg.Button("楽曲追加"),sg.Button("戻る", key="-modoru_2-")]
    ]

def make_layout_set():
    return [
        [sg.Button("追加", size=(11,1)),sg.Button("削除", size=(11,1))],
        [sg.Button("(追加/削除)パスワード変更", size=(24,1),key="-pas-")],
        [sg.Text("")],
        [sg.Button("戻る", key="-modoru_3-")]
    ]

def make_layout_pas():
    return [
        [sg.Text("現在の追加・削除用パスワード")],
        [sg.Text("追加用", size=(10,1)), sg.Input(size=(20,1),key="-pas_ad_re-",password_char="*")],
        [sg.Text("削除用", size=(10,1)), sg.Input(size=(20,1),key="-pas_re_re-",password_char="*")],
        [sg.Button("決定",key="-pas_0-"),sg.Button("戻る", key="-modoru_4-")]
    ]

def make_layout_new_pas():
    return [
        [sg.Text("新しい追加・削除用パスワード")],
        [sg.Text("追加用", size=(10,1)), sg.Input(size=(20,1),key="-pas_ad-",password_char="*")],
        [sg.Text("確認", size=(10,1)), sg.Input(size=(20,1),key="-pas_ad_ck-",password_char="*")],
        [sg.Text("")],
        [sg.Text("削除用", size=(10,1)), sg.Input(size=(20,1),key="-pas_re-",password_char="*")],
        [sg.Text("確認", size=(10,1)), sg.Input(size=(20,1),key="-pas_re_ck-",password_char="*")],
        [sg.Button("決定",key="-pas_1-"),sg.Button("戻る", key="-modoru_5-")]
    ]

window_main = sg.Window("phigrosスコア化", layout_main,finalize=True)

while True:
    window, event, values = sg.read_all_windows()
    if event == sg.WIN_CLOSED or event == '閉じる':
        break

    elif event == 'リセット' or event == "-modoru_1-" or event == "-modoru_2-" or event == "-modoru_3-":
        window_main['-diff-'].update(set_to_index=[])
        window_main['-level-'].update(set_to_index=[])
        window_main['-music-'].update(set_to_index=[])
        level=[]
        window_main["-level-"].update(values=level)
        music=[]
        window_main["-music-"].update(values=music)
        window_main["-OUTPUT-"].update("")

    elif event == "決定":
        if values["-diff-"]!=[] and values["-level-"]==[] and values["-music-"]==[]:
            window_main["-OUTPUT-"].update(f"選択されたのは {values["-diff-"][0]} です。")
            diff_0=diff.index(values["-diff-"][0])
            for i in range(3):
                if diff_0==i:
                    level=[j[0] for j in data[i]]
                    level.remove(diff[i])
            window_main["-level-"].update(values=level)

        elif values["-diff-"]!=[] and values["-level-"]!=[] and values["-music-"]==[]:
            window_main["-OUTPUT-"].update(f"選択されたのは {values["-diff-"][0]} {values["-level-"][0]} です。")
            level_0=level.index(values["-level-"][0])
            level_load()
            for k in range(3):
                if diff_0==k:
                    for i in range(data[k][0][1]):
                        if level_0==i:#ex30*6,#ex31*12,#ex32*1,#ms33*13,#ms34*7#ms35*7#ms36*1#ms38*1,#ap31*15,#ap32*11,#ap33*11,#ap34*4,#ap35*5,#ap36*5,#ap37*6,#ap38*1
                            music=[j[0] for j in data[k][i+1][1]]
            window_main["-music-"].update(values=music)

        elif values["-diff-"]!=[] and values["-level-"]!=[] and values["-music-"]!=[]:
            music_0=music.index(values["-music-"][0])
            window_sub = sg.Window("phigrosスコア化",make_layout_sub(),finalize=True)
            window_sub["-kyokumei-"].update(f"選択されたのは {values["-diff-"][0]} {values["-level-"][0]} , {values["-music-"][0]} です。")
        else:
            window_main["-OUTPUT-"].update(f"難易度を選択してください")

    elif event == "-keisan-" and window_sub is not None:
        if values["-combo-"]=="" or values["-parfect-"]=="" or values["-great-"]=="":
            sg.popup_ok("情報を入力して下さい")
        else:
            furukon=data[diff_0][level_0+1][1][music_0][1]#levelの変更
            furukon=2*furukon
            parfect=int(values["-parfect-"])
            great=int(values["-great-"])
            combo=int(values["-combo-"])
            sukoa=float((10/furukon)*(9*(parfect+great*0.65)+combo))
            for i in range(4):
                if sukoa>=100-4*i:
                    hantei_1=i
            if sukoa<=3:
                if sukoa>=82:
                    hantei_1=4
                elif sukoa>=70:
                    hantei_1=5
                elif sukoa<70:
                    hantei_1=6
            hantei_2=["φ","V","S","A","B","C","F"]
            if 10*(10000*sukoa%1)<5:
                sukoa=math.floor(10000*sukoa)
            else:
                sukoa=math.ceil(10000*sukoa)
            if sukoa>=1000000:
                sukoa=1000000
            window_sub["-kekka-"].update(f"{sukoa} {hantei_2[int(hantei_1)]}")

    elif event == "設定":
        diff_set=values["-diff-"]
        level_set=values["-level-"]
        music_set=values["-music-"]
        window_set = sg.Window("設定",make_layout_set(),finalize=True)

    elif event == "追加":
        password = sg.popup_get_text("追加キーを入力してください",password_char="*")
        if str(password) == data[3][0]:
            sg.popup("認証成功")
            window_add = sg.Window("楽曲追加",make_layout_add(),finalize=True)
        else:
            sg.popup_error("パスワードが違います")

    elif event == "削除":
        password = sg.popup_get_text("削除キーを入力してください",password_char="*")
        if str(password) == data[3][1]:
            sg.popup("認証成功")
            if diff_set==[] or level_set==[] or music_set==[]:
                sg.popup_ok("削除楽曲を選択して下さい")
            else:
                if sg.popup_yes_no(f"{diff_set[0]}{level_set[0]} , {music_set[0]}を削除しますか？") == "Yes":
                    music_0=music.index(music_set[0])
                    data[diff_0][level_0+1][1].remove([music_set[0],data[diff_0][level_0+1][1][music_0][1]])
                    level_load()
                    save_data(data)
                    diff_level.clear
                    add_level()
                    sg.popup_ok("楽曲を削除しました")

        else:
            sg.popup_error("パスワードが違います")

    elif event == "楽曲追加":
        if values["-ADD_DIFF-"]=="" or values["-ADD_LEVEL-"]=="" or values["-ADD_MUSIC-"]=="" or values["-ADD_COMBO-"]=="":
            sg.popup_ok("楽曲情報を追加して下さい")
        else:
            diff_add = values["-ADD_DIFF-"][0]
            level_add = int(values["-ADD_LEVEL-"])
            music_add = values["-ADD_MUSIC-"]
            combo_add = int(values["-ADD_COMBO-"])
            if sg.popup_yes_no(f"{diff_add}{level_add}{music_add} , コンボ数{combo_add}を追加しますか？") == "Yes":
                combo_add = combo_add/2
                diff_add_0=diff_level.index(diff_add)
                level_1=[i[0] for i in data[diff_add_0]]
                del level_1[0]
                if not level_add in level_1 :
                    i=1
                    while i < data[diff_add_0][0][1] :
                        if data[diff_add_0][i][0] > level_add :
                            data_add_1=[level_add,[]]
                            data[diff_add_0].insert(i,data_add_1)
                            break
                        i=i+1
                for i in range(3):
                    if diff_add_0==i:
                        level=[j[0] for j in data[i]]
                data[diff_add_0][level.index(level_add)][1].append([music_add, combo_add])
                save_data(data)
                diff_level.clear
                add_level()
                sg.popup_ok("楽曲を追加しました")
                window_add.close()

    elif event == "-pas-":
        window_pas = sg.Window("パスワード確認", make_layout_pas(),finalize=True)

    elif event == "-pas_0-":
        if str(values["-pas_ad_re-"]) == data[3][0] and str(values["-pas_re_re-"]) == data[3][1] :
            pas_ad=int(values["-pas_ad_re-"])
            pas_re=int(values["-pas_re_re-"])
            window_new_pas = sg.Window("パスワード設定", make_layout_new_pas(),finalize=True)
        else:
            sg.popup_error("パスワードが違います")
    
    elif event == "-pas_1-":
        if values["-pas_ad-"] == values["-pas_ad_ck-"] and values["-pas_re-"] == values["-pas_re_ck-"]:
            del data[3]
            data.insert(3,[values["-pas_ad-"],values["-pas_re-"]])
            save_data(data)
            sg.popup_ok("パスワードを変更しました")
        else:
            sg.popup_ok("入力が間違っています")


    if event == "-modoru_1-"  :
        window_sub.close()

    elif event == "-modoru_2-" :
        window_add.close()

    elif event == "-modoru_3-"  :
        window_set.close()
    
    elif event == "-modoru_4-" or event == "-pas_0-"  :
        window_pas.close()

    elif event == "-modoru_5-" or event == "-pas_1-" :
        window_new_pas.close()
