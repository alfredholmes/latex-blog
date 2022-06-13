# LaTeX Blog
If you find this project useful, please consider supporting me on [Ko-fi](https://ko-fi.com/holmes).

Blogging website written in Django the renders LaTeX blog posts to html. Posts are written in LaTeX and rendered using make4ht to HTML which is then used to display the posts. Is the code that is used on [my blog](https://alfredholmes.uk).

To run, it is expected that the computer is running Linux with make4ht installed. See the post [How to blog with Latex](https://alfredholmes.uk/posts/how-to-latex-blog) for detailed instructions.

Quick how to run (Linux or macOS), assuming make4ht is installed and can be run in the command line with `make4ht`:

```
git clone https://github.com/alfredholmes/django-latex-blog
cd django-latex-blog

virtualenv venv
source venv/bin/activate
(venv) pip install -r requirements.txt

(venv) python manage.py

```
Then you should see the site if you navigate to `localhost:8000`.

To run on Windows, or with different HTML rendering software, you'll need to change the models in posts/models.py so that make4ht or you chosen renderer can be run. If you have some other software that takes a file and renders HTML then the code could be easily modified to render in this way instead of using LaTeX.

To deploy the site you can do two things. If you run

```
mkdir static-html
cd static-html
wget --mirror --convert-links localhost:8000
```
Will create a static HTML version of the site in the folder `static-html`. This can then be uplocaded to any static HTML hosting that you have, for example a department website. The advantage to this is that this hosting is often cheap or even free.

The other option is to run the site on a cloud server that runs django. This is a bit difficult to set up, but details can be found [here](https://alfredholmes.uk/posts/how-to-latex-blog). Annoyingly you'll most likely have to manage your own server because the server needs to have LaTeX installed. If you find a hosting site that allows managed Django with the ability to install command line applications, please let me know.


