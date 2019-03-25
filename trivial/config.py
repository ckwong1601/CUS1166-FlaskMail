import os
class Config(object):
    DEBUG = True

    MAIL_SERVER = 'smtp.gmail.com' # name of the email server (Outlook is smtp.office365.com)
    MAIL_PORT = 465 # port of server (Outlook is 587)
    # MAIL_USE_TSL = True for more encryption
    MAIL_USE_SSL = True # enable SSL encryption
    MAIL_USERNAME = os.environ.get('FLASKEMAIL') # username of sender
    MAIL_PASSWORD = os.environ.get('FLASKPASSWORD') # password of sender
    #MAIL_DEFAULT_SENDER
    #MAIL_MAX_EMAILS
    #MAIL_SUPPRESS_SEND
    #MAIL_ASCII_ATTACHMENTS
