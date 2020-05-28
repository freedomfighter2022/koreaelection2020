# Data for investigation on the general election of Korea in 2020

Updated 2020/05/28: Added constituency data to the 20th regional election sqlite files (korea_election_regional_20_kor.sqlite and korea_election_regional_20_eng.sqlite). The source of constituency-voting district mapping was the National Election Committee (https://www.nec.go.kr/portal/bbs/view/B0000338/32767.do).

Update 2020/05/26: Added makedb_21_regional.py, which is a script to make korea_election_regional_21_[kor/eng].sqlite. Usage is in the script.

Update 2020/05/17: Updated korea_election_regional_20_(kor/eng).sqlite files have been updated with correct num_invalid and num_novote. Also, independent candidates were assigned to separate independent parties (musosog1, musosog2, and etc) in this update. Also, updated proportional election data for the 20th and 21st with the fix on num_invalid and num_novote and using the latest data from the NEC.

Update: korea_election_regional_21_(kor/eng).sqlite files have been updated with correct num_invalid and num_novote. Also, independent candidates were assigned to separate independent parties (musosog1, musosog2, and etc) in this update.

Update: \*_regional_*.sqlite files have been updated with the latest data from the National Election Commission of Korea as of 2020/04/29.

A general election was held in South Korea on April 15, 2020. There has been the suspicion that this year's election was rigged. For the researchers and investigators who are interested in looking into this question, sqlite3 databases of the current and previous general elections of Korea are released.

There are 4 database files in this repository:

* korea_election_regional_20_eng.sqlite: South Korea 20th general election for regional representatives on April 13, 2016
* korea_election_regional_21_eng.sqlite: South Korea 21th general election for regional representatives on April 15, 2020
* korea_election_proportional_20_eng.sqlite: South Korea 20th general election for proportional representatives on April 13, 2016
* korea_election_proportional_21_eng.zip: South Korea 21th general election for proportional representatives on April 15, 2020 (decompress to get .sqlite file)

In the 20th and the 21st elections, every voter cast one vote for a "regional" representative and another vote for a political party. A regional representative was elected in each election district based on the sum of the first vote. The second vote was tallied nationwide by political parties and a fixed number of "proportional" representative seats were divided and given to each political party according to their proportion of the second votes.

The regional and proportional votes in the 20th election and the regional votes in the 21st election were counted electronically. The proportional votes in the 21st one were counted by humans.

The four databases have the same architecture. Below are the tables in each db.

* area1: provincial level
  (uid int, name text)

* area2: election district level
  (uid int, name text, area1 int)
  `area1` is `uid` in `area1` table.

* area3: sub-election district level
  (uid int, name text, area2 int, sum_people int, sum_vote int, sum_invalid int, sum_novote int)
  `area2` is `uid` in `area2` table.
  `sum_people` is the number of eligible voters.
  `sum_vote` is the number of valid votes.
  `sum_invalid` is the number of invalid votes.
  `sum_novotes` is the number of the people who did not vote.
  Special names:
    `disabled_ship` is the voters in ships or disabled.
    `prevote_out` is the voters who live outside of their election district and voted before the election day.
    `abroad` is the voters who live and voted outside Korea.
    `abroad_office` is the voters who live in abroad Korean foreign offices and voted outside of Korea.
    (`abroad_office` exists only in the 21st election data.)

* area4: voting post level
  (uid int, name text, area3 int, sum_people int, sum_vote int, sum_invalid int, sum_novote int)
  `area3` is `uid` in `area3` table.
  `sum_people` is the number of eligible voters.
  `sum_vote` is the number of valid votes.
  `sum_invalid` is the number of invalid votes.
  `sum_novotes` is the number of the people who did not vote.
  Special names:
    `prevote_in` in the voters who live in their election district and voted before the election day.

* party: political parties
  (uid int, name text)

* candidate: candidates
  (uid int, name text, party int)
  `party` is `uid` in `party` table.
  This table exists only in regional election data.

* vote: votes
  (candidate int, area int, vote int) in regional election data
  (party int, area int, vote int) in proportional election data
  The number of votes for a given candidate in a given area.
  `candidate` is `uid` of `candidate` table.
  `party` is `uid` of `party` table.
  `area` is `uid` of either `area3` or `area4` table.

There also is one compressed file, korea_election_20_and_21_regional_and_proportional_txt_eng.zip, which has the following 4 flat files:

* korea_election_regional_20_eng.txt: South Korea 20th general election for regional representatives on April 13, 2016
* korea_election_regional_21_eng.txt: South Korea 21th general election for regional representatives on April 15, 2020
* korea_election_proportional_20_eng.txt: South Korea 20th general election for proportional representatives on April 13, 2016
* korea_election_proportional_21_eng.txt: South Korea 21th general election for proportional representatives on April 15, 2020

The flat files have the following columns:

area1 | area2 | area3 | area4 | party | candidate (regional files only) | vote

Note on pre-voting: In both the 21st and the 20th general elections of Korea, 'pre-voting' was done, which is to vote before the election day. The total number of votes for a candidate is calculated by adding the votes for him/her from pre-voting and those from the election day. In the 21st general election of Korea for example, pre-voting was done on April 10th and 11th, 2020 and the election day was April 15, 2020. There is the suspicion that the result of pre-voting might have been rigged in the 21st election but not in the 20th one. `prevote_in` in `area4` table and 'prevote_out` in `area3` table record the votes cast by pre-voting.

Note on summing the votes for each candidate: Some votes are recorded in area3-level and some in area4-level, which is due to the fact that voting by disabled voters, voting from ships, out-of-town pre-voting, and voting-from-abroad cannot have area4-level granularity. `vote` table has votes from both these area3-level voting posts and area4-level voting posts.

Korean people are finding suspicious statistics from this data, but claims by Korean people on Korean election data can be painted as partisan. Thus, we are seeking the international community of statisticians, election fraud investigators, and data scientists to provide objective opinions.

Please leave any bug report at https://github.com/freedomfighter2022/koreaelection2020/issues.

Below is for Korean speakers.

# 20대와 21대 대한민국 총선 데이터베이스

지역구와 비례대표 선거 결과를 각각 데이터베이스화 하였습니다.

* 21대 지역구: korea_election_regional_21_kor.sqlite
* 20대 지역구: korea_election_regional_20_kor.sqlite
* 21대 비례대표: korea_election_proportional_21_kor.zip (압축을 푸십시오)
* 20대 비례대표: korea_election_proportional_20_kor.sqlite

데이터베이스의 구조는 위의 영문 설명을 참조해 주십시오.

텍스트 파일로 된 자료는 korea_election_20_and_21_regional_and_proportional_txt_kor.zip 에 들어 있습니다. 이 파일에는 아래의 4개 파일이 들어 있습니다.

* korea_election_regional_20_kor.txt: 20대 지역구
* korea_election_regional_21_kor.txt: 21대 지역구
* korea_election_proportional_20_kor.txt: 20대 비례대표
* korea_election_proportional_21_kor.txt: 21대 비례대표

위의 텍스트 파일들에는 아래의 컬럼들이 있습니다.

시/도 | 구/군 | 동/면 | 투표소 | 당 | 후보 (지역구 파일에만 존재) | 득표수
