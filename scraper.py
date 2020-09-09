import enum
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup


class PARSE_OUTCOME(enum.Enum):
    PARK = 0,
    OTHER = -1,
    INCORRECTMETALEN = -9


TYPE   = ['Steel', 'Wood']
SCALE  = ['Extreme', 'Thrill', 'Family', 'Kiddie']
DESIGN = ['Sit Down', 'Inverted', 'Suspended', 'Wing', 'Flying', 'Stand Up', 'Bobsled', 'Pipeline']


def parse_page(soup):
    meta = soup.body.section.div.div

    CoasterName = meta.div.h1.string

    tmp = meta.div.find_all("a")
    
    if len(tmp) < 4:
        return PARSE_OUTCOME.PARK

    Park    = tmp[-4].string
    City    = tmp[-3].string
    State   = tmp[-2].string
    Country = tmp[-1].string

    Status  = meta.p.a.string

    OpSince = None
    OpUntil = None
    if Status == "Operating":
        if meta.p.time != None:
            OpSince = meta.p.time['datetime']
    elif Status == "Operated":
        tmp = meta.p.find_all('time')
        if len(tmp) == 2:
            OpSince = tmp[0]['datetime']
            OpUntil = tmp[1]['datetime']
    elif Status == "Under Construction":
        pass             # NYI
    elif Status == "In Business":
        return PARSE_OUTCOME.PARK
    elif Status == "In Production":
        pass            # NYI
    elif Status == "SBNO":
        OpUntil = meta.p.time['datetime']
    elif Status == "In Storage":
        pass            # NYI
    elif Status == "Manufactured":
        pass            # NYI
    elif Status == "Uncompleted":
        pass            # NYI
    else:
        return PARSE_OUTCOME.OTHER

    if meta.ul == None:
        return PARSE_OUTCOME.OTHER
    
    Type   = None
    Scale  = None
    Design = None
    for s in meta.ul.strings:
        if   s in TYPE:
            Type   = s
        elif s in SCALE:
            Scale  = s
        elif s in DESIGN:
            Design = s


    Length   = None
    Height   = None
    Drop     = None
    Speed    = None
    Inversions = None
    Vertical = None
    Duration = None
    spec = list(soup.find('table', {'class' : 'stat-tbl'}).strings)
    for i in range(len(spec)):
        if spec[i] == 'Length':
            Length = spec[i + 1]
        elif spec[i] == 'Height':
            Height = spec[i + 1]
        elif spec[i] == 'Drop':
            Drop = spec[i + 1]
        elif spec[i] == 'Speed':
            Speed = spec[i + 1]
        elif spec[i] == 'Inversions':
            Inversions = spec[i + 1]
        elif spec[i] == 'Vertical Angle':
            Vertical = spec[i + 1]
        elif spec[i] == 'Duration':
            Duration = spec[i + 1]
        else:
            continue
        i += 1
    
    return [CoasterName, Park, City, State, Country, Status, OpSince, OpUntil, Type, Scale, Design, Length, Height, Drop, Speed, Inversions, Vertical, Duration]


def m_2(x0, x1):
    header = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.44"}
    data = [['ID', 'CoasterName', 'Park', 'City', 'State', 'Country', 'Status', 'OpSince', 'OpUntil', 'Type', 'Scale', 'Design', 'Length', 'Height', 'Drop', 'Speed', 'Inversions', 'Vertical', 'Duration']]

    anomalies = []
    parks     = []

    for i in range(x0, x1 + 1):
        if i % 50 == 0:
            time.sleep(30)
        p = requests.get("https://rcdb.com/" + str(i) + ".htm", headers=header)
        if p.status_code == 200:
            try:
                pr = parse_page(BeautifulSoup(p.text, "html.parser"))
                if pr == PARSE_OUTCOME.PARK:
                    parks += [i]
                elif pr == PARSE_OUTCOME.INCORRECTMETALEN:
                    anomalies += [i]
                elif pr == PARSE_OUTCOME.OTHER:
                    anomalies += [i]
                else:
                    data.append([i] + pr)
            except Exception:
                anomalies += [i]
        else:
            anomalies += [i]

    pd.DataFrame(data).to_csv(     'data/rcdb' + str(x1 - 1) + '.csv',    index=False, header=False)
    pd.DataFrame(anomalies).to_csv('anomalies_i_' + str(x1 - 1) + '.csv', index=False, header=False)
    pd.DataFrame(parks).to_csv(    'parks_i_' + str(x1 - 1) + '.csv',     index=False, header=False)

    return len(data), len(parks), len(anomalies)


def main():
    x0 =              1
    x1 =     18685 // 8
    x2 =     18685 // 4
    x3 = 3 * 18685 // 8
    x4 =     18685 // 2
    x5 = 5 * 18685 // 8
    x6 = 3 * 18685 // 4
    x7 = 7 * 18685 // 8
    x8 =      18685 + 1

    xs_first_q = [x0, x1, x2]
    xs_secon_q = [x2, x3, x4]
    xs_third_q = [x4, x5, x6]
    xs_fourt_q = [x6, x7, x8]

    print("Quarter 1")
    for i in range(len(xs_first_q) - 1):
        _, _, a1 = m_2(xs_first_q[i], xs_first_q[i+1])
    print("Quarter 1 Done -", a1, "anomalies")
    time.sleep(120)
    print("Quarter 2")
    for i in range(len(xs_secon_q) - 1):
        _, _, a2 = m_2(xs_secon_q[i], xs_secon_q[i+1])
    print("Quarter 2 Done -", a2, "anomalies")
    time.sleep(120)
    print("Quarter 3")
    for i in range(len(xs_third_q) - 1):
        _, _, a3 = m_2(xs_third_q[i], xs_third_q[i+1])
    print("Quarter 3 Done -", a3, "anomalies")
    time.sleep(120)
    print("Quarter 4")
    for i in range(len(xs_fourt_q) - 1):
        _, _, a4 = m_2(xs_fourt_q[i], xs_fourt_q[i+1])
    print("Quarter 4 Done -", a4, "anomalies")


if __name__ == '__main__':
    main()
