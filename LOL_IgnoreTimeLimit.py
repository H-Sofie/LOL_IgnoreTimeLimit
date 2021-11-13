import os,easygui,sys,win32api,stat

#安装跳过WeGame补丁
#Install Skip_WeGame patch
def WeGameFix():
    os.chmod(r'.\TCLS\wegame_launch.ini',stat.S_IWRITE)
    wegame_launch_ini = open(r'.\TCLS\wegame_launch.ini' , 'w+')
    wegame_launch_ini.write('[TCLS]\ndata_name=lol')
    wegame_launch_ini.close()
    os.chmod(r'.\TCLS\wegame_launch.ini',stat.S_IREAD)
    os.chmod(r'.\TCLS\wegame_launch.tmp',stat.S_IWRITE)
    wegame_launch_tmp = open(r'.\TCLS\wegame_launch.tmp' , 'w+')
    wegame_launch_tmp.write('[TCLS]\nLastLoginMethod=1\nLocalR=99')
    wegame_launch_tmp.close()
    os.chmod(r'.\TCLS\wegame_launch.tmp',stat.S_IREAD)
    easygui.msgbox(msg = '已成功安装！', title = '完成' , ok_button = '好的')

#是否需要跳过WeGame
#Whether to skip WeGame
def WeGame_need_fix():
    suggest = 0
    with open(r'.\TCLS\wegame_launch.ini','r') as WeGame_launch:
        WeGame_launch = WeGame_launch.read()
    if '''[TCLS]
data_name=lol''' not in WeGame_launch:
        suggest = 1
    with open(r'.\TCLS\wegame_launch.tmp','r') as WeGame_launch:
        WeGame_launch = WeGame_launch.read()
    if '''[TCLS]
LastLoginMethod=1
LocalR=99''' not in WeGame_launch:
        suggest = 1
    return suggest

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
        os.chdir('.\LeagueClient\Plugins')
        with open('plugin-manifest2.json' , 'w+') as replace:
            replace.write(read4)
        os.remove('plugin-manifest.json')
        os.rename('plugin-manifest2.json' , 'plugin-manifest.json')
        easygui.msgbox(msg = '已成功替换{}处'.format(t) , title = '完成' , ok_button = '好的')

#定义一个获取exe文件版本的函数
#Define a function to get the version of the exe file.
def getFileVersion(file_name):
    info = win32api.GetFileVersionInfo(file_name, os.sep)
    ms = info['FileVersionMS']
    ls = info['FileVersionLS']
    version = '%d.%d.%d.%04d' % (win32api.HIWORD(ms), win32api.LOWORD(ms), win32api.HIWORD(ls), win32api.LOWORD(ls))
    return version

times = 0

#判断是否有路径配置文件
#Judge whether there is a path configuration file.
Settingpath = 'C:' + os.environ['HOMEPATH'] + r'\AppData\Roaming\LOL_TimeLimit\Setting.txt'
if os.path.exists(Settingpath):
    Spath = open(Settingpath , 'r+')
    Spathline = Spath.readlines()
    Spath.close()
    Spath = Spathline[1]
    Spath = Spath.lstrip('[PATH]=')
    os.chdir(Spath)
elif not os.path.exists('C:' + os.environ['HOMEPATH'] + r'\AppData\Roaming\LOL_TimeLimit'):
    os.mkdir('C:' + os.environ['HOMEPATH'] + r'\AppData\Roaming\LOL_TimeLimit')

#循环检测路径直到匹配
#Loop the path until the match is successful.
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

#写入路径配置文件
#Write the path configuration file.
with open(Settingpath,'w+') as Settingpath:
    Settingpath.write('#该文件为路径配置文件请勿删除！' + '\n[PATH]=' + Spath)

#获取游戏版本
#Get the game version.
Game_Version = getFileVersion(r'.\Game\League of Legends.exe')

#读进read
#Read in 'read'.
with open(r'.\LeagueClient\Plugins\plugin-manifest.json' , 'r+') as file:
        read = file.read()

#先锁文件防傻狗TX乱改
#Lock the file to prevent TX from messing up.
os.chmod(r'.\TCLS\wegame_launch.tmp',stat.S_IREAD)
os.chmod(r'.\TCLS\wegame_launch.ini',stat.S_IREAD)
#执行的操作
#Operation.
if Statistics() == 0 and WeGame_need_fix() == 0:
    easygui.msgbox(msg = '您无需修改',title = '提示',ok_button = '好的')
    easygui.msgbox(msg = '有疑问或bug反馈请在Github上提交issues\n\n源码参见:https://github.com/SaoHYC/LOL_IgnoreTimeLimit' , title = 'Debug' , ok_button = '好的')
    sys.exit()
elif Statistics() != 0 and WeGame_need_fix() == 0:
    choice = easygui.buttonbox(msg = '目前可以修改{num}处地方解除限时(共3处)\n\n选择操作：'.format(num = Statistics()) ,title = '适配游戏版本{}'.format(Game_Version),choices = ['修改文件','取消'])
elif Statistics() == 0 and WeGame_need_fix() != 0:
    choice = easygui.buttonbox(msg = '目前可以破解WeGame强制登录，是否安装补丁？',title = '适配游戏版本{}'.format(Game_Version),choices = ['安装补丁','取消'])
elif Statistics() != 0 and WeGame_need_fix() != 0:
    choice = easygui.buttonbox(msg = '目前可以修改{num}处地方解除限时(共3处)\n\n可以安装跳过WeGame补丁\n\n选择操作：'.format(num = Statistics()) ,title = '适配游戏版本  {}'.format(Game_Version),choices = ['修改文件','安装补丁','一键修复','取消'])

#调用函数
#Call function.
if choice == '修改文件':
    replace_json()
if choice == '安装补丁':
    WeGameFix()
if choice == '一键修复':
    WeGameFix()
    replace_json()
if choice == '取消':
    easygui.msgbox(msg = '操作已取消' , title = 'Cancel' , ok_button = '好的')
easygui.msgbox(msg = '有疑问或bug反馈请在Github上提交issues\n\n源码参见:https://github.com/SaoHYC/LOL_IgnoreTimeLimit' , title = 'Debug' , ok_button = '好的')