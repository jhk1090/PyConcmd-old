"""

Made by JhK_ in python console
Console Version == 1.0
제작일자: 20.11.29:: 3:44 // 20.11.30:: 3:47

"""


import os
import sys

# 커맨드 생성
class Command:
    # 변수 생성
    def __init__(self, name, desc, trig, forceStopLoop=True):
        self.content = {}
        self.argu = {}
        self.name = name
        self.desc = desc
        self.trig = trig
        self.forceStop = forceStopLoop

    # 함수 속성과 그 설명 생성
    def descArg(self, arg, desc, descDetail=None):
        descCollab = {
            'short': desc,
            'detail': descDetail
        }
        self.argu[arg] = descCollab 
    
    # 종합 컨텐츠 불러오기
    def callCont(self):
        self.content = {
            'cmd': self.name,
            'desc': self.desc,
            'arg': self.argu
        }
    
    # 커맨드에 대한 도움말
    def callHelp(self):
        self.callCont()
        print("=================================================")
        print(self.content['desc'])
        print()
        print(self.content['cmd'].upper(), end=' ')
        if len(self.content['arg']) == 0:
            pass
        else:
            for i in self.content['arg']:
                print('[{}]'.format(i), end=' ')
        print(end='\n\n')
        for i in self.content['arg']:
            print('{} - {}'.format(i, self.content['arg'][i]['short']))
            if self.content['arg'][i]['detail'] != None:
                print('\n{}'.format(self.content['arg'][i]['detail']))
            print()
        print("=================================================")
        os.system('pause')

# 콘솔 보조
class Sub:
    def cmdWithArg(self, func, args):
        func(*args)

    def decoInputDefault(self):
        pass

    def conInputGuide(self):
        return "\"help\"로 도움말 보기 >>> "
sub = Sub()

# 콘솔 총괄
class Console:
    # 변수 생성
    def __init__(self, listcmd, inputDeco=sub.decoInputDefault, conInputguide=sub.conInputGuide):
        """
        listcmd = list()
        """
        self.listcmd = listcmd
        self.stoploop = False
        self.inDeco = inputDeco
        self.inGuide = conInputguide
    
    # 콘솔 입력
    def inputText(self):
        self.inDeco()
        self.contentcmd = input("{}".format(self.inGuide()))
    
    # 콘솔 커맨드 입력
    def inputCommand(self):
        if self.contentcmd != '':
            self.content = self.contentcmd.split()
            if self.content[0].lower() in [i.name for i in self.listcmd]:
                for i in self.listcmd:
                    if self.content[0].lower() in i.name:
                        value = i   # ?
                        value.callCont()
                        if len(self.content[1:]) == len(value.content['arg']):
                            self.stoploop = value.forceStop
                            contentarg = []
                            for i in self.content[1:]:
                                contentarg.append(i)
                            if len(value.content['arg']) != 0:
                                sub.cmdWithArg(value.trig, contentarg)
                            else:
                                value.trig()
                        else:
                            print('\'{}\' 커맨드는 총 {}개의 속성이 필요합니다. ({}개 입력됨.)'.format(self.content[0], len(value.content['arg']), len(self.content[1:])))
                            os.system('pause')
            elif self.content[0].lower() == 'help':
                if len(self.content) == 1:
                    print("=================================================")
                    print("<사용 가능한 커맨드>")
                    if len(self.listcmd) != 1:
                        for j in range(len(self.listcmd) - 1):
                            print('\'{}\','.format(self.listcmd[j].name), end=' ')
                        print('\'{}\'.'.format(self.listcmd[len(self.listcmd) - 1].name))
                    else:
                        print('\'{}\'.'.format(self.listcmd[0].name))
                    print(end='\n')
                    print("help [커맨드]로 커맨드별 도움말 불러오기.")
                    print("help list로 커맨드 모음 불러오기.")
                    print("=================================================")
                    os.system('pause')
                else:
                    if self.content[1].lower() in [i.name for i in self.listcmd]:
                        for i in self.listcmd:
                            if self.content[1].lower() in i.name:
                                value = i
                                value.callHelp()
                    elif self.content[1].lower() == 'list':
                        print("=================================================")
                        print('<커맨드 목록>')
                        print('== <커맨드> ==\t== <설명> ==')
                        for j in range(len(self.listcmd)):
                            print('{}\t{}'.format(self.listcmd[j].name, self.listcmd[j].desc))
                        print("=================================================")
                        os.system('pause')
                    else:
                        if self.content[1].lower() != "help":
                            print("\'{}\'은/는 커맨드가 아닙니다. 명령 실행에 실패했습니다.".format(self.content[1].lower()))
                        else:
                            print("help로 명령어 도움말 출력하기")
                        os.system('pause')
                
            else:
                print("\'{}\'은/는 커맨드가 아닙니다. 명령 실행에 실패했습니다.".format(self.content[0].lower()))
                os.system('pause')
    # 콘솔 총 실행라인
    def processConsole(self):
        while True:
            self.inputText()
            self.inputCommand()
            if self.stoploop == True:
                self.stoploop = False
                break



