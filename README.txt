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
1) First copy the util file to $PATH directory.{Any}
2) Goto the path and create a symbolic link
ln -s {/path/to/file-name} {link-name}

-----------------------------------------------------------
Regarding fixing \r issues that is getting appened to files
-----------------------------------------------------------
1) Github suggests that you should only use \n as new line char.
2) Looks like you have to set config git config --global core.autocrlf true
3) Also use, git rm --cached -r .
4) Test this and if valid remove clean.sh script from env



-----------------------------------------------------------
11. To undo a working copy modifications of one file in git.
-----------------------------------------------------------
1) git checkout -- file
2) Reference link: http://stackoverflow.com/questions/692246/undo-working-copy-modifications-of-one-file-in-git

