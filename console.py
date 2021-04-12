"""

Made by JhK_ in python console
Console Version == 1.5
제작일자: 20.12.24 -

"""


import os
import sys
import asyncio

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
                print('[{}{}: {}]'.format('' if self.content['arg'][i]["isNecess"] == True else '*', i, sub.sortTypeFilter(self.content['arg'][i]['selectIn'])), end=' ')
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

    # 필수 항목만 카운트
    def calcNece(self, cmd):
        minstack = 0
        for i in cmd.content['arg']:
            if cmd.content['arg'][i]['isNecess'] == True:
                minstack += 1
            else:
                pass
        maxstack = 0
        for i in cmd.content['arg']:
            maxstack += 1
        return [minstack, maxstack]

    # 속성 값 바꾸기 & 오류 출력
    def checkSortType(self, cmd, comparis):
        # isNecessFalse = False
        isNecessCount = 0   # 필수 항목 갯수
        generatePack = []
        indexArgu = None
        WrongArgu = '속성 값이 잘못되었습니다. '
        NoneType = type(None)

        for loop in range(len(comparis[1:])):
            isNecessCount += 1
        for index, i in enumerate(cmd.content['arg']):
            if isNecessCount != 0:
                isNecessCount -= 1
                indexArgu = cmd.content['arg'][i]
                attrName = list(cmd.content['arg'].items())[index][0]

                # 리스트가 기본이면
                if type(indexArgu['selectIn']) == list:
                    if comparis[index + 1] not in indexArgu['selectIn']:
                        return WrongArgu + "({} 속성에서, {}중에 {}는 없습니다)".format(attrName, self.sortTypeFilter(indexArgu['selectIn']), comparis[index + 1])
                
                # 아무것이 기본이면
                elif type(indexArgu['selectIn']) == NoneType:
                    pass

                # 위를 제외한 것이 기본이면
                elif type(indexArgu['selectIn']) != NoneType and type(indexArgu['selectIn']) != list:
                    changeType = indexArgu['selectIn']
                    try:
                        comparis[index + 1] = changeType(comparis[index + 1])
                    except:
                        return WrongArgu + "({} 속성에서, {}는 {}로 변환될 수 없는 문자열입니다)".format(attrName, comparis[index + 1], indexArgu['selectIn'].__name__)

            else:
                break
        return [True, comparis[1:]]

    # 필수 항목이 충족되었는지 확인 & 오류 출력
    def checkLength(self, cmd, content):
        if self.calcNece(cmd)[0] <= len(content[1:]) <= self.calcNece(cmd)[1]:
            return True
        else:
            if self.calcNece(cmd)[0] == self.calcNece(cmd)[1]:
                return '\'{}\' 커맨드는 {}개의 속성이 필요로 합니다. ({}개 입력됨.)'.format(content[0], self.calcNece(cmd)[0], len(content[1:]))
            else:
                return '\'{}\' 커맨드는 최소 {}개, 최대 {}개의 속성이 필요로 합니다. ({}개 입력됨.)'.format(content[0], self.calcNece(cmd)[0], self.calcNece(cmd)[1], len(content[1:]))

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
    
    # 속성값 변환
    def cleanArg(self, cmd, content):
        basic = content.split()
        output = [basic[0]]
        for index, i in enumerate(basic[1:]):
            # data = [i for i in cmd.contnt['arg']] (data[index])
            indexArgu = cmd.content['arg']
            if i.startswith('$') == True:
                try:
                    insideVar = i[1:i.find('=')]
                    insideValue = i[i.find('=')+1:]
                    insideIndex = list(indexArgu).index(insideVar) + 1
                    if len(output) <= insideIndex:
                        while len(output) <= insideIndex:
                            appendIndex = len(output)
                            try:
                                if output[appendIndex] != None: # index 값이 존재하는 지 확인 여부
                                    pass
                                appendIndex += 1

                            except Exception as errorValue:
                                if type(errorValue) == IndexError:
                                    output.append(None)
                                    appendIndex += 1
                    output[insideIndex] = insideValue
                except:
                    pass
                    
            else:
                output.append(i)
        return output

sub = Sub()

class Default:
    # Input 위의 데코레이션(기본, 없음)
    def dec(self):
        pass
    
    # Input 가이드라인
    def wS(self):
        return "\"help\"로 도움말 보기 >>> "
    
    # 시작했을때 최초
    def onStart(self):
        pass

    # 끝났을때 최종
    def onStop(self):
        pass

de = Default()



# 콘솔 총괄
class Console:
    """
    딕셔너리로 구성된 팩을 넣으세요.
    기본 구조는 다음과 같습니다:
    [* 필수]
    {
        "listcmd": *[설정한 커맨드 목록(list로 입력)],
        "deco": 입력창 위 데코레이션(함수로 입력),
        "withStr": 입력창 데코레이션(함수로 입력),
        "version": 호환 버전(정수, 실수의 버전으로 입력),
        "isProvideCmd": 기본 내장 커맨드를 제공할 지 선택(기본: True),
        "trigger": {
            "start": 시작시 최초 출력(함수로 입력),
            "stop": 중지시 최종 출력(함수로 입력)
        }
    }
    """
        
    # 변수 생성
    def __init__(self, pack):
        # 콘솔내 변수 선언
        self.package = pack
        self.ver = 1.5

        # pack 검사
        if 'deco' not in self.package:
            self.package['deco'] = de.dec
        if 'withStr' not in self.package:
            self.package['withStr'] = de.wS
        if 'version' not in self.package:
            self.package['version'] = self.ver
        if 'isProvideCmd' not in self.package:
            self.package['isProvideCmd'] = True
        if 'trigger' not in self.package:
            self.package['trigger'] = {
                'start': de.onStart,
                'stop': de.onStop
            }
        else:
            if 'start' not in self.package:
                self.package['trigger']['start'] = de.onStart
            if 'stop' not in self.package:
                self.package['trigger']['stop'] = de.onStop
        # 필수 변수
        self.listcmd = self.package["listcmd"]
        self.stoploop = False
        
        # 선택적 변수
        self.inDeco = self.package["deco"]
        self.inGuide = self.package["withStr"]
        self.version = self.package['version']
        self.isPC = self.package['isProvideCmd']
        self.onStart = self.package['trigger']['start']
        self.onStop = self.package['trigger']['stop']

        # 사용자 바로잡이
        for i in self.listcmd:
            if i.name.lower() == "help":
                raise CannotIncludeError('Help 명령어는 기본 내장된 명령어입니다. 기본 내장 명령어를 중복사용 할 수 없습니다.')
            elif self.listcmd.count(i) > 1:
                raise CannotIncludeError('한 명령어를 중복사용 할 수 없습니다.')
        if self.version != self.ver:
            raise VersionError('1.5 버전은 {}버전과 호환되지 않습니다.'.format(self.ver))
    
    def on_start(self):
        self.onStart()
    
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
                        self.content = sub.cleanArg(value, self.contentcmd)
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
                            for index, i in enumerate([sub.checkLength, sub.checkSortType]):
                                if index == 0:
                                    if i(value, self.content) != True:
                                        print(i(value, self.content))
                                        break
                                else:
                                    if i(value, self.content)[0] != True:
                                        print(i(value, self.content))
                            os.system('pause')
            elif self.isPC == True:
                if self.content[0].lower() == 'help':
                    if len(self.content) == 1:
                        listcmdCateSort = []
                        for i in self.listcmd:
                            if i.cate != None:
                                listcmdCateSort.append(i.cate)
                        listcmdCateSort.sort()
                        print("=================================================")
                        print("<사용 가능한 커맨드>")
                        if len(self.listcmd) != 1:
                            for j in range(len(self.listcmd) - 1):
                                print('\'{}\','.format(self.listcmd[j].name), end=' ')
                            print('\'{}\'.'.format(self.listcmd[len(self.listcmd) - 1].name))
                        else:
                            print('\'{}\'.'.format(self.listcmd[0].name))
                        print(end='\n')
                        print('<커맨드 목록>')
                        print(' <커맨드> \t <설명> ')
                        for j in listcmdCateSort:
                            print('- 카테고리 \'{}\''.format(j))
                            for index in range(len(self.listcmd)):
                                if self.listcmd[index].cate == j:
                                    print(' {}\t {}'.format(self.listcmd[index].name, self.listcmd[index].desc))
                            print()    
                        print("- 카테고리 없음")
                        for indexNone in range(len(self.listcmd)):
                            if self.listcmd[indexNone].cate == None:
                                print(' {}\t {}'.format(self.listcmd[indexNone].name, self.listcmd[indexNone].desc))
                        print("=================================================")
                        print("help [커맨드]로 커맨드별 도움말 불러오기.")
                        print("=================================================")
                        os.system('pause')
                    else:
                        if self.content[1].lower() in [i.name for i in self.listcmd]:
                            for i in self.listcmd:
                                if self.content[1].lower() in i.name:
                                    value = i
                                    value.callHelp()
                        else:
                            if self.content[1].lower() != "help":
                                print("\'{}\'은/는 커맨드가 아닙니다. 명령 실행에 실패했습니다.".format(self.content[1].lower()))
                            else:
                                print("help로 명령어 도움말 출력하기")
                            os.system('pause')
                
            else:
                print("\'{}\'은/는 커맨드가 아닙니다. 명령 실행에 실패했습니다.".format(self.content[0].lower()))
                os.system('pause')

    def on_stop(self):
        self.onStop()
    
    # 콘솔 총 실행라인
    def execute(self):
        self.on_start()
        while True:
            self.inputText()
            self.inputCommand()
            if self.stoploop == True:
                self.stoploop = False
                break
        self.on_stop()

class CannotIncludeError(Exception):
    pass
class VersionError(Exception):
    pass