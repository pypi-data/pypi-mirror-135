=====
fishwxnotifys
=====

fishwxnotifys is a Django app to send wechat notify. For each question,
visitors can choose between a fixed number of answers.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "polls" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'fishwxnotifys',
    ]

2. Configure the APPID & APP_SECRET::

    in settings.py
    APPID = "xxx"
    APP_SECRET= "xxx"

3. Use send_message in your django app
   from fishwxnotifys import send_message
   send_message.delay(message=dict_msg)
