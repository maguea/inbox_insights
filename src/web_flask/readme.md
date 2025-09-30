# Getting Started
the instructions should be in the root [README.md](../../README.md). You should have venv working and installed flask with `pip install flask`.

**weird error**: you need to change line 6 of email_scraper.py to get it to work. change it to this `from .email_consts import EMAIL_CONST`
# File
## '/'
the goal is to have a landing page that will check connection to the list of emails. it should be a simple green check status for connected, 3 moving dots for trying, or red check for failed.
 - failed, go to settings
 - success, go to dashbaord

## '/settings'
settings should have a list configurable options, with the top of it the email status and add new email

i may rename this to `'config'`

## 'dashboard'
this will have maybe 3 options. recommendations of emails sent in the last day, week, 30months. the **default** will be a week

## 'history'
this one hasnt been decided in terms of layout. the function will be showing all emails stored in the database. not sure how the db will work, but maybe load 50 emails at a time, from newest to oldest.

functions that can affect the algorithm (**MAYBE**???)

- delete
- ignore
- favorite

i would like to copy either the google or outlook style. either a compact list of emails where if you select you get a focused view or a side bar with emails listed and the email's message
# Assets
## Bootstrap Template
Use the [docs](https://getbootstrap.com/docs/5.3/getting-started/introduction/) to figure out classname and usage

## Icons
you can search for Bootstrap icons [here](https://icons.getbootstrap.com/) and use like so `<i class="bi-search"></i>`

# References
favicon from [here](https://www.favicon.cc/?action=icon&file_id=980768)