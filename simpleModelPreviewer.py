import os

import maya.cmds as cmds


class simpleModelPreviewer(object):
    def __init__(self, *args):
        self._name = "simpleModelPreviewer"
        self._title = "Simple Model Previewer"

        self._modelFilePath = ""
        self.renderOutputFilePath = ""

        self.meshList = []

        self.frameLength = 60.0
        self.animationFPS = 24

        self.totalFramenumber = int(self.frameLength * self.animationFPS)

        self.outputFormat = "png"

        # config maya unit
        cmds.currentUnit(angle='degree', time='film')

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
        # textChangedCommand=self.on_input_model_path_text_changed)

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
        self.button3 = cmds.button("Create Camera and Motion", c=self.create_camera)
        self.button4 = cmds.button("Adjust Camera and Motion", c=self.adjust_camera)
        cmds.text("Animation Length (seconds):")
        self.frameLengthField = cmds.floatField(minValue=0.0, value=self.frameLength, precision=2,
                                                changeCommand=self.config_animation_length)
        cmds.text("Animation FPS:")
        self.animationFPSOption = cmds.optionMenu(changeCommand=self.config_animation_fps)
        cmds.menuItem(label="12")
        cmds.menuItem(label="24")
        cmds.menuItem(label="25")
        cmds.menuItem(label="30")
        cmds.menuItem(label="50")
        cmds.menuItem(label="60")
        cmds.optionMenu(self.animationFPSOption, e=True, value="24")

        cmds.setParent("..")
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
                                               buttonCommand=self.config_output_path,
                                               textChangedCommand=self.on_output_path_text_changed)


        cmds.rowColumnLayout(numberOfColumns=2,
                             columnWidth=[(1, 200), (2, 200)],
                             cal=[(1, "right"), (2, "center")],
                             cs=[(1, 5), (2, 5)],
                             rs=[(1, 5), (2, 5)])

        cmds.text("Choose Output Format")
        self.outputFormatOption = cmds.optionMenu(changeCommand=self.on_output_format_change)
        cmds.menuItem(label="png")
        cmds.menuItem(label="tif")
        cmds.menuItem(label="openEXR")

        cmds.text("Start Frame:")
        self.startFrameField = cmds.intField(minValue=1, value=1, changeCommand=self.on_start_frame_change)
        cmds.text("End Frame:")
        self.endFrameField = cmds.intField(minValue=1, value=self.totalFramenumber,
                                           changeCommand=self.on_end_frame_change)

        cmds.text("Output Width:")
        self.outputWidthField = cmds.intField(minValue=0, value=720, changeCommand=self.on_output_width_change)
        cmds.text("OutputHeight:")
        self.outputHeightField = cmds.intField(minValue=0, value=576, changeCommand=self.on_output_height_change)

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
            cmds.textFieldButtonGrp(self.button7, text=os.path.dirname(self.inputModelFilename), e=True)
            cmds.button(self.button2, e=True, enable=True)
            self.reload_model(self.inputModelFilename)
        else:
            print ("Error, model file name is empty.")

    # def on_input_model_path_text_changed(self, *args):
    # self.inputModelFilename = cmds.textFieldButtonGrp(self.button1, query=True, text=True)
    #     print self.inputModelFilename
    #     if self.inputModelFilename != "":
    #         cmds.textFieldButtonGrp(self.button7, text=os.path.dirname(self.inputModelFilename), e=True)
    #         cmds.button(self.button2, e=True, enable=True)
    #         self.reload_model(self.inputModelFilename)
    #     else:
    #         print ("Error, model file name is empty.")

    def reload_model(self, *args):
        # check self.inputModelFilename
        if self.inputModelFilename:
            #check if scene is empty or show a dialog
            currentMeshList = cmds.ls(geometry=True)
            if len(currentMeshList) > 0:
                print ("Warning, current scene has other mesh objects:")
                print (str(currentMeshList))

                #user should remove all the mesh objects, otherwise they may get unwanted result.
                val = cmds.confirmDialog(title='Scene has other geometry.',
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
            self.prep_model()
            self.create_camera()
        else:
            print ("Error, input model filename is empty.")

    def prep_model(self):
        """
        prepare newly imported geometry. move them to the origin. mute all the existing lights,
        """
        # find all the geometry objects
        self.allGeometry = cmds.ls(geometry=True)
        allRoot = []

        # find all root objects
        for obj in self.allGeometry:
            objIter = obj
            while True:
                parent = cmds.listRelatives(objIter, allParents=True, path=True)
                if not parent:
                    allRoot.append(objIter[0])
                    break
                objIter = parent
        #make root objects be unique in the container
        allRoot = set(allRoot)
        allRoot = list(allRoot)
        #select all the root objects
        cmds.select(allRoot)
        #move all the root objects as one object to the origin
        boundingbox_center = cmds.xform(q=True, bb=True, ws=True)
        cmds.move(-(boundingbox_center[0] + boundingbox_center[3]) / 2.0,
                  -(boundingbox_center[1] + boundingbox_center[4]) / 2.0,
                  -(boundingbox_center[2] + boundingbox_center[5]) / 2.0,
                  absolute=True)
        cmds.select(None)

        # delete the light group created by this plugin
        if "SMP_Lights" in cmds.ls("SMP_Lights"):
            cmds.select("SMP_Lights")
            cmds.delete()
        #hide all lights
        if cmds.ls(type='light'):
            cmds.select(cmds.ls(type='light'))
            cmds.hide()
            cmds.select(None)
        #create 3 layer of directional lights plus a top light
        topLayer = []
        midLayer = []
        botLayer = []
        #3 layer at +75, 0, -75 degree
        angleStep = 5.0
        topAngle = 75.0
        midAngle = 0.0
        botAngle = -75.0
        #this formula gives the unit light intensity
        generalIntensity = 1 / (360.0 / angleStep * 3) * 3
        #create circles of lights in a loop
        angle = 0.0
        while (angle < 360.0):
            topLayer.append(cmds.directionalLight(intensity=generalIntensity, rotation=(topAngle, angle, 0)))
            midLayer.append(cmds.directionalLight(intensity=generalIntensity * 4, rotation=(midAngle, angle, 0)))
            botLayer.append(cmds.directionalLight(intensity=generalIntensity, rotation=(botAngle, angle, 0)))
            angle += angleStep
        #add the top light
        above = cmds.directionalLight(intensity=generalIntensity * 360 / angleStep * 0.5, rotation=(-90, 0, 0))
        #organize all lights into group
        lightLists = topLayer + midLayer + botLayer + [above]
        cmds.select(lightLists)
        cmds.group(n="SMP_Lights")
        cmds.select(None)

    def create_camera(self, *args):
        # delete SMP_Camera is already exists
        if "SMP_Camera" in cmds.listCameras():
            cmds.select("SMP_Camera")
            cmds.delete()
        newcam = cmds.camera()
        # it appears SMP_CameraShape was modified automatically
        cmds.rename(newcam[0], "SMP_Camera")

        cmds.select(self.allGeometry)
        #fit camera, factor of 0.5 means the geometry will occupy about half of the fov
        cmds.viewFit("SMP_CameraShape", an=False, f=0.5)
        cmds.select("SMP_Camera")
        cmds.rotate(-20, 0, 0, p=[0, 0, 0], a=True)

        #move camera pivot to origin
        cmds.move(0, 0, 0, str("SMP_Camera" + ".scalePivot"), str("SMP_Camera" + ".rotatePivot"), a=True)
        #create an expression for camera motion
        angleStepPerFrame = str(360.0 / self.totalFramenumber)
        expr = "SMP_Camera.rotateY=(frame-1) * " + angleStepPerFrame
        self.camera_motion_expression = cmds.expression(n="SMP_Camera_Motion_Expression",
                                                        s=expr)

    def adjust_camera(self):
        """
        Cause the options like frame length can change, so must update the expression here
        :return:
        """
        cmds.select(self.allGeometry)
        # fit camera, factor of 0.5 means the geometry will occupy about half of the fov
        cmds.viewFit("SMP_CameraShape", an=False, f=0.5)
        cmds.select("SMP_Camera")
        cmds.rotate(-20, 0, 0, p=[0, 0, 0], a=True)

        #move camera pivot to origin
        cmds.move(0, 0, 0, str("SMP_Camera" + ".scalePivot"), str("SMP_Camera" + ".rotatePivot"), a=True)
        #create an expression for camera motion
        angleStepPerFrame = str(360.0 / self.totalFramenumber)
        expr = "SMP_Camera.rotateY=(time-1) * " + angleStepPerFrame
        self.camera_motion_expression = cmds.expression(n="SMP_Camera_Motion_Expression",
                                                        s=expr)


    def config_animation_length(self, *args):
        self.frameLength = cmds.floatField(self.frameLengthField, query=True, value=True)
        print(self.frameLength)
        self.totalFramenumber = int(self.frameLength * self.animationFPS)
        self.adjust_camera()

    def config_animation_fps(self, *args):
        self.animationFPS = int(cmds.optionMenu(self.animationFPSOption, query=True, value=True))
        print(self.animationFPS)
        self.totalFramenumber = int(self.frameLength * self.animationFPS)
        self.adjust_camera()
        
    def config_model_material(self, *args):
        pass
        
    def config_output_path(self, *args):
        self.output_path_dialog = cmds.fileDialog2(dir=os.path.dirname(self.inputModelFilename), dialogStyle=2, fm=3)
        self.renderOutputFilePath = self.output_path_dialog[0]
        cmds.textFieldButtonGrp(self.button7, text=self.renderOutputFilePath, e=True)

    def on_output_path_text_changed(self, *args):
        self.renderOutputFilePath = cmds.textFieldButtonGrp(self.button7, query=True)

    def on_output_format_change(self, *arg):
        self.outputFormat = cmds.optionMenu(self.outputFormatOption, query=True, value=True)
        print (self.outputFormat)

    def on_start_frame_change(self, *arg):
        self.startFrame = cmds.intField(self.startFrameField, query=True, value=True)
        print(self.startFrame)

    def on_end_frame_change(self, *arg):
        self.endFrame = cmds.intField(self.endFrameField, query=True, value=True)
        print(self.endFrame)

    def on_output_width_change(self, *arg):
        self.outputWidth = cmds.intField(self.outputWidthField, query=True, value=True)
        print(self.outputWidth)

    def on_output_height_change(self, *arg):
        self.outputHeight = cmds.intField(self.outputHeightField, query=True, value=True)
        print(self.outputHeight)
    def renderOutput(self):
        pass


b_cls = simpleModelPreviewer()
b_cls.show()
