from datetime import datetime
import re
from typing import List, Dict, Tuple


def from_innings(
    inngs: str,
) -> Tuple[Dict[str, List], Dict[str, List], List[int], List[str], Dict[str, int], int]:
    # initialized a tuple that will store all the below given datas
    bowlers: Dict[str, List] = {}
    # dictionary of batsmen
    batsman: Dict[str, List] = {}
    # dictionary of bowlers
    totalscore: List[int] = [0, 0]
    # innigs score list 
    fall_of_wickets: List[str] = []
    # list to store the balls at which wickets fell
    extras: Dict[str, int] = {
        # dictionary to store the extra runs
        "wides": 0,
        "byes": 0,
        "leg byes": 0,
        "no_balls": 0,
        "penalty": 0,
    }
    runs06 = 0
    # runs scored in totalovers 0-6
    valid_balls = 0
    with open(inngs) as file1:
        for line in file1.readlines():
            if line == "\n":
                continue
            over, context = re.split(r"\s", line, 1)
            over = list(map(int, over.split(".")))
            bowler_to_batter, result = re.split(r", ", context, 1)
            result, context = re.split(
                r"!" if result.startswith("out") else r", ", result, 1
            )
            bowler, batter = re.split(" to ", bowler_to_batter, 1)

            if bowlers.get(bowler) is None:
                # balls, maidens, runs, wickets, no balls, wides
                bowlers[bowler] = [0, 0, 0, 0, 0, 0]

            if batsman.get(batter) is None:
                # status, runs, balls, fours, sixes
                batsman[batter] = ["not out", 0, 0, 0, 0]

            bowlers[bowler][0] += 1
            batsman[batter][2] += 1
            valid_balls += 1
            # valid bowled

            if result.startswith("out "):
                # out condition
                totalscore[1] += 1
                bowlers[bowler][3] += 1
                _, result = re.split("out ", result, 1)
                status: str = ""
                if result == "Bowled":
                    status = f"b {bowler}"
                elif result == "Lbw":
                    status = f"lbw b {bowler}"
                else:
                    catcher = re.sub("Caught by ", "", result)
                    status = f"c {catcher} b {bowler}"

                batsman[batter][0] = status
                fall_of_wickets.append(
                    f"{totalscore[0]}-{totalscore[1]} ({batter}, {over[0]}.{over[1]})"
                )

            elif re.match(r"(\d )?wides?", result):
                runs = 1 if result == "wide" else int(result[0])
                totalscore[0] += runs
                bowlers[bowler][3] += runs
                bowlers[bowler][-1] += runs
                extras["wides"] += runs
                bowlers[bowler][0] -= 1
                batsman[batter][2] -= 1
                valid_balls -= 1
            elif re.match(r"(leg )?byes", result):
                bye_data, _ = re.split(r", ", context, 1)
                runs = 0
                if re.match(r"(no|(\d)?) runs?", bye_data) and not bye_data.startswith(
                    "no "
                ):
                    runs = int(bye_data[0])
                elif bye_data == "FOUR":
                    runs = 4
                elif bye_data == "SIX":
                    runs = 6
                extras[result] += runs
                totalscore[0] += runs

            elif re.match(r"(no|(\d)?) runs?", result):
                if not result.startswith("no"):
                    runs = int(result[0])
                    totalscore[0] += runs
                    bowlers[bowler][2] += runs
                    batsman[batter][1] += runs
            elif result == "FOUR":
                totalscore[0] += 4
                bowlers[bowler][2] += 4
                batsman[batter][1] += 4
                batsman[batter][-2] += 1
            elif result == "SIX":
                totalscore[0] += 6
                bowlers[bowler][2] += 6
                batsman[batter][1] += 6
                batsman[batter][-1] += 1
            else:
                print(f"{over}# {bowler} -> {batter}: {result}")
        
            if valid_balls == 36:
                runs06 = i
                # runs scored in totalovers 0-6

    return (batsman, bowlers, totalscore, fall_of_wickets, extras, runs06)


def blanks(x: int) -> str:
    # for blanks
    return " " * x


def totalovers(x: int) -> str:
    return f"{x // 6}{f'.{x % 6}' if x % 6 > 0 else ''}"


def string_temp(extras: Dict[str, int]) -> str:
    return f"{sum(extras.values())} (b {extras['byes']}, lb {extras['leg byes']}, w {extras['wides']}, nb {extras['no_balls']}, p {extras['penalty']})"


def teamName(stringtemp):
    # for getting team name
    ans = ""
    for i in stringtemp:
        if i == ':':
            break
        ans+=i
    ansf = ans[:-13]
    return ansf
           

teams = open("teams.txt", 'r')

teamlist = teams.readlines()

for i in teamlist:
    if(i=='\n'):
        teamlist.remove(i)

for i in range(len(teamlist)):
    if(teamlist[i].endswith('\n')):
        teamlist[i]=teamlist[i][:-1]

teamlist.pop(-1)

team1name = teamName(teamlist[0])
team2name = teamName(teamlist[1])

def fun2write(batsman, bowlers, totalscore, fall_of_wickets, extras, runs06, outfile, teamname):
    # function to write the innings score in the final txt file
    with open(outfile, "a") as f:
        f.writelines(
            [
                f"{teamname} Innings\n\n\n"
                f"BATTER{blanks(54)}R{blanks(4)}B{blanks(4)}4s{blanks(3)}6s{blanks(3)}SR\n\n",
                "\n".join(
                    [
                        f"{batter: <20}{data[0]: <40}{data[1]: <5}{data[2]: <5}{data[3]: <5}{data[4]: <5}{round(data[1] * 100 / data[2], 2)}"
                        for batter, data in batsman.items()
                    ]
                ),
                f"\n\nEXTRAS: {string_temp(extras)}\n",
                f"INNINGS SCORE: {totalscore[0]}-{totalscore[1]} ({totalovers(sum([x[0] for x in bowlers.values()]))} Ov)",
                "\n\nFALL OF WICKETS: \n",
                ", ".join(fall_of_wickets),
                f"\n\nBOWLER{blanks(14)}O{blanks(4)}M{blanks(4)}R{blanks(4)}W{blanks(4)}NB{blanks(3)}WD{blanks(3)}ECO\n\n",
                "\n".join(
                    [
                        f"{bowler: <20}{totalovers(data[0]): <5}{data[1]: <5}{data[2]: <5}{data[3]: <5}{data[4]: <5}{data[5]: <5}{round(data[2] * 6 / data[0], 2)}"
                        for bowler, data in bowlers.items()
                    ]
                ),
                f"\n\nPOWERPLAYS{blanks(10)}totalovers{blanks(10)}Runs\n",
                f"Mandatory{blanks(11)}0.1-6{blanks(15)}{runs06}",
                "\n\n",
                f"*"*600,
                "\n\n"
            ]
        )


def final(teams_file: str, first: str, second: str, outfile: str):
    # final function to implement the whole code
    teams = open(teams_file, 'r')
    teamlist = teams.readlines()
    for i in teamlist:
        if(i=='\n'):
            teamlist.remove(i)
    for i in range(len(teamlist)):
        if(teamlist[i].endswith('\n')):
            teamlist[i]=teamlist[i][:-1]
    
    teamlist.pop(-1)
    teams = {}
    indexofcol1 = teamlist[0].rfind(':')
    indexofcol1+=2
    team1temp = teamlist[0][indexofcol1:]
    indexofcol2 = teamlist[1].rfind(':')
    indexofcol2+=2
    team2temp = teamlist[1][indexofcol2:]
    teams[team1name] = team1temp.split(", ")
    teams[team2name] = team2temp.split(", ")
    
    
    # clear the file
    with open(outfile, "w") as filenew:
        filenew.write("")

    fun2write(*from_innings(first), outfile, team1name)
    fun2write(*from_innings(second), outfile, team2name)


if __name__ == "__main__":
    start_time = datetime.now()

    final("teams.txt", "pak_inns1.txt", "india_inns2.txt", "Scorecard.txt")
    # implementing the code, with given files

    end_time = datetime.now()
    print("Duration of Program Execution: {}".format(end_time - start_time))