# MailUtility

A package containing a tool to send mail and a tool to monitor a mailbox easily.
Supports remote directories with transparentpath.

## Installation

`pip install mailutility`

## MailSender

Utils to send mails, supports attaching files. Only compatible with an sending account that does not use a
double authentification method.

## Usage

```python
from mailutility import MailSender
from transparentpath import TransparentPath as Tp
some_directory_path = Tp("gs://my_bucket/some_dir")
# If the password is not provided, you will asked to provide it interactively
ms = MailSender(sender="chien@chat.com", passwd="thepasswd")
ms.test_mail_server()
ms.send_mail(
   adresses=["foo@bar.com", "foo2@bar2.com"],
   subject=f"the mail subject",
   files=[some_directory_path / "some_file_name.pdf", some_directory_path / "some_other_file_name.csv"],
)
```

## MailMonitor

Class allowing to monitor a mailbox to save attachments to a
directory using conditions on sender and subjet.

If two-factor auth is activated, you will need to
provide  an app password instead of your regular password. If you do not
have one or do not remember it, make a new one by following the
instructions here (only valid for office365 acconuts):
https://docs.microsoft.com/fr-fr/azure/active-directory/user-help/
multi-factor-authentication-end-user-app-passwords

The relevant security page to set the app passwords :
https://account.activedirectory.windowsazure.com/Proofup.aspx

MailMonitor will use threading to allow for the monitoring of
different conditions and saving to different paths.

For a basic usage (monitoring one set of conditions and saving to one
location) :

## Usage
```python
from mailutility import MailMonitor
mail = MailMonitor("username")
mail.monitor(
    conditions={"subject": "test",
                "sender": "cottephi@gmail.com"},
    to_path="/home/username/Bureau",
    time_to_sleep=5
)
```

To monitor several sources and save to different paths, use :

```python
mail.monitor(
    conditions=[{"sender": "a@b.c", "subject": "g"}, {"sender": "d@e.f", "subject": "h"}],
    to_path=["/home/username/Desktop", "/home/username/Documents"],
    time_to_sleep=5,
)
```

You can decide to save to GCS by using TransparentPath:

```python
# noinspection PyShadowingNames, PyUnresolvedReferences
from transparentpath import TransparentPath as Path
from mailutility import MailMonitor
Path.set_global_fs("gcs", bucket="my_bucket", project="my_project")
mail = MailMonitor("tomonitor@mailbox.com")
mail.monitor(
    conditions={"subject": "test",
                "sender": "chient@chat.com"},
    to_path=Path("attachment"), 
    time_to_sleep=5
)
```

If conditions is an empty dict, will save attachments of all incoming
mails.

Any email triggering the monitor will be marked as SEEN.

### Notes and warnings:

1. Even though multiprocessing is used, any code written after the
call to mail.monitor will not be executed until the monitoring ends.

2. The file saving system tends to see mail signature as attachments,
you will have to delete the files yourself, or ignore them in your
analysis.
