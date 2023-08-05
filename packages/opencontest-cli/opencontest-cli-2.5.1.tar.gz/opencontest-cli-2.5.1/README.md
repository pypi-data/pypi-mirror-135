# OpenContest CLI

A very simple [OpenContest](https://github.com/LadueCS/OpenContest) command line client written in Python and [requests](https://docs.python-requests.org/en/master/index.html).

## Usage

Install this client using `pip`:
```
pip install opencontest-cli
```

Register an account on an OpenContest server:
```
occ register -s homeserver.com -N name -E email -U username -P password
```

Save username, homeserver (the server you registered your account on), and password to disk:
```
occ save -U username -H homeserver.com -P pasword
```

Get information about an OpenContest server:
```
occ about -s server.com
```

Get information about a contest:
```
occ info -s server.com -c contest
```

View the number of solves of each problem:
```
occ solves -s server.com -c contest
```

View the submission history of all users in a contest:
```
occ history -s server.com -c contest
```

Download problem statement:
```
occ problems -s server.com -c contest -p problem
```

Submit code:
```
occ submit -s server.com -c contest -p problem -c code_file
```

Check user status:
```
occ status -s server.com -c contest
```

Query your contest submission history:
```
occ submissions -s server.com -c contest
```

Get code for a specific submission number:
```
occ code -s server.com -c contest -n submission_number
```
