import sys

def ExecParserIn(DAYFILE):
    try:
        d = {}
        with open(DAYFILE) as f:
            for line in f:
                # '#'로 시작하는 라인은 무시합니다.
                if line.startswith(' ') or line.startswith('#')  or line.startswith('\r') or line.startswith('\r\n')  or line.strip() == '' :
                    continue
                
                
                # '='를 기준으로 키와 값으로 분리합니다.
                (key, val) = line.split('=')
                d[str(key)] = val.rstrip('\r\n')

        day1 = d.get('YYYY') + d.get('MM') + d.get('DD')
        days = int(d.get('DAYS'))
    except:
        print('파일이 없거나 권한이 불충분 합니다. 파일명 : [' + DAYFILE + ']')
        print('프로그램을 종료 합니다.')
        sys.exit()

ExecParserIn('/root/script/get_foresttrip_v2.in')