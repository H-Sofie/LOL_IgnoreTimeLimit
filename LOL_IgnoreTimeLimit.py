import os,easygui,sys,win32api,requests

#定义联网获取源json的还原函数
#Define the restore function to get the source JSON through networking.
def back(file):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
    try:
        r = requests.get('https://raw.githubusercontent.com/SaoHYC/LOL_IgnoreTimeLimit/Main/plugin-manifest.json' , headers = headers)
    except:
        easygui.msgbox(msg = '无法与互联网建立连接，请再次重试' , title = '网络连接失败' , ok_button = '好的')
        sys.exit()
    r = r.text
    with open('test.txt' , 'w+') as file_write:
        file_write.write(r)
    with open('test.txt' , 'r+') as file_write:
        lines = file_write.readlines()
    del lines[-2:]
    file_rstrip = open('test2.txt' , 'a+')
    for line in lines:
        line = line.rstrip()
        if len(line) != 0:
            file_rstrip.writelines(line)
            file_rstrip.write('\n')
    file_rstrip.close()
    with open('test2.txt' , 'a+') as file_add:
        file_add.write('}')
    with open('test2.txt' , 'r+') as lastestfile:
        the_backup = lastestfile.read()
    file.write(the_backup)
    os.remove('test.txt')
    os.remove('test2.txt')

#定义一个统计函数
#Define a statistical function.
def Statistics():
        need = 0
        if '''            "name": "rcp-be-lol-kickout",
            "affinity": null,
            "lazy": false''' in read:
                need +=1
        if '''            "name": "rcp-fe-lol-kickout",
            "affinity": null,
            "lazy": false''' in read:
                need += 1
        if '''            "name": "rcp-be-lol-kr-playtime-reminder",
            "affinity": null,
            "lazy": false''' in read:
                need += 1
        return need

#定义一个用于修改替换的函数
#Define a function to modify and replace.
def replace_json():
        t = 0
        if '''            "name": "rcp-be-lol-kickout",
            "affinity": null,
            "lazy": false'''in read:

            read2 = read.replace('''            "name": "rcp-be-lol-kickout",
            "affinity": null,
            "lazy": false''' , '''            "name": "rcp-be-lol-kickout",
            "affinity": null,
            "lazy": true''')
            t += 1
        else:
            read2 = read
        if  '''            "name": "rcp-fe-lol-kickout",
            "affinity": null,
            "lazy": false'''in read2:

            read3 = read2.replace('''            "name": "rcp-fe-lol-kickout",
            "affinity": null,
            "lazy": false''' , '''            "name": "rcp-fe-lol-kickout",
            "affinity": null,
            "lazy": true''')
            t += 1
        else:
            read3 = read2
        if '''            "name": "rcp-be-lol-kr-playtime-reminder",
            "affinity": null,
            "lazy": false'''in read3:

            read4 = read3.replace('''            "name": "rcp-be-lol-kr-playtime-reminder",
            "affinity": null,
            "lazy": false''' , '''            "name": "rcp-be-lol-kr-playtime-reminder",
            "affinity": null,
            "lazy": true''')
            t += 1
        else:
            read4 = read3

        with open('plugin-manifest2.json' , 'w+') as replace:
            replace.write(read4)
        os.remove('plugin-manifest.json')
        os.rename('plugin-manifest2.json' , 'plugin-manifest.json')
        easygui.msgbox(msg = '已成功替换{}处'.format(t) , title = '完成' , ok_button = '好的')

#定义一个获取exe文件版本的函数
#Define a function to get the version of the EXE file.
def getFileVersion(file_name):
    info = win32api.GetFileVersionInfo(file_name, os.sep)
    ms = info['FileVersionMS']
    ls = info['FileVersionLS']
    version = '%d.%d.%d.%04d' % (win32api.HIWORD(ms), win32api.LOWORD(ms), win32api.HIWORD(ls), win32api.LOWORD(ls))
    return version

#循环检测路径直到匹配
#Loop the path until the match is successful.
times = 0
while not os.path.isdir('LeagueClient') and times == 0:
    times += 1
    choice = easygui.buttonbox(msg = '没有检测到当前目录下的英雄联盟相关文件，请手动选择英雄联盟游戏目录！' , title = '手动选择' , choices = ['选择' , '取消'])
    if choice == '选择':
        Spath = easygui.diropenbox()
        os.chdir(Spath)
    else:
        sys.exit()
while not os.path.isdir('LeagueClient') and times == 1:
    choice = easygui.buttonbox(msg = '你选择位置不合适，需要选择“英雄联盟”文件夹（内含LeagueClient等文件夹）！',title = '注意！',choices = ['重新选择' , '取消'])
    if choice == '重新选择':
        Spath = easygui.diropenbox()
        os.chdir(Spath)
    else:
        sys.exit()

Game_Version = getFileVersion(r'.\Game\League of Legends.exe')

#更改工作路径并读进read
#Change working path and read in 'read'.
os.chdir(r'.\LeagueClient\Plugins')
with open('plugin-manifest.json' , 'r+') as file:
        read = file.read()

#当不需要修改时执行的操作
#Operation when no modification is required.
if Statistics() == 0:
    choice = easygui.buttonbox(msg = '不需要再修改了，但可以还原文件',title = '提示',choices = ['还原为官方文件' , '退出'])
    if choice == '还原为官方文件':
        with open('plugin-manifest.json' , 'w+') as backup:
            back(backup)
        easygui.msgbox(msg = '已成功还原' , title = '还原' , ok_button = '好的')
    easygui.msgbox(msg = '有疑问或bug反馈请在Github上提交issues\n\n源码参见:https://github.com/SaoHYC/LOL_IgnoreTimeLimit',title = 'Debug',ok_button = '好的')
    sys.exit()
choice = easygui.buttonbox(msg = '目前可以修改{num}处地方(共3处)\n\n选择操作：'.format(num = Statistics()) ,title = '适配游戏版本{}'.format(Game_Version),choices = ['修改文件','还原为官方文件','取消'])

#调用replace_json函数
#Call replace_json function.
if choice == '修改文件':
    replace_json()

#恢复源文件
#Restore files.
elif choice == '还原为官方文件':
    with open('plugin-manifest.json' , 'w+') as backup:
        back(backup)
    easygui.msgbox(msg = '已成功还原' , title = '还原' , ok_button = '好的')
easygui.msgbox(msg = '有疑问或bug反馈请在Github上提交issues\n\n源码参见:https://github.com/SaoHYC/LOL_IgnoreTimeLimit' , title = 'Debug' , ok_button = '好的')