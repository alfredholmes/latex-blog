# LaTeX Blog


Blogging website written in Django the renders LaTeX blog posts to html. Posts are written in LaTeX and rendered using make4ht to HTML which is then used to display the posts. Is the code that is used on [my blog](https://alfredholmes.uk).

To run, it is expected that the computer is running Linux with make4ht installed.

Quick how to run (Linux or macOS), assuming make4ht is installed and can be run in the command line with `make4ht`:

```
git clone https://github.com/alfredholmes/django-latex-blog
cd django-latex-blog


cp blog/settings_local_template.py blog/settings.py

virtualenv venv
source venv/bin/activate
(venv) pip install -r requirements.txt

```
Now create your own a secret key using the command

```
(venv) python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
and set the `SECRET_KEY` variable in `blog/settings.py` equal to the output of this. Now run

```
(venv) ./manage.py makemigrations posts
(venv) ./manage.py migrate
(venv) ./manage.py createsuperuser
```
and fill in some details for admin account to access the admin part of the site. Now run
```
(venv) ./manage.py runserver
```
If you navigate to `localhost:8000` you should see an empty version of the site running. Navigating to `loaclhost:8000/admin` and logging in with the account details you made will allow you to edit the site. For example, to start you may want to add a title element, which will add a heading to the site. 



To run on Windows, or with different HTML rendering software, you'll need to change the models in posts/models.py so that make4ht or you chosen renderer can be run. If you have some other software that takes a file and renders HTML then the code could be easily modified to render in this way instead of using LaTeX.

To deploy the site you can do two things. If you run

```
mkdir static-html
cd static-html
wget --mirror --convert-links localhost:8000
```
this will create a static HTML version of the site in the folder `static-html`. This can then be uplocaded to any static HTML hosting that you have, for example a department website. The advantage to this is that this hosting is often cheap or even free.

The other option is to run the site on a cloud server that runs django. This is a bit difficult to set up. Annoyingly you'll most likely have to manage your own server because the server needs to have LaTeX installed. If you find a hosting site that allows managed Django with the ability to install command line applications, please let me know.


