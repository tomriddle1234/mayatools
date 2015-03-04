import maya.cmds as cmds
import maya.OpenMaya as om

class createMyLayoutCls(object):
    def __init__(self, *args):
        pass
    def show(self):
        self.createMyLayout()
    def createMyLayout(self):
        self.window = cmds.window(widthHeight=(400, 200), title="Simple Model Previewer",   resizeToFitChildren=1)
        cmds.rowLayout("button1, button2, button3", numberOfColumns=5)

        cmds.columnLayout(adjustableColumn=True, columnAlign="center", rowSpacing=10)

        self.button1 = cmds.textFieldButtonGrp(label="LocatorCurve",
                                        text="Please key in your coordinates",
                                        changeCommand=self.edit_curve,
                                        buttonLabel="Execute",
                                        buttonCommand=self.locator_curve)
        
        self.button2 = cmds.textFieldButtonGrp(label="LoadModel",
                                        text="Please select your model file",
                                        buttonLabel="Execute",
                                        buttonCommand=self.load_model)         

        self.button3 = cmds.textFieldButtonGrp(label="Create Camera",
                                        text="Click to create a render camera for selected model",
                                        buttonLabel="Execute",
                                        buttonCommand=self.load_model)                                       
        cmds.setParent(menu=True)

        cmds.showWindow(self.window)

    def locator_curve(self,*args):
        # Coordinates of the locator-shaped curve.
        crv = cmds.curve(degree=1,
                     point=[(1, 0, 0),
                            (-1, 0, 0),
                            (0, 0, 0),
                            (0, 1, 0),
                            (0, -1, 0),
                            (0, 0, 0),
                            (0, 0, 1),
                            (0, 0, -1),
                            (0, 0, 0)])
        return crv

    def edit_curve(self,*args):
        parts = self.button1.split(",")
        print parts
        txt_val = cmds.textFieldButtonGrp(self.button1, q=True,text=True)
        print txt_val
        
    def load_model(self, *args):
        pass
        
    def create_camera(self, *args):
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

b_cls = createMyLayoutCls()  
b_cls.show()
