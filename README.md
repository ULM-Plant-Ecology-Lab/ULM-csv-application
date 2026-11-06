# RAW data Tool
## 🛠️ Prerequisites & Setup 
Follow these steps to install the tool.
### 1. Downloading the template file
1. on your desktop or if you would like to make this folder elsewhere do the same thing below but in a file explorer window
2. right click on a blank part of the desktop and a menu should appear go to the new button and hover over it then select folder from the drop down menu name the folder what ever you want and note where it is
3. From the repository on your web browser click on the `templateFile.csv` file to open it
4. On the file preview screen, locate the group of 3 buttons in the top-right corner (the first button is labeled **Raw**).
5. Click the 3rd button on the right (the download icon, which shows the tooltip **"Download raw file"** when you hover over it) to save the file to your computer.
6. save it in that folder you make in step 2
### 2. Downloading The Exe File

1. Open the `Raw Data Tool` folder in this repository.
2. Click on the `RDTOOLV1.3.2.exe` file.
3. On the file preview screen, locate the group of 3 buttons in the top-right corner (the first button is labeled **Raw**).
4. Click the 3rd button on the right (the download icon, which shows the tooltip **"Download raw file"** when you hover over it) to save the file to your computer.
5. you should save the tool in the same folder you saved the `templateFile.csv` earlier if you do not do this the tool will have errors
6. in the folder you have saved the tool left click on the `RDTOOLV1.3.2.exe` file and in the next menu click see more options at the bottom when the new menu comes hover over send to and click the 🖥️Desktop(create shortcut) menu button in the menu that comes up when you hover over the send to button be careful not to click any of the other options
## 💻 Using The Tool
1. double click the Desktop shortcut you created for the tool in the setup steps and wait for the window to open
2. click the <kbd>Add Files...</kbd> button near the top of the window and next to the white box labeled Input Headless Files then select your files for the current year using windows file explorer
> ‼️**IMPORTANT NOTE** ‼️ **DO NOT** change the location of the temp file in the input window the only reason it is there is so that if we were to later need other use cases they may want to change that but as long as you are dealing with carbon data you **SHOULD** ***NEVER*** touch that input
3. once you've added all the data files for this particular year please remember to name the output file after the year
4. then select either Chronological or Reverse Chronological depending on what you need but please use same order for all your files 
> **Note:** the default is Chronological if unsure use that
5. once you are done naming the output file click the <kbd>Merge & Apply Headers</kbd> button
6. press the <kbd>Okay</kbd> button on the success prompt and check the folder where your output is for a headered file with dates ordered by whatever you selected in step 4
> **Note:** now this file is ready for the next tool
7. to create the next file hit the <kbd>Clear All</kbd> button (located below the <kbd>Remove Selected</kbd> button and next to the white box that displays your file inputs)
8. Now repeat steps 2 through 7 until all headered year files have been properly generated
# ULM_CSV_TOOL
the replacement for the old query system for ULM
## 🛠️ Prerequisites & Setup 
Follow these steps to install the tool.
### 1. Downloading The Exe File

1. Open the `releases` folder in this repository.
2. Click on the `ULMCSVTOOLV2.2.0.exe` file.
3. On the file preview screen, locate the group of 3 buttons in the top-right corner (the first button is labeled **Raw**).
4. Click the 3rd button on the right (the download icon, which shows the tooltip **"Download raw file"** when you hover over it) to save the file to your computer.
5. save the tool in the same folder as the raw data tool using windows file explorer 
6. in the folder you have saved the tool left click on the `ULMCSVTOOLV2.2.0.exe` file and in the next menu click see more options at the bottom when the new menu comes hover over send to and click the 🖥️Desktop(create shortcut) menu button in the menu that comes up when you hover over the send to button be careful not to click any of the other options
## 💻 Using The Tool
### 1. Selecting The Input and Output Files
1. First you will need to double-click the desktop shortcut
2. Next you will need to hit the <kbd>Browse...</kbd> button in the program window next to the `input file:` label and after the white input box
3. Navigate to your data file's location using windows file explorer and select the file
4. If you want to use multiple files here hit the <kbd>+ Add Input File</kbd> button at the bottom of the file options box until you have enough input file items (if you hit this button too many times just use the <kbd>Remove</kbd> button (it's the last button) on any file inputs that are not needed) then repeat steps 2 and 3 until all input files have been selected
> **Optional Step 5:** the output file will automatically name itself after your input file's name with `_processed.csv` on original file name (it uses the first file name) if you do not want the output file to be named this way please click the <kbd>Browse...</kbd> button on the end of the input labeled output file and navigate to the place you would like to have your output file then name it whatever you want
### 2. Selecting The Fields
1. There are 2 ways to input fields if you have a preset file skip to step 4 if not go through steps 2 and 3 and skip step 4
2. use the searchable drop down menu to select your fields
3. once you select the fields using the searchable drop down you can rename them in the output column renaming menu
4. if you have a 2 line preset file load it in the input labeled Header Preset File (2-line): by clicking the <kbd>Apply Preset File</kbd> button and then using file explorer to navigate to your preset csv file and select it the tool will auto-load the fields in your preset and rename them according to what you have set in the second line of your preset file
### 3. Selecting the Dates
1. please enter a comma separated list of start dates into the field named Start Dates and then a respective list of end dates into the field labeled End Dates please make sure you follow the requirements below when entering dates
> **Important Requirements:** It is important that you make sure to enter an equal amount of start and end dates. it is important you follow the format that the program asks for as anything not in this format will generate malformed files and possibly require manual clean up (see troubleshooting for what to do if this does happen). Also remember any dates not present in your data files should not be used so make sure you know the date ranges of your files before searching(see troubleshooting if this happens).
2. once you have correctly entered the dates hit the <kbd>Start Processing</kbd> button on the bottom left of the window next to the <kbd>Show Debug Window</kbd> button.
> **Note:** the Show debug window button is only for finding problems with the application and you should not need it
### 4. Checking The Output File
1. after the processing is finished there should be a pop up saying the processing completed successfully click the <kbd>okay</kbd> button
2. now open the output file with whatever program you wish and check that your filtered data is there
> **Note:** if you kept the default it will have made the output in the input file folder with the same name as the first input file (without the .csv) plus `_processed.csv` on the end of it
## 🪛 trouble shooting:
1. if you have accidentally entered in correct date formats or if you entered incorrect dates and generated malformed output please search where you put your output file for what you named it and delete any files you find
2. go back to the tool and correct your input and try again
## Dev notes:
1. if you ever need to update the backend.py file and you need to pack it into an exe file you need to run this command inside the folder you downloaded the repo to then pull it out of the dist folder and move it into the releases folder and then delete the dist folder and also if you do this remember to update the version numbers the first one is For large changes the second number is for medium changes and the third number is for small changes examples of large changes are if the whole User interface is being reworked into a different one a medium change is if you add a feature that requires a new UI element and/or some additional functionality is added to the backend. An example of a small change is changing comments or wording on the UI 
> **Command 1:** PyInstaller --onefile --noconsole --name "RDTOOLV1.0.0" --icon "ULM_icon.ico" --add-data "templateFile.csv;." helper.py
> **Command 2:** PyInstaller --onefile --noconsole --name "ULMCSVTOOLV2.1.0" --icon "ULM_icon.ico" backend.py
