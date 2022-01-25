# Sprite Loader

This plugin works in conjunction with the GODump mod for Hollow Knight (https://github.com/jngo102/HollowKnight.GODump),
taking the sprites and JSON files containing animation data to automatically generate a Krita file containing the selected
animation and several pre-defined layers to lighten the burden of creating custom skins for Hollow Knight, i.e. using
Custom Knight.

# Installation

## Download plugin into Krita
1. Copy this GitHub page's URL (https://github.com/jngo102/SpriteLoader).
2. Open Krita.
2. Open "Tools" in the top menu bar, then open "Scripts", and finally select "Import Python Plugin from Web".
3. Paste the copied link into the input field, then select "OK".

## Manual installation
1. Open the following link in a new tab: https://github.com/jngo102/SpriteLoader/releases/download/1.0.0/SpriteLoader.zip, or expand the green "Code" button, then select "Download ZIP".
2. Once the download has finished, open Krita.
3. Open "Tools" in the top menu bar, then open "Scripts", and finally select "Import Python Plugin from File".
4. Navigate to and select the ZIP file that you downloaded.

# Usage

## Loading Sprites for Editing
1. Open "Tools" in the top menu bar, then open "Scripts", and finally select "Load Sprites". The location of the sprites dumped by GODump will open in a file browser.
2. Select a folder that contains the individual sprite PNG files (if you open the animation folder, it should open up to an empty directory; the PNG files and animation data JSON file will not appear).
3. Select the button on the file browser that loads the folder; double-clicking on the folder will not load the sprites, it will only open the folder.

## Exporting Sprites to file system
1. Make sure an animation has been currently loaded using "Load Sprites".
2. Open "Tools" in the top menu bar, then open "Scripts", and finally select "Export Sprites". 
3. Select "OK" for each prompt that appears to export each frame of the modifed animation to the folder of the animation that you initially loaded.