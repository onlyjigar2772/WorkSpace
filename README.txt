#README.txt

-----------------------------------------------------
1. Unable to execute PERL script. Unable to initialize device PRN "$ ./helloWorld.pl"
-----------------------------------------------------
1) You forgot the "she-bang" line.
2) http://stackoverflow.com/questions/6168604/unable-to-initialize-device-prn-message-upon-executing-rb-script-in-cygwin
3) Tag(s) - perl

-----------------------------------------------------
2. Help in installing cygwin packages, here django
-----------------------------------------------------
1) Reference link: 
http://blog.adlibre.org/2011/01/11/how-to-install-and-setup-a-python-django-development-environment-on-windows-7/
2) Tag(s) - django, cygwin

-----------------------------------------------------
3. To bypass proxy and access hub, you need to set up http.config in git.
-----------------------------------------------------
1) Reference link: http://stackoverflow.com/questions/496277/git-error-fatal-unable-to-connect-a-socket-invalid-argument
2) Tag(s) - proxy, django

-----------------------------------------------------
4. Setting the env varibale in windows
-----------------------------------------------------
1) Goto my comp, right click properties, advance, env variable. append to the variable the path
2) Tag(s) - desktop, script

-----------------------------------------------------
5. In wipro, due to admin we will have to made the following change to the setting.py in the mysite folder to avoid lockdown
-----------------------------------------------------
1) Referece link: http://stackoverflow.com/questions/6554528/help-with-error-no-module-named-polls-from-the-django-project-tutorial-1
2) 
INSTALLED_APPS = (
#'django.contrib.admin',
'django.contrib.auth',
'django.contrib.contenttypes',
'django.contrib.sessions',
'django.contrib.sites',
'django.contrib.messages',
'django.contrib.staticfiles',
'polls'
)
3) Tag(s) - django

-----------------------------------------------------
6. To check if a particular perl module is installed in PERL, we can also visit /usr/bin/perl/.
-----------------------------------------------------
1) perldoc -l XML::Simple
2) Tag(s) - perl

-----------------------------------------------------
7. Regarding Alias
-----------------------------------------------------
1) Have added alias alias create='bash ../shell/create.sh'
2) syntax to add: alias alias_name='the command'
3) To check the alias type create
4) Reference link: http://www.mediacollege.com/linux/command/alias.html
5) Tag(s) - Unix, script

-----------------------------------------------------
8. Regarding ^M and \r is found at the end of each line
-----------------------------------------------------
1) To view the ^M or \r use the cmd: head myScript.sh | cat -vet
2) To remove the problem, sed -i 's/\r$//' myScript.sh
3) Tag(s) - Unix, script

------------------------------------------------------
9. Regarding creating util commands in workspace
------------------------------------------------------
1) First copy the util file to $PATH directory.{Any}
2) Goto the path and create a symbolic link
ln -s {/path/to/file-name} {link-name}
3) Tag(s) - Unix

-----------------------------------------------------------
10. Regarding fixing \r issues that is getting appened to files
-----------------------------------------------------------
1) Github suggests that you should only use \n as new line char.
2) Looks like you have to set config git config --global core.autocrlf true
3) Also use, git rm --cached -r .
4) Test this and if valid remove clean.sh script from env
5) Tag(s) - git

-----------------------------------------------------------
11. To undo a working copy modifications of one file in git.
-----------------------------------------------------------
1) git checkout -- file
2) Reference link: http://stackoverflow.com/questions/692246/undo-working-copy-modifications-of-one-file-in-git
3) Tag(s) - git

-----------------------------------------------------------
12. How do I add a multi-line comment to Perl source code?
-----------------------------------------------------------

1) simply do =head ##your code to comment =cut
2) Reference Link: http://stackoverflow.com/questions/3828205/how-do-i-enter-a-multi-line-comment-in-perl
3) Tag(s) - perl

-----------------------------------------------------------
13. Commands to check the Linux Version, Release name and Kernel version.
-----------------------------------------------------------

1) uname -a
2) Reference Link: http://www.symantec.com/connect/articles/commands-check-linux-version-release-name-kernel-version
3) Tag(s) - Unix, Linux

-----------------------------------------------------------
14. Command to naviagte to other driver in DOS.
-----------------------------------------------------------

1) You do not need to cd d:\ just enter d:. CD stands for change directory, which is not what you want to do.
2) Reference Link: 
http://superuser.com/questions/302505/cmd-cd-to-other-drives-except-c-not-working
3) Tag(s) - Windows

-----------------------------------------------------------
15. Shortcuts to launch the terminal in Ubuntu
-----------------------------------------------------------

1) Applications menu -> Accessories -> Terminal. Keyboard Shortcut: Ctrl + Alt + T
2) Tag(s) - Ubuntu

-----------------------------------------------------------
16. How to find a file in a directory in unix
-----------------------------------------------------------
1) cmd - find foldername -name filename E.g - find . -name env_check.py
2) Tag(s) - Unix
