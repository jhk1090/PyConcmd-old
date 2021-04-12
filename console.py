"""

Made by JhK_ in python console
Console Version == 1.2
제작일자: 20.12.16:: PM 10:-- // 20.12.17:: PM 1:18

"""


import os
import sys

# 커맨드 생성
class Command:
    # 변수 생성
    def __init__(self, name, desc, trig, forceStopLoop=True, category=None):
        self.content = {}
        self.argu = {}
        self.name = name
        self.desc = desc
        self.trig = trig
        self.forceStop = forceStopLoop
        self.cate = category

    # 함수 속성과 그 설명 생성
    def descArg(self, arg, desc, descDetail=None, isNecess=True, setSelect=None):
        descCollab = {
            'short': desc,
            'detail': descDetail,
            'selectIn': setSelect,
            'isNecess': isNecess
        }
        self.argu[arg] = descCollab 
    
    # 종합 컨텐츠 불러오기
    def callCont(self):
        self.content = {
            'cmd': self.name,
            'desc': self.desc,
            'arg': self.argu,
            'cate': self.cate
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
                print('[{}{}: {}]'.format('' if self.content['arg'][i]["isNecess"] == True else '*', i, sub.sortTypeFilter(self.content['arg'][i]['selectIn']), end=' '))
        print(end='\n\n')
        for i in self.content['arg']:
            print('{}{} - {}'.format('' if self.content['arg'][i]['isNecess'] == True else '*', i, self.content['arg'][i]['short']))
            if self.content['arg'][i]['detail'] != None:
                print('\n{}'.format(self.content['arg'][i]['detail']))
            print()
        print("=================================================")
        os.system('pause')

# 콘솔 보조
class Sub:
    # 트리거와 속성 합쳐 실행
    def cmdWithArg(self, func, args):
        func(*args)

    # Input 위의 데코레이션(기본, 없음)
    def decoInputDefault(self):
        pass
    
    # Input 가이드라인
    def conInputGuide(self):
        return "\"help\"로 도움말 보기 >>> "

    # 필수 항목만 카운트
    def calcExceptNece(self, cmd):
        stack = 0
        for i in cmd.content['arg']:
            if cmd.content['arg'][i]['isNecess'] == True:
                stack += 1
            else:
                pass
        return stack
    
    # 속성 값 바꾸기 & 오류 출력
    def checkSortType(self, cmd, comparis):
        WrongArgu = '속성 값이 잘못되었습니다. '
        NoneType = type(None)
        for index, i in enumerate(cmd.content['arg']):
            indexArgu = cmd.content['arg'][i]
            try:
                # 리스트가 기본이면
                if type(indexArgu['selectIn']) == list and (indexArgu['isNecess'] == True or i == comparis[index + 1]):
                    if comparis[index + 1] in indexArgu['selectIn']:
                        pass
                    else:
                        return WrongArgu + "({}중에 {}는 없습니다)".format(self.sortTypeFilter(indexArgu['selectIn']), comparis[index + 1])
                
                # 아무것이 기본이면
                elif type(indexArgu['selectIn']) == NoneType and (indexArgu['isNecess'] == True or i == comparis[index + 1]):
                    pass

                # 위를 제외한 것이 기본이면
                elif type(indexArgu['selectIn']) != NoneType and type(indexArgu['selectIn']) != list\
                    and (indexArgu['isNecess'] == True or i == comparis[index + 1]):
                    changeType = indexArgu['selectIn']
                    try:
                        comparis[index + 1] = changeType(comparis[index + 1])
                    except:
                        return WrongArgu + "({}로 변환될 수 없는 문자열입니다)".format(indexArgu['selectIn'].__name__)
                    else:
                        pass
            except:
                # 만약 필수 항목이 아니라면 // 현재 필수 항목은 한개만 지정 가능
                pass
        return [True, comparis[1:]]

    # 필수 항목이 충족되었는지 확인 & 오류 출력
    def checkLength(self, cmd, content):
        if len(content[1:]) == self.calcExceptNece(cmd):
            return True
        else:
            return '\'{}\' 커맨드는 총 {}개의 속성이 필수로 필요로 합니다. ({}개 입력됨.)'.format(content[0], self.calcExceptNece(cmd), len(content[1:]))

    # arg에 넣을 수 있는 type 디스플레이 표시
    def sortTypeFilter(self, source):
        if source == None:
            return 'any'
        else:
            if type(source) == list:
                output = ''
                output += '<'
                for index, i in enumerate(source):
                    if len(source) != index + 1:
                        output += "{}|".format(i)
                    else:
                        output += "{}".format(i)
                output += '>'
                return output
            else:
                return source.__name__


        

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
                        # 오류가 있는지 확인
                        if sub.checkLength(value, self.content) == True and sub.checkSortType(value, self.content)[0] == True:
                            self.stoploop = value.forceStop
                            contentarg = []
                            # 속성 추가
                            for arg in sub.checkSortType(value, self.content)[1]:
                                contentarg.append(arg)
                            if len(self.content[1:]) != len(sub.checkSortType(value, self.content)[1]):
                                for j in range(len(self.content[1:]) - len(sub.checkSortType(value, self.content)[1])):
                                    contentarg.append(None)
                            # 트리거 실행
                            if len(value.content['arg']) != 0:
                                sub.cmdWithArg(value.trig, contentarg)
                            else:
                                value.trig()
                        # 오류 출력
                        else:
                            for i in [sub.checkLength, sub.checkSortType]:
                                if i(value, self.content) == True:
                                    pass
                                else:
                                    print(i(value, self.content))
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
                        listcmdCateSort = []
                        for i in self.listcmd:
                            if i.cate != None:
                                listcmdCateSort.append(i.cate)
                        listcmdCateSort.sort()

                        print("=================================================")
                        print('<커맨드 목록>')
                        print('== <커맨드> ==\t== <설명> ==')
                        for j in listcmdCateSort:
                            print('- 카테고리 \'{}\''.format(j))
                            for index in range(len(self.listcmd)):
                                if self.listcmd[index].cate == j:
                                    print('{}\t{}'.format(self.listcmd[index].name, self.listcmd[index].desc))
                            print()    
                        print("- 카테고리 없음")
                        for indexNone in range(len(self.listcmd)):
                            if self.listcmd[indexNone].cate == None:
                                print('{}\t{}'.format(self.listcmd[indexNone].name, self.listcmd[indexNone].desc))
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

