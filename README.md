# RP draft

##Installation Guidelines


### For Windows

Install virtualenvironment (if not already)
```
pip install virtualenv
virtualenv myenv
```

Activate virtualenv
```
myenv/scripts/activate
```

> PS : Linux Users follow different guidelines 
> For further details refer <a href="https://www.geeksforgeeks.org/creating-python-virtual-environment-windows-linux/">https://www.geeksforgeeks.org/creating-python-virtual-environment-windows-linux/</a>


Django Installation
```
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

> Navigate to localhost:8000 to see the magic
