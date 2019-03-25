# Setup
### Environmental Variables
If you are running this outside of a virtual environment, set the environmental variables `FLASKEMAIL` and `FLASKPASSWORD` to the email and password that you wish to send emails from. You can do this from python shell:
```
import os
os.environ['FLASKEMAIL'] = "your@email.com"
os.environ['FLASKPASSWORD'] = "yourPassword123"
```

If you are running this through pipenv, create a file called `.env` in the root directory. It should contain:
```
FLASKEMAIL=your@email.com
FLASKPASSWORD=yourPassword123
```

If you are not using Gmail as your SMTP server, you will have to change the `config.py` file and change the `MAIL_SERVER`.