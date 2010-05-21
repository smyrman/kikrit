1 INSTALLATION (Stand-alone client setup):
  (New installation instructions expected for v0.3)

 a) Download and unzip the latest version from the 'downloads tab'. Move the
    folder to somwhere on your harddrive, e.g to /home/user/kikrit.

 b) Edit settings/production.py to your liking. That includes in particular
    the database. The other settings can wait.

 c) Start the client with '$ python start_kikrit.py' (or just click on the
    file). You will now get a first-run dialog that will help you create the
    database.

 d) Create a super user by issuing:
    $ python django_kikrit/manage.py createsuperuser

2 UPGRADING(Stand-alone client setup):
  (New upgrading instructions expected for v0.3)

  a) Rename the folder where you keep the old KiKrit installation to something
     like 'kikrit_old'

  b) Follow step a,b and c in section 1. In the first-run dialog that shows
     up, chose to import database from previos installation.


3 ADMINISTRATIVE USAGE:
 a) Start the clinet with 'python start_kikrit.py'

 b) Click on the 'Admin' tab, and log in with the super user account you
 created in step d, section 1.

 c) Add users, accounts and merchandise to your liking.


4 INSTALLATION (Server/clinet setup)
  Explanations for how to achive this setup will be added after the v0.3
  release.
