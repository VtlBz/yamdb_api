"""
Configuration for data import script from csv-file to DB.

Specify in first position in IMPORT_CONFIG the filename,
import that shall be done. In second position - the name of application
and model which you want to fill with data.
Specify like the <app_name.Model_name>, in an order that respects
foreign key dependencies.
For Many-to-Many relation table set the flag '1' to third position
and specify model name like the
<app_name>.<first_Model_name>_<second_Model_name>

Run script:
manage.py csvtodb -p <path to folder with tables>

Argument '-p' ('--path') is optional, you can use constant DEFAULT_PATH
"""

# Correlation table <file_name.csv> -- > <app_name>.<Model_name>
IMPORT_CONFIG: tuple = (
    ('yamdbuser.csv', 'users.YamdbUser', 0),
    ('categories.csv', 'reviews.Category', 0,),
    ('genres.csv', 'reviews.Genre', 0,),
    ('titles.csv', 'reviews.Title', 0,),
    ('titles_genres.csv', 'reviews.Title_Genre', 1,),
    ('reviews.csv', 'reviews.Review', 0,),
    ('comments.csv', 'reviews.Comment', 0,),
)

DEFAULT_PATH = ''
