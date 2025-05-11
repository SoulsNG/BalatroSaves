# BalatroSaves
BalatroSaves is an unofficial script for convinient Balatro steam and android save files syncing. The script allows you to transfer your steam save files (even the currently played run know as save.jkr) to your phone and vice versa automatically with just the push of... two buttons.
## How does the script work?
Well it is actually two scripts or rather one python script and one Automate flow chart. They both do the same thing just in they respective environments - one is for your PC, and one you run on your android device using the Automate app.
The core functionality is pretty simple. Both scripts just copy Balatro save files (meta.jkr, profile.jkr and save.jkr) from your device and upload or download them to or from the Google Drive depending on which are newer. Simple right?

> [!WARNING]
> * **This will only work if your android device is rooted.** There is currently no possible way to access and modify the contents of /data/data folder where Balatro saves reside without superuser (root) permission. If you don't know what that is then this script is probably not for you. Sadly as much as I would like to make it layman friendly there is nothing to be done at the moment to go around this. If you still want to root your device I recommend finding resources about rooting it online yourself as there is no universal method.
> * For the script to work you must disable Google Play service cloud save for Balatro. The cloud saving is pretty aggressive and it will always try to replace the transfered files with the cloud save. With google cloud save disabled you can't really transfer the saved progress beetwen android devices anymore (unless the other one is also rooted in which case you should be able to use the same script for android with no issues).

![](https://raw.githubusercontent.com/kapi2289/vulcan-api/master/docs/source/_static/registered.png)
## Downloading


## Installation


[python-mini-projects](https://github.com/Python-World/python-mini-projects)
