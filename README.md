
These instructions assume you already have python and anaconda installed. If not, go to: https://www.anaconda.com/. 
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
INSTALLATION and REQUIRMENTS 

OBS comes with an integrated virtual camera feature, but it provides only a single camera instance, 
so it is not possible to send frames from the the built-in OBS virtual Camera to Python, do manipulations
to the videostream and then send these frames to zoom using the same virtual camera. 
Therefore, the filter pipeline requires two seperate virtucal camera extensions. 
One working as an input source from OBS to the script and the other as input source to zoom (or some other platform). 
Thankfully there is an old plugin that still works fine and that can be used simultaneously as the one already integrated in OBS. 
Here is a scetch of the workflow (more details later):

1. OBS-screen capture of participants zoom window.
2. This videostream of the participant is used as input to the python script using OBS-virtual camera plugin (lets call it VC1). 
3. The script allows for manipulation of the videostream and sends frames to the built-in virtual camera. 
4. Select OBS Virtual Camera as input source on Zoom and you will be broadcasting frames from the script. 

Make sure to install the following versions of Zoom and the virtual camera plugin (newer versions of OBS are incompatilble with the older plugin):
Correct OBS-version: https://www.videohelp.com/software?d=OBS-Studio-26.0-Full-Installer-x64.exe
Old Virtual camera plugin/addon: https://obsproject.com/forum/resources/obs-virtualcam.949/

Once both of these are installed: 
1. Open OBS, 
2. Select tools from the top panel, 
3. select the option that says VirtucalCam, 
4. In the options menu check the autostart option, this will have the plugin virtual camera be availble as input to script whenever you open OBS. 

Installing virtual environment: 
1. If you havent already, go to https://github.com/DanielZander/Virtual-cam- and make sure all files are download in a seperate folder. 
(Or open git bash and do: git clone https://github.com/DanielZander/Virtual-cam-.git)
2. Open anaconda promt. 
3. Type: conda env create -f your-path-to-yaml-file\virtual_filter_env.yaml 
For example, I would write the following in the prompt: conda env create -f C:\Users\DanielZander\Documents\Virtual-cam-\virtual_filter_env.yaml
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
DIFFERENT SETUPS

Setup for self-use/filter testing:
1. Open anaconda promt.
2. type: conda activate virtual_filter
3. type: spyder

Note: usually takes a few seconds to open up.
4. In the tope panel, click flike and then open. 
5. Browse to the file name 'script' in your designated folder and double click it. 
6. Scroll down to line 39 of the script and make sure that the index = 0. 
7. Have "OBS Virtual Camera" selected as input source on zoom. 
8. Run the script by pressing the play button in spyder. 

Setup for experiment:
1. Open OBS and capture the frames of the participants' zoom window. (Make sure you have started the virtual camera plugin, should be on autostart if you did all the steps in the installation part). 
2. Open anaconda promt.
3. type: conda activate virtual_filter
4. type: spyder

Note: usually takes a few seconds to open up.
5. Browse to the file name 'script' in your designated folder and double click it (assuming it is not already opened in spyder).
6.  Scroll down to line 39 of the script and change the videocapture index to 1 or 2, if one doesnt work, try the other. 

Note: these indices refer to different cameras (virutal or otherwise) that are recognized by windows. You want to find the virtual camera plugin and use it as input since the script will per default send frames to the built-in version. 
7. Have "OBS Virtual Camera" selected as input source on zoom. 
8. Run the script by pressing the play button in spyder. 








