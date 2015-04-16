#README.txt

----------------
Regarding Alias
----------------
1) Have added alias alias create='bash ../shell/create.sh'
2) syntax to add: alias alias_name='the command'
3) To check the alias type create
4) Reference link: http://www.mediacollege.com/linux/command/alias.html


-----------------------------------------------------
Regarding ^M and \r is found at the end of each line
-----------------------------------------------------
1) To view the ^M or \r use the cmd: head myScript.sh | cat -vet
2) To remove the problem, sed -i 's/\r$//' myScript.sh

------------------------------------------------------
Regarding creating util commands in workspace
------------------------------------------------------

-----------------------------------------------------------
Regarding fixing \r issues that is getting appened to files
-----------------------------------------------------------
