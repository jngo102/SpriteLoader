import json, os, string, sys
from krita import *
from PyQt5.QtWidgets import QFileDialog


# This is a plug-in for the FLOSS painting application Krita. It works in conjunction with the GODump mod for Hollow Knight 
# (https://github.com/jngo102/HollowKnight.GODump), taking the sprites and JSON files containing animation data to automatically
# generate a Krita file containing the selected animation and several pre-defined layers to lighten the burden of creating
# custom skins for Hollow Knight, i.e. using Custom Knight.


class SpriteLoader(Extension):
    def __init__(self, parent):
        super().__init__(parent)
        self.mainDocument = None
        self.referenceFiles = []
        
    # Must be overriden for the plugin to work.
    def setup(self):
        pass

    # Add actions to Krita so that they may be accessed from the 'Tools' menu.
    def createActions(self, window):
        loadAction = window.createAction("loadSprites", "Load Sprites")
        loadAction.triggered.connect(self.loadSprites)
        exportAction = window.createAction("exportSprites", "Export Sprites")
        exportAction.triggered.connect(self.exportSprites)

    # Load sprites from an animation folder into a Krita file.
    def loadSprites(self):
        self.referenceFiles.clear()

        if self.spritesPath == "":
            
            return
        animationDirectory = QFileDialog.getExistingDirectory(
            None,
            "Select folder containing Sprite .pngs",
            self.spritesPath,
            QFileDialog.ShowDirsOnly,
        )

        while animationDirectory == "":
            warning = QMessageBox(QMessageBox.Icon(),
                                  "Error!", "This is an invalid path for an animation.")
            warning.show()
            warning.exec()

            animationDirectory = QFileDialog.getExistingDirectory(
                None,
                "Select folder containing Sprite .pngs",
                self.spritesPath,
                QFileDialog.ShowDirsOnly,
            )

        animationName = animationDirectory.split("/")[-1].split(".")[-1]
        self.mainDocument = Krita.instance().createDocument(2, 2, animationName, "RGBA", "U8", "", 120.0)
        root = self.mainDocument.rootNode()
        Krita.instance().activeWindow().addView(self.mainDocument)
        firstPng = os.path.join(animationDirectory, os.listdir(animationDirectory)[0])
        animInfo = open(os.path.join(animationDirectory, "AnimInfo.json"))
        animJson = json.loads(animInfo.read())
        fps = animJson["fps"]
        document = Krita.instance().openDocument(firstPng)
        self.mainDocument.setWidth(document.width())
        self.mainDocument.setHeight(document.height())
        for rootDir, directory, files in os.walk(animationDirectory):
            for file in files:
                if ".png" in file:
                    filePath = os.path.join(rootDir, file)
                    self.referenceFiles.append(filePath)
        Krita.instance().setActiveDocument(self.mainDocument)
        self.mainDocument.importAnimation(self.referenceFiles, 0, 1)
        referenceLayer = root.childNodes()[1]
        referenceLayer.setName("Reference")
        referenceLayer.setOpacity(127)
        sketchGroupLayer = self.mainDocument.createNode("Sketch", "groupLayer")
        sketchPaintLayer = self.mainDocument.createNode("Sketch", "paintLayer")
        finalLayer = self.mainDocument.createNode("Final", "groupLayer")
        inkLayer = self.mainDocument.createNode("Ink", "paintLayer")
        baseLayer = self.mainDocument.createNode("Base", "paintLayer")
        shadeLayer = self.mainDocument.createNode("Shade", "paintLayer")
        lightLayer = self.mainDocument.createNode("Light", "paintLayer")
        shadeLayer.setAlphaLocked(True)
        lightLayer.setAlphaLocked(True)
        root.addChildNode(finalLayer, None)
        finalLayer.addChildNode(baseLayer, None)
        finalLayer.addChildNode(shadeLayer, baseLayer)
        finalLayer.addChildNode(lightLayer, baseLayer)
        finalLayer.addChildNode(inkLayer, shadeLayer)
        root.addChildNode(sketchGroupLayer, finalLayer)
        sketchGroupLayer.addChildNode(sketchPaintLayer, None)

        self.mainDocument.setFramesPerSecond(fps)
        self.mainDocument.setFullClipRangeEndTime(len(self.referenceFiles) - 1)
        self.mainDocument.setActiveNode(sketchPaintLayer)

    # Export all edited frames from the loaded animation back into the selected animation's folder.
    def exportSprites(self):
        if len(self.referenceFiles) <= 0:
            warning = QMessageBox(QMessageBox.Icon(), "Error!", "An animation has not been loaded yet! Please select an animation folder using \"Load Sprites\".")
            warning.show()
            warning.exec()
            return
        for frame in range(len(self.referenceFiles) - 1):
            self.mainDocument.setCurrentTime(frame)
            self.mainDocument.saveAs(self.referenceFiles[frame])
            os.remove(self.referenceFiles[frame] + "~")


Krita.instance().addExtension(SpriteLoader(Krita.instance()))
