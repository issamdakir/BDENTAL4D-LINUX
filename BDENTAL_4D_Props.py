import bpy
from os.path import abspath

from bpy.props import (
    StringProperty,
    IntProperty,
    FloatProperty,
    EnumProperty,
    FloatVectorProperty,
    BoolProperty,
)

from .Operators.BDENTAL_4D_Utils import *

def text_body_update(self, context):
    props = context.scene.ODC_modops_props
    if context.object:
        ob = context.object
        if ob.type == "FONT":
            mode = ob.mode
            bpy.ops.object.mode_set(mode="OBJECT")
            ob.data.body = props.text_body_prop

            # Check font options and apply them if toggled :
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.font.select_all()

            dict_font_options = {
                "BOLD": props.bold_toggle_prop,
                "ITALIC": props.italic_toggle_prop,
                "UNDERLINE": props.underline_toggle_prop,
            }
            for key, value in dict_font_options.items():
                if value == True:
                    bpy.ops.font.style_toggle(style=key)

            ob.name = ob.data.body
            bpy.ops.object.mode_set(mode=mode)


def text_bold_toggle(self, context):
    if context.object:
        ob = context.object
        if ob.type == "FONT":
            mode = ob.mode
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.font.select_all()
            bpy.ops.font.style_toggle(style="BOLD")
            bpy.ops.object.mode_set(mode=mode)


def text_italic_toggle(self, context):
    if context.object:
        ob = context.object
        if ob.type == "FONT":
            mode = ob.mode
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.font.select_all()
            bpy.ops.font.style_toggle(style="ITALIC")
            bpy.ops.object.mode_set(mode=mode)


def text_underline_toggle(self, context):
    if context.object:
        ob = context.object
        if ob.type == "FONT":
            mode = ob.mode
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.font.select_all()
            bpy.ops.font.style_toggle(style="UNDERLINE")
            bpy.ops.object.mode_set(mode=mode)


class BDENTAL_4D_Props(bpy.types.PropertyGroup):

    #####################
    #############################################################################################
    # CT_Scan props :
    #############################################################################################
    #####################

    UserProjectDir: StringProperty(
        name="Project Directory Path",
        default="",
        description="Project Directory Path",
        subtype="DIR_PATH",
    )

    #####################

    UserDcmDir: StringProperty(
        name="DICOM Path",
        default="",
        description="DICOM Directory Path",
        subtype="DIR_PATH",
    )

    UserImageFile: StringProperty(
        name="User 3D Image File Path",
        default="",
        description="User Image File Path",
        subtype="FILE_PATH",
    )

    #####################

    Data_Types = ["DICOM Series", "3D Image File", ""]
    items = []
    for i in range(len(Data_Types)):
        item = (str(Data_Types[i]), str(Data_Types[i]), str(""), int(i))
        items.append(item)

    DataType: EnumProperty(items=items, description="Data type", default="DICOM Series")

    #######################

    DcmInfo: StringProperty(
        name="(str) DicomInfo",
        default="{'Deffault': None}",
        description="Dicom series files list",
    )
    #######################

    PngDir: StringProperty(
        name="Png Directory",
        default="",
        description=" PNG files Sequence Directory Path",
    )
    #######################

    SlicesDir: StringProperty(
        name="Slices Directory",
        default="",
        description="Slices PNG files Directory Path",
    )
    #######################

    NrrdHuPath: StringProperty(
        name="NrrdHuPath",
        default="",
        description="Nrrd image3D file Path",
    )
    Nrrd255Path: StringProperty(
        name="Nrrd255Path",
        default="",
        description="Nrrd image3D file Path",
    )

    #######################

    IcpVidDict: StringProperty(
        name="IcpVidDict",
        default="None",
        description="ICP Vertices Pairs str(Dict)",
    )
    #######################

    Wmin: IntProperty()
    Wmax: IntProperty()

    #######################
    # SoftTissueMode = BoolProperty(description="SoftTissue Mode ", default=False)

    GroupNodeName: StringProperty(
        name="Group shader Name",
        default="",
        description="Group shader Name",
    )

    #######################

    Treshold: IntProperty(
        name="Treshold",
        description="Volume Treshold",
        default=600,
        min=-400,
        max=3000,
        soft_min=-400,
        soft_max=3000,
        step=1,
        update=BDENTAL4D_Treshold_Prop_UpdateFunction,
    )
    Progress_Bar: FloatProperty(
        name="Progress_Bar",
        description="Progress_Bar",
        subtype="PERCENTAGE",
        default=0.0,
        min=0.0,
        max=100.0,
        soft_min=0.0,
        soft_max=100.0,
        step=1,
        precision=1,
    )
    SoftTreshold: IntProperty(
        name="SOFT TISSU",
        description="Soft Tissu Treshold",
        default=-300,
        min=-400,
        max=3000,
        soft_min=-400,
        soft_max=3000,
        step=1,
    )
    BoneTreshold: IntProperty(
        name="BONE",
        description="Bone Treshold",
        default=600,
        min=-400,
        max=3000,
        soft_min=-400,
        soft_max=3000,
        step=1,
    )
    TeethTreshold: IntProperty(
        name="Teeth Treshold",
        description="Teeth Treshold",
        default=1400,
        min=-400,
        max=3000,
        soft_min=-400,
        soft_max=3000,
        step=1,
    )
    SoftBool: BoolProperty(description="", default=False)
    BoneBool: BoolProperty(description="", default=False)
    TeethBool: BoolProperty(description="", default=False)

    SoftSegmentColor: FloatVectorProperty(
        name="Soft Segmentation Color",
        description="Soft Color",
        default=[0.8, 0.46, 0.4, 1.0],  # [0.63, 0.37, 0.30, 1.0]
        soft_min=0.0,
        soft_max=1.0,
        size=4,
        subtype="COLOR",
    )
    BoneSegmentColor: FloatVectorProperty(
        name="Bone Segmentation Color",
        description="Bone Color",
        default=[0.44, 0.4, 0.5, 1.0],  # (0.8, 0.46, 0.4, 1.0),
        soft_min=0.0,
        soft_max=1.0,
        size=4,
        subtype="COLOR",
    )
    TeethSegmentColor: FloatVectorProperty(
        name="Teeth Segmentation Color",
        description="Teeth Color",
        default=[0.55, 0.645, 0.67, 1.000000],  # (0.8, 0.46, 0.4, 1.0),
        soft_min=0.0,
        soft_max=1.0,
        size=4,
        subtype="COLOR",
    )

    #######################

    CT_Loaded: BoolProperty(description="CT loaded ", default=False)
    CT_Rendered: BoolProperty(description="CT Rendered ", default=False)
    sceneUpdate: BoolProperty(description="scene update ", default=True)
    AlignModalState: BoolProperty(description="Align Modal state ", default=False)

    #######################
    ActiveOperator: StringProperty(
        name="Active Operator",
        default="None",
        description="Active_Operator",
    )
    #######################
    # Guide Components :

    TeethLibList = ["Christian Brenes Teeth Library"]
    items = []
    for i in range(len(TeethLibList)):
        item = (str(TeethLibList[i]), str(TeethLibList[i]), str(""), int(i))
        items.append(item)

    TeethLibrary: EnumProperty(
        items=items,
        description="Teeth Library",
        default="Christian Brenes Teeth Library",
    )

    ImplantLibList = ["BDENTAL4D_Implant_Library"]
    items = []
    for i in range(len(ImplantLibList)):
        item = (str(ImplantLibList[i]), str(ImplantLibList[i]), str(""), int(i))
        items.append(item)

    ImplantLibrary: EnumProperty(
        items=items,
        description="Implant Library",
        default="BDENTAL4D_Implant_Library",
    )
    #######################
    SleeveDiameter: FloatProperty(
        name="Sleeve Diameter",
        description="Sleeve Diameter",
        default=5.0,
        min=0.0,
        max=100.0,
        soft_min=0.0,
        soft_max=100.0,
        step=1,
        precision=1,
    )
    #######################
    SleeveHeight: FloatProperty(
        name="Sleeve Height",
        description="Sleeve Height",
        default=5.0,
        min=0.0,
        max=100.0,
        soft_min=0.0,
        soft_max=100.0,
        step=1,
        precision=1,
    )
    #######################
    HoleDiameter: FloatProperty(
        name="Hole Diameter",
        description="Hole Diameter",
        default=2.0,
        min=0.0,
        max=100.0,
        soft_min=0.0,
        soft_max=100.0,
        step=1,
        precision=1,
    )
    #######################
    HoleOffset: FloatProperty(
        name="Hole Offset",
        description="Sleeve Offset",
        default=0.1,
        min=0.0,
        max=100.0,
        soft_min=0.0,
        soft_max=100.0,
        step=1,
        precision=1,
    )

    #########################################################################################
    # Mesh Tools Props :
    #########################################################################################

    # Decimate ratio prop :
    #######################
    no_material_prop: StringProperty(
        name="No Material",
        default="No Color",
        description="No active material found for active object",
    )
    decimate_ratio: FloatProperty(
        description="Enter decimate ratio ", default=0.5, step=1, precision=2
    )
    #########################################################################################

    CurveCutterNameProp: StringProperty(
        name="Cutter Name",
        default="",
        description="Current Cutter Object Name",
    )

    #####################

    CuttingTargetNameProp: StringProperty(
        name="Cutting Target Name",
        default="",
        description="Current Cutting Target Object Name",
    )

    #####################

    Cutting_Tools_Types = [
        "Curve Cutter 1",
        "Curve Cutter 2",
        "Curve Cutter 3",
        "Square Cutter",
        "Paint Cutter",
    ]
    items = []
    for i in range(len(Cutting_Tools_Types)):
        item = (
            str(Cutting_Tools_Types[i]),
            str(Cutting_Tools_Types[i]),
            str(""),
            int(i),
        )
        items.append(item)

    Cutting_Tools_Types_Prop: EnumProperty(
        items=items, description="Select a cutting tool", default="Curve Cutter 1"
    )

    CurveCutCloseModeList = ["Open Curve", "Close Curve"]
    items = []
    for i in range(len(CurveCutCloseModeList)):
        item = (
            str(CurveCutCloseModeList[i]),
            str(CurveCutCloseModeList[i]),
            str(""),
            int(i),
        )
        items.append(item)
    CurveCutCloseMode: EnumProperty(items=items, description="", default="Close Curve")

    cutting_mode_list = ["Cut inner", "Keep inner"]
    items = []
    for i in range(len(cutting_mode_list)):
        item = (str(cutting_mode_list[i]), str(cutting_mode_list[i]), str(""), int(i))
        items.append(item)

    cutting_mode: EnumProperty(items=items, description="", default="Cut inner")

    TubeWidth: FloatProperty(description="Tube Width ", default=2, step=1, precision=2)

    TubeCloseModeList = ["Open Tube", "Close Tube"]
    items = []
    for i in range(len(TubeCloseModeList)):
        item = (str(TubeCloseModeList[i]), str(TubeCloseModeList[i]), str(""), int(i))
        items.append(item)
    TubeCloseMode: EnumProperty(items=items, description="", default="Close Tube")

    BaseHeight: FloatProperty(
        description="Base Height ", default=10, step=1, precision=2
    )
    SurveyInfo: StringProperty(
        name="Models Survey Local Z",
        default="{}",
        description="Models Survey Local Z",
    )

    #############################################################################################
    # BDENTAL_4D Align Properties :
    #############################################################################################
    IcpVidDict: StringProperty(
        name="IcpVidDict",
        default="None",
        description="ICP Vertices Pairs str(Dict)",
    )

    #######################
    AlignModalState: BoolProperty(description="Align Modal state ", default=False)

    #############################################################################################
    # JTrack Props Properties :
    #############################################################################################
    JTrack_UserProjectDir: StringProperty(
        name="",
        default="",
        description="Location of BDJawTracker project Directory",
        subtype="DIR_PATH",
    )

    CalibImages: StringProperty(
        name="Calibration Images path",
        default="",
        description="Location of calibration Images directory ",
        subtype="DIR_PATH",
    )

    TrackFile: StringProperty(
        name="Video Track File",
        default="",
        description="Location of tracking  Rec video file ",
        subtype="FILE_PATH",
    )

    TrackedData: StringProperty(
        name="",
        default="",
        description="Location tracked data file (.txt)",
        subtype="FILE_PATH",
    )

    UserSquareLength: FloatProperty(
        description="Square length in meters", default=0.0244, step=1, precision=4
    )
    UserMarkerLength: FloatProperty(
        description="Marker length in meters", default=0.0123, step=1, precision=4
    )

    #####################

    # Tracking_Types = ["Precision", "Precision resized(1/2)", "Fast", "Fast resized(1/2)"]
    Tracking_Types = ["Precision", "Fast"]
    items = []
    for i in range(len(Tracking_Types)):
        item = (str(Tracking_Types[i]), str(Tracking_Types[i]), str(""), int(i))
        items.append(item)

    TrackingType: EnumProperty(
        items=items, description="Tracking method", default="Fast"
    )
    BakeLowPlane: BoolProperty(
        name="Enable or Disable Low occlusal plane baking",
        description="Lower occlusal plane baking",
        default=False,
    )

    BakeUpPlane: BoolProperty(
        name="Enable or Disable Up occlusal plane baking",
        description="Upper occlusal plane baking",
        default=False,
    )

    #####################################################################
    # DSD props
    #####################################################################
    Back_ImageFile: StringProperty(
            name="Background Image",
            default="",
            description="Background Image File Path",
            subtype="FILE_PATH",
        )
    DSD_CalibFile: StringProperty(
            name="Calibration File",
            default="",
            description="Calibration File Path",
            subtype="FILE_PATH",
        )

#################################################################################################
# Registration :
#################################################################################################

classes = [
    BDENTAL_4D_Props,
]


def register():

    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.BDENTAL_4D_Props = bpy.props.PointerProperty(type=BDENTAL_4D_Props)


def unregister():

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.BDENTAL_4D_Props


# props examples :

# Axial_Loc: FloatVectorProperty(
#     name="AXIAL location",
#     description="AXIAL location",
#     subtype="TRANSLATION",
#     update=AxialSliceUpdate,
# )
# Axial_Rot: FloatVectorProperty(
#     name="AXIAL Rotation",
#     description="AXIAL Rotation",
#     subtype="EULER",
#     update=AxialSliceUpdate,
# )
################################################
# Str_Prop_Search_1: StringProperty(
#     name="String Search Property 1",
#     default="",
#     description="Str_Prop_Search_1",
# )
# Float Props :
#########################################################################################

# F_Prop_1: FloatProperty(
#     description="Float Property 1 ",
#     default=0.0,
#     min=-200.0,
#     max=200.0,
#     step=1,
#     precision=1,
#     unit="NONE",
#     update=None,
#     get=None,
#     set=None,
# )
#########################################################################################
# # FloatVector Props :
#     ##############################################
#     FloatV_Prop_1: FloatVectorProperty(
#         name="FloatVectorProperty 1", description="FloatVectorProperty 1", size=3
#     )
#########################################################################################
