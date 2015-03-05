import maya.cmds as cmds
import maya.OpenMaya as om


class simpleModelPreviewer(object):
    def __init__(self, *args):
        self._name = "simpleModelPreviewer"
        self._title = "Simple Model Previewer"

        self._modelFilePath = ""
        self._renderOutputFilePath = ""

        self.meshList = []

    def show(self):
        self.createLayout()

    def createLayout(self):
        # create UI
        win = self._name
        if cmds.window(win, ex=True):
            cmds.deleteUI(win)

        win = cmds.window(self._name, widthHeight=(400, 200), title=self._title, resizeToFitChildren=1)

        cmds.columnLayout(adjustableColumn=True, columnAlign="center", rowSpacing=5)

        cmds.separator()
        cmds.text("Load Model File")
        cmds.separator()

        cmds.columnLayout(adjustableColumn=True, columnAlign="left", rowSpacing=5)

        self.button1 = cmds.textFieldButtonGrp(label="File Path:",
                                        text="Please select your model file",
                                        buttonLabel="Load Model",
                                        width=200,
                                        buttonCommand=self.load_model)

        self.button2 = cmds.button("Reload", enable=False, c=self.reload_model)

        cmds.setParent("..")
        cmds.separator()
        cmds.text("Camera Options")
        cmds.separator()
        cmds.rowColumnLayout(numberOfColumns=2,
                             columnWidth=[(1, 200), (2, 200)],
                             cal=[(1, "right"), (2, "center")],
                             cs=[(1, 5), (2, 5)],
                             rs=[(1, 5), (2, 5)])
        self.button3 = cmds.button("Create Camera", c=self.create_camera)
        self.button4 = cmds.button("Adjust Camera", c=self.adjust_camera)
        cmds.text("Animation Length (seconds):")
        self.frameLength = cmds.floatField(minValue=0.0)
        cmds.text("Animation FPS:")
        self.animationFPS = cmds.optionMenu()
        cmds.menuItem(label="12")
        cmds.menuItem(label="24")
        cmds.menuItem(label="25")
        cmds.menuItem(label="30")
        cmds.menuItem(label="50")
        cmds.menuItem(label="60")

        cmds.setParent("..")
        self.button5 = cmds.button("Create Camera Motion", width=100, c=self.create_camera_motion)

        cmds.separator()
        cmds.text("Material Options")
        cmds.separator()
        cmds.rowColumnLayout(numberOfColumns=2,
                             columnWidth=[(1, 200), (2, 200)],
                             cal=[(1, "right"), (2, "center")],
                             cs=[(1, 5), (2, 5)],
                             rs=[(1, 5), (2, 5)])

        self.materialOption = cmds.optionMenu()
        cmds.menuItem(label="Stone")
        cmds.menuItem(label="Plastic")
        cmds.menuItem(label="Glass")
        cmds.menuItem(label="Wood")
        self.button6 = cmds.button("Assign Material", c=self.config_model_material)

        cmds.setParent("..")
        cmds.separator()
        cmds.text("Output Options")
        cmds.separator()

        cmds.columnLayout(adjustableColumn=True, columnAlign="left", rowSpacing=5)
        self.button7 = cmds.textFieldButtonGrp(label="Output File Path:",
                                               text="Please select your output path.",
                                               buttonLabel="Select Path",
                                               width=200,
                                               buttonCommand=self.config_output_path)

        cmds.rowColumnLayout(numberOfColumns=2,
                             columnWidth=[(1, 200), (2, 200)],
                             cal=[(1, "right"), (2, "center")],
                             cs=[(1, 5), (2, 5)],
                             rs=[(1, 5), (2, 5)])

        cmds.text("Choose Output Format")
        self.outputFormatOption = cmds.optionMenu()
        cmds.menuItem(label="png")
        cmds.menuItem(label="tif")
        cmds.menuItem(label="openEXR")

        cmds.text("Start Frame:")
        self.startFrame = cmds.intField(minValue=0)
        cmds.text("End Frame:")
        self.endFrame = cmds.intField(minValue=0)

        cmds.text("Output Width:")
        self.outputWidth = cmds.intField(minValue=0)
        cmds.text("OutputHeight:")
        self.outputHeight = cmds.intField(minValue=0)

        cmds.setParent("..")
        cmds.separator()
        self.renderButton = cmds.button("RENDER", width=200, backgroundColor=[0, 1, 0], c=self.renderOutput)
        cmds.separator()


        cmds.setParent(menu=True)

        cmds.showWindow(win)



    def load_model(self, *args):
        filter = "All Files (*.*);;Maya Ascii (*.ma);;Maya Binary (*.mb)"
        self.load_model_dialog = cmds.fileDialog2(fileFilter=filter, dialogStyle=1, fm=1)

        if self.load_model_dialog is None:
            return
        if not (len(self.load_model_dialog)):
            return

        self.inputModelFilename = self.load_model_dialog[0]
        print self.inputModelFilename
        if self.inputModelFilename != "":
            cmds.textFieldButtonGrp(self.button1, text=self.inputModelFilename, e=True)
            cmds.button(self.button2, e=True, enable=True)
            self.reload_model(self.inputModelFilename)
        else:
            print ("Error, model file name is empty.")

    def reload_model(self, *args):
        # check self.inputModelFilename
        if self.inputModelFilename:
            #check if scene is empty or show a dialog
            currentMeshList = cmds.ls(type='mesh')
            if len(currentMeshList) > 0:
                print ("Warning, current scene has other mesh objects:")
                print (str(currentMeshList))

                #user should remove all the mesh objects, otherwise they may get unwanted result.
                val = cmds.confirmDialog(title='Scene is not empty.',
                                         message='Please prepare an empty scene to better use this plugin. ',
                                         button=['OK', 'Ignore'])

                #press OK to prepare the scene manually.
                if val == "OK":
                    cmds.textFieldButtonGrp(self.button1, text="Please select your model file", e=True)
                    cmds.button(self.button2, e=True, enable=False)
                    return

            print ("Loading %s..." % self.inputModelFilename)
            try:
                cmds.file(self.inputModelFilename, i=True)
            except:
                print ("Error, unable to load file %s." % self.inputModelFilename)
                return

            #record the mesh objects
            self.meshList = cmds.ls(type='mesh')

        else:
            print ("Error, input model filename is empty.")





        pass
    def create_camera(self, *args):
        pass

    def adjust_camera(self):
        pass
    
    def create_camera_motion(self, *args):
        pass
    def update_camera_motion(self, *args):
        pass
    def config_animation_speed(self, *args):
        pass
    def config_camera_motion_time(self, *args):
        pass
    
    def create_basic_lighting(self, *args):
        pass
        
    def config_model_material(self, *args):
        pass
        
    def config_output_path(self, *args):
        pass
    def config_output_format(self, optionIdx):
        pass
    def config_output_range(self, startIdx, endIdx):
        pass
    def config_output_resolution(self, optionIdx):
        pass

    def renderOutput(self):
        pass


b_cls = simpleModelPreviewer()
b_cls.show()
