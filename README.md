# L7z
This is a Python-based GUI for 7zip on non-Window$ systems.   
It aims to imitate the official 7zip-GUI's behaviour and layout, while being themable through Qt6 and compatible 
with Linux and other *NIXes without the use of WINE.   

## Why? 
People who go from Window$ to Linux often miss the programs they liked to use. 7zip actually exists on Linux, just that 
it's a pure CLI application.   
I got fed up with the snap trying to bring 7zip's GUI to Linux through WINE, because it cannot use Unicode file names 
(e.g. my downloads folder, `~/Hämtningar`, becomes `~/HÃ¤mtningar`) and because the right click menu in the file view 
doesn't work. That's why I'm writing a whole new GUI for 7zip that uses the CLI 7zip under the hood but presents the 
familiar GUI.   

Please note that I will not be making this whole program within a few days, but until then you can install the official 
7zip Window$ GUI in a WINE prefix of your choice and use it without having to rely on SNAP. That way you'll be able to 
use the context menu and 7zip will follow your WINE theme.   