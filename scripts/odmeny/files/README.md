
Použití: byro-odmeny [-n|-f|-a] [-u USER] [-t TIME] [-wd NUM] [--all]

Normal use:

1. byro-odmeny -n -t 2015-08 -wd 21 --all
2. fill in missing values (money for tasks and sanctions)
3. byro-odmeny -f --all
4. byro-odmeny -a

Switches:

-n     create new file
-f     calculate the missing sums
-a     output simple accounting data

-u     filter by user id in redmine
-t     filter by month in YYYY-MM
-wd    number of working days
--all  apply to all users

Author: Jakub Michálek, Česká pirátská strana
License: GNU GPL v3
