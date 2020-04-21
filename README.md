# Data for investigation on the general election of Korea in 2020

A general election was held in South Korea on April 15, 2020. There has been the suspicion that the election was rigged. For the researchers and investigators who are interested in looking into this question, a sqlite3 database of the election is released. For comparison, the same kind of database for the previous general election in South Korea in 2016 is released also.

There are two database files in this repository:

* South Korea 21th general election on April 15, 2020: korea_election_regional_21_eng.sqlite
* South Korea 20th general election on April 13, 2016: korea_election_regional_20_eng.sqlite

The schema of the two databases is the same. Below are the tables in each db.

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
    (`abroad_office` exists only is korea_election_regional_21_end.sqlite.)

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

* vote: votes
  (candidate int, area int, vote int)
  The number of votes for a given candidate in a given area.
  `candidate` is `uid` of `candidate` table.
  `area` is `uid` of either `area3` or `area4` table.

Note on pre-voting: In both the 21st and the 20th general elections of Korea, 'pre-voting' was done, which is to vote before the election day. The total number of votes are calculated by adding the votes from pre-voting and the votes from the election day. In the 21st general election of Korea for example, pre-voting was done on April 10th and 11th, 2020 and the election day was April 15, 2020. There is the suspicion that the result of pre-voting might have been rigged in the 21st election but not in the 20th one. `prevote_in` in `area4` table and 'prevote_out` in `area3` table record the votes cast by pre-voting.

Note on summing the votes for each candidate: Some votes are recorded in area3-level and some in area4-level, which is due to the fact that voting by disabled voters, voting from ships, out-of-town pre-voting, and voting-from-abroad cannot have area4-level granularity. `vote` table has votes from both these area3-level voting posts and area4-level voting posts.

Korean people are finding suspicious statistics from this data, but claims by Korean people on Korean election data can be painted as partisan. Thus, we are seeking the international community of statisticians, election fraud investigators, and data scientists to provide objective opinions.
