# BalatroSaves

BalatroSaves is an unofficial script for convinient Steam and Android Balatro save files syncing. The script allows you to transfer your steam save files (even the currently played run, also known as save.jkr) to your phone and vice versa, automatically with just the push of... two buttons.

## How does it work?

The project consist of one python script and one Automate flow chart. They both do the same thing just in they respective environments - one is for PC, and one is run on an Android device using the Automate app.
The core functionality for both platforms is the same and also pretty simple in theory. Both scripts synchronize Balatro save files (meta.jkr, profile.jkr, and save.jkr) between your device and Google Drive, automatically uploading or downloading files based on the most recent modification dates. Easy right?

> [!WARNING]
> * **This will only work if your android device is rooted.** There is currently no possible way to access and modify the contents of `/data/data` folder where Balatro saves reside without superuser (root) permission. If you don't know what that is then this script is probably not for you. Sadly as much as I would like to make it layman friendly there is nothing to be done at the moment to go around this. If you still want to root your device I recommend finding resources about rooting it online yourself as there is no universal guide and methods vary a lot depending on the manufacturer and model of your device.
> * For the script to work you must disable Google Play service cloud save for Balatro. The cloud saving is pretty aggressive and it will always try to replace the transfered files with the cloud save. With google cloud save disabled you can't really transfer the saved progress beetwen android devices anymore (unless the other one is also rooted in which case you should be able to use the same script for android with no issues).

## Downloads

All the necessary files are found in [Releases](https://github.com/SoulsNG/BalatroSaves/releases). Download the latest PC and Android files respectively.

## Installation

### PC

First you need to create a Google Cloud project. To do so:
1. Go to https://console.cloud.google.com/projectcreate. Name the project, however you like but for convenience just stick with BalatroSaves. Then click Create.
2. In the Google Cloud console, go to Menu > Google Auth platform > Clients. [[link](https://console.cloud.google.com/auth/clients)]
3. Click Create Client.
4. Click Application type > Desktop app.
5. In the Name field, type a name for the credential. This name is only shown in the Google Cloud console.
6. Click Create. The newly created credential appears under "OAuth 2.0 Client IDs."
7. Save the downloaded JSON file as credentials.json, and move the file to `BalatroSaves/PCv2.0/credentials`.
8. Create a folder on your Google Drive. After you do this, open the folder and check the URL: <br />
![](assets/installation.png) <br />
This is your folder ID. Copy it and paste it into BalatroSaves.py: `PARENT_FOLDER_ID = “paste folder ID here”`.
9. Install the dependencies found in `requirements.txt`.
    
```bash
    pip install -r requirements.txt
 ```

### Android

1. Download Automate app. <br /> https://llamalab.com/automate/
2. Open Automate and go to the settings and set Privileged service start method as the superuser.
3. Import Balatro Saves `.flo` file.
4. Make sure to give all the needed permissions and privileges for the flow and the Automate app to ensure the script will run correctly.  

## Usage

After setting everything up you should just be able to run the BalatroSaves.py from the terminal. The script should automatically decide to upload or to download files. It also automatically puts them in your saves folder. After it runs you should just be able to play the game. <br />
When it comes to Android version of the script the principle is the same. You just run it in Automate app and after it runs all saves should be either backed up or uploaded to your device. <br />
> [!NOTE] 
Remember that you will need to run the corresponding script every time you launch or close the game on both Android and PC.

