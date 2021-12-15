<!-- PROJECT SHIELDS -->
![](https://img.shields.io/github/contributors/sa-y-an/rportal1)
&nbsp;&nbsp;&nbsp;&nbsp;
![](https://img.shields.io/github/forks/sa-y-an/rportal1)
&nbsp;&nbsp;&nbsp;&nbsp;
![](https://img.shields.io/github/stars/sa-y-an/rportal1)
&nbsp;&nbsp;&nbsp;&nbsp;
![](https://img.shields.io/github/issues-pr-closed-raw/sa-y-an/rportal1)
&nbsp;&nbsp;&nbsp;&nbsp;
![](https://img.shields.io/github/issues/sa-y-an/rportal1)


# Research Portal Backend


<!-- GETTING STARTED -->
## Getting Started

<!--Installation-->
### Installation:
### For Windows

Add the following to requirements.txt (only for windows)
```
pip install python-magic-bin
```
### For Linux/Debian
```
sudo apt-get install libmagic1
```


Install virtualenvironment (if not already)
```
pip install virtualenv
virtualenv myenv
```

Activate virtualenv
```
myenv\scripts\activate
```

> PS : Linux Users follow different guidelines 
> For further details refer <a href="https://www.geeksforgeeks.org/creating-python-virtual-environment-windows-linux/">https://www.geeksforgeeks.org/creating-python-virtual-environment-windows-linux/</a>


Django Installation ( Developer Mode )
```
pip install -r requirements.txt
python local.py makemigrations
python local.py migrate
python local.py runserver
```

<!--Setup-->
### Setup Guidelines:
- After sucessfull installation create a .env in the directory where settings.py is located following the structure of .env.example file



<!--Contribution Guidelines-->
## Contribution Guidelines 

Before making a migration run 
```
python local.py makemigrations --dry-run --verbosity 3
```
to make sure if it breaks any thing

- Fork this Repo
- Create a branch in the forked repo 
```
git checkout -b develop
```
- Make Changes 
- Push to your repo & make a pull request

> PS 3 : Instructions to update git forked repo <a href="https://medium.com/@topspinj/how-to-git-rebase-into-a-forked-repo-c9f05e821c8a"> Medium </a>

<br>

<!--Contacts-->
## Contacts
<br>

> Website : &nbsp;&nbsp;&nbsp; <a href="https://www.ieeesbnitdgp.com/"> https://www.ieeesbnitdgp.com/</a><br>
>Github :  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <a href="https://github.com/ieeesb-nitdgp">https://github.com/ieeesb-nitdgp</a>

<br>

<!--Rp backend Contributors-->
## Contributors

<table>
<tr>
<td align="center"><img src="https://avatars.githubusercontent.com/u/55195504?v=4" width="100px;" alt=""/><br /><sub><a href="https://github.com/sa-y-an"><b>Sayan Mondal</b></a></sub></td>
<td align="center"><img src="https://avatars.githubusercontent.com/u/26196922?v=4" width="100px;" alt=""/><br /><sub><a href="https://github.com/arin17bishwa"><b>Bishwajit Ghosh</b></a></sub></td>
<td align="center"><img src="https://avatars.githubusercontent.com/u/74106901?v=4" width="100px;" alt=""/><br /><sub><a href="https://github.com/durbar2003"><b>Durbar Chakrabarty</b></a></sub></td>
<td align="center"><img src="https://avatars.githubusercontent.com/u/77785024?v=4" width="100px;" alt=""/><br /><sub><a href="https://github.com/Sreemoyee26"><b>Sreemoyee Sadhukhan</b></a></sub></td>
<td align="center"><img src="https://avatars.githubusercontent.com/u/77566807?v=4" width="100px;" alt=""/><br /><sub><a href="https://github.com/NaveenS143"><b>Naveen Leo</b></a></sub></td>
</tr>
</table>

<br>

> For any suggestions, create an issue or start a discussion in the discussion tab.

