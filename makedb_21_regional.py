import xlrd
import glob
import sqlite3
import os
import sys

hanstart = 0xac00
fcs = ('g', 'gg', 'n', 'd', 'dd', 'r', 'm', 'b', 'bb', 's', 'ss', '', 'j', 'jj', 'ch', 'k', 't', 'p', 'h')
mcs = ('a', 'ae', 'ya', 'yae', 'eo', 'ei', 'yeo', 'yei', 'o', 'wa', 'wae', 'wai', 'yo', 'u', 'wueo', 'wuei', 'wi', 'yu', 'eu', 'eui', 'i')
lcs = ('', 'g', 'gg', 'gs', 'n', 'nj', 'nh', 'd', 'l', 'lg', 'lm', 'lb', 'ls', 'lt', 'lp', 'lh', 'm', 'b', 'bs', 's', 'ss', 'ng', 'j', 'ch', 'k', 't', 'p', 'h')
fcsl = len(fcs)
mcsl = len(mcs)
lcsl = len(lcs)
mlsize = mcsl * lcsl

def get_uid ():
    global uid
    uid += 1
    return uid

def get_eng (name):
    newname = ''
    for c in name:
        n = ord(c)
        if n < hanstart:
            newname += c
        else:
            n = n - hanstart
            fn = int(n / mlsize)
            rem = n % mlsize
            mn  = int(rem / lcsl)
            ln = rem % lcsl
            newname += fcs[fn] + mcs[mn] + lcs[ln]
    return newname

dbpath = sys.argv[1]
engflag = sys.argv[2]
if os.path.exists(dbpath):
    os.remove(dbpath)
db = sqlite3.connect(dbpath)
c = db.cursor()
c.execute('create table area1 (uid int, name text)')
c.execute('create table area2 (uid int, name text, area1 int, unique (name, area1))')
c.execute('create table area3 (uid int, name text, area2 int, sum_people int, sum_vote int, sum_invalid int, sum_novote int, unique (name, area2))')
c.execute('create table area4 (uid int, name text, area3 int, sum_people int, sum_vote int, sum_invalid int, sum_novote int, unique (name, area3))')
c.execute('create table party (uid int, name text)')
c.execute('create table candidate (uid int, name text, party int, unique(name, party))')
c.execute('create table vote (candidate int, area int, vote int, unique (candidate, area))')
c.execute('create index area1_idx1 on area1 (uid)')
c.execute('create index area1_idx2 on area1 (name)')
c.execute('create index area2_idx1 on area2 (uid)')
c.execute('create index area2_idx2 on area2 (name)')
c.execute('create index area2_idx3 on area2 (area1)')
c.execute('create index area3_idx1 on area3 (uid)')
c.execute('create index area3_idx2 on area3 (name)')
c.execute('create index area3_idx3 on area3 (area2)')
c.execute('create index area4_idx1 on area4 (uid)')
c.execute('create index area4_idx2 on area4 (name)')
c.execute('create index area4_idx3 on area4 (area3)')
c.execute('create index party_idx1 on party (uid)')
c.execute('create index party_idx2 on party (name)')
c.execute('create index candidate_idx1 on candidate (uid)')
c.execute('create index candidate_idx2 on candidate (name)')
c.execute('create index vote_idx1 on vote (candidate)')

uid = 0
parties = {}
candidates = {}
fns_1=os.listdir('.')
fns_1_area1 = {}
for fn_1 in fns_1:
    if os.path.isdir(fn_1) == False:
        continue
    area1 = fn_1.lstrip('1234567890')
    if engflag == 'eng':
        area1 = get_eng(area1)
    fns_1_area1[area1] = fn_1
area1s = list(fns_1_area1.keys())
area1s.sort()
independent_party_count = 1
for area1 in area1s:
    if engflag == 'eng':
        area1 = get_eng(area1)
    area1_uid = get_uid()
    c.execute(f'insert into area1 values ({area1_uid}, "{area1}")')
    print(f'fns_1_area1={fns_1_area1}')
    fn_1 = fns_1_area1[area1]
    print(area1, fn_1)
    fns_2 = glob.glob(os.path.join(fn_1, '*.xlsx'))
    for fn_2 in fns_2:
        if '~$' in fn_2:
            continue
        wb=xlrd.open_workbook(fn_2)
        sheet=wb.sheets()[0]
        # area2
        area2 = '_'.join(fn_2[:-5].split('_')[1:])
        if engflag == 'eng':
            area2 = get_eng(area2)
        area2_uid = get_uid()
        row = sheet.row(6)
        print(f'@ area1={area1} area2={area2}')
        c.execute(f'insert into area2 values ({area2_uid}, "{area2}", {area1_uid})')
        # parties and candidates
        row = sheet.row(4)
        parties_candidates_t = [v.value.split('\n') for v in row[4:-3]]
        parties_t = []
        candidates_t = []
        end_col_candidate = 0
        for i in range(len(parties_candidates_t)):
            v = parties_candidates_t[i]
            if v[0] == '':
                end_col_candidate = i
                break
            if v[0] == '무소속':
                v[0] += str(independent_party_count)
                independent_party_count += 1
            parties_t.append(v[0])
            candidates_t.append(v[1])
        party_uids = {}
        candidate_uids = {}
        for i in range(len(candidates_t)):
            party = parties_t[i]
            candidate = candidates_t[i]
            if engflag == 'eng':
                candidate = get_eng(candidate)
            if engflag == 'eng':
                party = get_eng(party)
            if party not in parties:
                party_uid = get_uid()
                parties[party] = party_uid
                c.execute(f'insert into party values ({party_uid}, "{party}")')
                candidates[party_uid] = {}
            else:
                party_uid = parties[party]
            if party_uid in candidates and candidate in candidates[party_uid]:
                candidate_uid = candidates[party_uid][candidate]
            else:
                candidate_uid = get_uid()
                c.execute(f'insert into candidate values ({candidate_uid}, "{candidate}", {party_uid})')
                candidates[party_uid][candidate] = candidate_uid
            party_uids[i] = party_uid
            candidate_uids[i] = candidate_uid
        # area3
        for rowno in range(7, 11):
            row = sheet.row(rowno)
            area3 = row[0].value
            if area3 == '합계':
                continue
            if area3 == '거소·선상투표':
                area3 = 'disabled_ship'
            if area3 == '관외사전투표':
                area3 = 'prevote_out'
            if area3 == '국외부재자투표':
                area3 = 'abroad'
            if area3 == '국외부재자투표(공관)':
                area3 = 'abroad_office'
            if engflag == 'eng':
                area3 = get_eng(area3)
            area3_uid = get_uid()
            num_people = int(row[2].value)
            num_vote = int(row[3].value)
            num_invalid = int(row[-2].value)
            num_novote = int(row[-1].value)
            c.execute(f'insert into area3 values ({area3_uid}, "{area3}", {area2_uid}, {num_people}, {num_vote}, {num_invalid}, {num_novote})')
            for i in range(len(candidates_t)):
                candidate_uid = candidate_uids[i]
                c.execute(f'insert into vote values ({candidate_uid}, {area3_uid}, {int(row[i + 4].value)})')
        rowno = 11
        while True:
            if rowno >= sheet.nrows:
                break
            row = sheet.row(rowno)
            rowno += 1
            area3_t = row[0].value
            if area3_t == '잘못 투입·구분된 투표지':
                end_rowno = rowno - 1
                break
            if area3_t != '':
                area3 = area3_t
                if engflag == 'eng':
                    area3 = get_eng(area3)
                area3_uid = get_uid()
                num_people = int(row[2].value)
                num_vote = int(row[3].value)
                num_invalid = int(row[-2].value)
                num_novote = int(row[-1].value)
                c.execute(f'insert into area3 values ({area3_uid}, "{area3}", {area2_uid}, {num_people}, {num_vote}, {num_invalid}, {num_novote})')
            area4 = row[1].value
            if area4 == '소계':
                continue
            if area4 == '관내사전투표':
                area4 = 'prevote_in'
            if engflag == 'eng':
                area4 = get_eng(area4)
            area4_uid = get_uid()
            num_people = int(row[2].value)
            num_vote = int(row[3].value)
            num_invalid = int(row[-2].value)
            num_novote = int(row[-1].value)
            c.execute(f'insert into area4 values ({area4_uid}, "{area4}", {area3_uid}, {num_people}, {num_vote}, {num_invalid}, {num_novote})')
            for i in range(len(candidates_t)):
                candidate_uid = candidate_uids[i]
                c.execute(f'insert into vote values ({candidate_uid}, {area4_uid}, {int(row[i + 4].value)})')
        db.commit()
