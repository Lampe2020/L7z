# L7z
This is a Python-based GUI for 7-zip on non-Window$ systems.   
It aims to imitate the official 7-zip-GUI's behaviour and layout, while being themable through Qt6 and compatible 
with Linux and other *NIXes without the use of WINE.   
To use this project you need the official CLI application installed, as this is just a GUI frontend for that. 

## Why? 
People who go from Window$ to Linux often miss the programs they liked to use. 7-zip actually exists on Linux, just that 
it's a pure CLI application.   
I got fed up with the snap trying to bring 7-zip's GUI to Linux through WINE, because it cannot use Unicode file names 
(e.g. my downloads folder, `~/Hämtningar`, becomes `~/HÃ¤mtningar`) and because the right click menu in the file view 
doesn't work. That's why I'm writing a whole new GUI for 7-zip that uses the CLI 7-zip under the hood but presents the 
familiar GUI.   
Also, with the soon-to-be death of Window$ 10, I (and many others) expect a bit of an influx in users to Linux, who are 
used to using Window$. And they don't want to relearn more than absolutely necessary. 

Please note that I will not be making this whole program within a few days, but until then you can install the official 
7-zip Window$ GUI in a WINE prefix of your choice and use it without having to rely on SNAP. That way you'll be able to 
use the context menu and 7-zip will follow your WINE theme.   

I had semi-abandoned this project for about nine months because real life (yes, I have a life) got in the way. But I plan 
on picking this back up soon, now that I have an extra motivation of it maybe actually becoming quite popular by being 
there at the right time (if I can manage to pull that off, please help me if you can by contributing to this repo). And I 
would really like to be the creator of a popular FOSS project, so I can feel like I have accomplished _something_ useful 
in my life, even if I should fail at landing my dream job in the future.   
