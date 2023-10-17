# getwfslayers
Hmm. Now looking again to this script I suspect I created wrong expectations in a twitter interaction. I'm sorry. I will try being constructive about this regardless. Maybe a good opportunity to have this right for something useful. (check TODO)
- Made this script in a hurry to help me in a specific WFS server/link I use a lot
- I didn't test this for other WFS servers/links. Looking at the code I'm not sure it will work for any WFS server (and just too tired to test it right now). Specially worried about line 85 (I think I have .split() upon some not immutable field, hardcoded there)  
  
If you want to try:
- Change 'servicelink' to the WFS service you want to fetch
- Create a working directory and set the 'workingdir' variable poiting to this directory.
- Set variable 'mode' = 1 to fetch WFS. It will create a file named 'layerNames.txt' in 'workingdir'
- Create a file 'layersToDownload.txt' in 'workingdir' with the layer titles you want to download. The first line in this file must be the destination directory you want to store downloaded layers. See the 'layersToDownload.txt' example file in this repo
- Set 'mode' = 2 and run the script again. It will (hopefully) download your layers to 'workingdir' and store a ZIP copy of the layers under 'workingdir'/zipcopies
- Suggestions: Run the two modes with the actual 'servicelink' to check how it works. Check code line 62
  
  
# TODO
- Turn this script into a python class so it can be used programatically in Python scripts
- Add functionality
- Make it work for any WFS server
- Package to PyPi