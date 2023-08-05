from typing import Iterable, Type, Tuple
import ctypes


def iterate(data: ctypes.c_void_p, t: Type[ctypes.Structure], count: int)->Iterable[ctypes.Structure]:
    p = ctypes.cast(data, ctypes.POINTER(t))
    for i in range(count):
        yield p[i]


class ImVector(ctypes.Structure):
    _fields_ = (
        ('Size', ctypes.c_int),
        ('Capacity', ctypes.c_int),
        ('Data', ctypes.c_void_p),
    )

    def each(self, t: Type[ctypes.Structure])->Iterable[ctypes.Structure]:
        return iterate(self.Data, t, self.Size)

class ImVec2(ctypes.Structure):
    _fields_=[
        ("x", ctypes.c_float), # FloatType: float
        ("y", ctypes.c_float), # FloatType: float
    ]

    def __iter__(self):
        yield self.x
        yield self.y

class ImVec4(ctypes.Structure):
    _fields_=[
        ("x", ctypes.c_float), # FloatType: float
        ("y", ctypes.c_float), # FloatType: float
        ("z", ctypes.c_float), # FloatType: float
        ("w", ctypes.c_float), # FloatType: float
    ]

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.w
        yield self.h

class ImFont(ctypes.Structure):
    pass

class ImFontConfig(ctypes.Structure):
    _fields_=[
        ("FontData", ctypes.c_void_p), # PointerType: void*
        ("FontDataSize", ctypes.c_int32), # Int32Type: int
        ("FontDataOwnedByAtlas", ctypes.c_bool), # BoolType: bool
        ("FontNo", ctypes.c_int32), # Int32Type: int
        ("SizePixels", ctypes.c_float), # FloatType: float
        ("OversampleH", ctypes.c_int32), # Int32Type: int
        ("OversampleV", ctypes.c_int32), # Int32Type: int
        ("PixelSnapH", ctypes.c_bool), # BoolType: bool
        ("GlyphExtraSpacing", ImVec2), # ImVec2WrapType: ImVec2
        ("GlyphOffset", ImVec2), # ImVec2WrapType: ImVec2
        ("GlyphRanges", ctypes.c_void_p), # PointerType: unsigned short*
        ("GlyphMinAdvanceX", ctypes.c_float), # FloatType: float
        ("GlyphMaxAdvanceX", ctypes.c_float), # FloatType: float
        ("MergeMode", ctypes.c_bool), # BoolType: bool
        ("FontBuilderFlags", ctypes.c_uint32), # UInt32Type: unsigned int
        ("RasterizerMultiply", ctypes.c_float), # FloatType: float
        ("EllipsisChar", ctypes.c_uint16), # UInt16Type: unsigned short
        ("Name", ctypes.c_int8 * 40), # ArrayType: char[40]
        ("DstFont", ctypes.c_void_p), # PointerToStructType: ImFont*
    ]

class ImFontAtlasCustomRect(ctypes.Structure):
    _fields_=[
        ("Width", ctypes.c_uint16), # UInt16Type: unsigned short
        ("Height", ctypes.c_uint16), # UInt16Type: unsigned short
        ("X", ctypes.c_uint16), # UInt16Type: unsigned short
        ("Y", ctypes.c_uint16), # UInt16Type: unsigned short
        ("GlyphID", ctypes.c_uint32), # UInt32Type: unsigned int
        ("GlyphAdvanceX", ctypes.c_float), # FloatType: float
        ("GlyphOffset", ImVec2), # ImVec2WrapType: ImVec2
        ("Font", ctypes.c_void_p), # PointerToStructType: ImFont*
    ]

class ImFontAtlas(ctypes.Structure):
    _fields_=[
        ("Flags", ctypes.c_int32), # Int32Type: int
        ("TexID", ctypes.c_void_p), # PointerType: void*
        ("TexDesiredWidth", ctypes.c_int32), # Int32Type: int
        ("TexGlyphPadding", ctypes.c_int32), # Int32Type: int
        ("Locked", ctypes.c_bool), # BoolType: bool
        ("TexReady", ctypes.c_bool), # BoolType: bool
        ("TexPixelsUseColors", ctypes.c_bool), # BoolType: bool
        ("TexPixelsAlpha8", ctypes.c_void_p), # PointerType: unsigned char*
        ("TexPixelsRGBA32", ctypes.c_void_p), # PointerType: unsigned int*
        ("TexWidth", ctypes.c_int32), # Int32Type: int
        ("TexHeight", ctypes.c_int32), # Int32Type: int
        ("TexUvScale", ImVec2), # ImVec2WrapType: ImVec2
        ("TexUvWhitePixel", ImVec2), # ImVec2WrapType: ImVec2
        ("Fonts", ImVector), # ImVector: ImVector
        ("CustomRects", ImVector), # ImVector: ImVector
        ("ConfigData", ImVector), # ImVector: ImVector
        ("TexUvLines", ImVec4 * 64), # ArrayType: ImVec4[64]
        ("FontBuilderIO", ctypes.c_void_p), # PointerType: ImFontBuilderIO*
        ("FontBuilderFlags", ctypes.c_uint32), # UInt32Type: unsigned int
        ("PackIdMouseCursors", ctypes.c_int32), # Int32Type: int
        ("PackIdLines", ctypes.c_int32), # Int32Type: int
    ]

    def AddFont(self, *args)->ImFont:
        from . import impl
        return impl.ImFontAtlas_AddFont(self, *args)
    def AddFontDefault(self, *args)->ImFont:
        from . import impl
        return impl.ImFontAtlas_AddFontDefault(self, *args)
    def AddFontFromFileTTF(self, *args)->ImFont:
        from . import impl
        return impl.ImFontAtlas_AddFontFromFileTTF(self, *args)
    def AddFontFromMemoryTTF(self, *args)->ImFont:
        from . import impl
        return impl.ImFontAtlas_AddFontFromMemoryTTF(self, *args)
    def AddFontFromMemoryCompressedTTF(self, *args)->ImFont:
        from . import impl
        return impl.ImFontAtlas_AddFontFromMemoryCompressedTTF(self, *args)
    def AddFontFromMemoryCompressedBase85TTF(self, *args)->ImFont:
        from . import impl
        return impl.ImFontAtlas_AddFontFromMemoryCompressedBase85TTF(self, *args)
    def ClearInputData(self, *args)->None:
        from . import impl
        return impl.ImFontAtlas_ClearInputData(self, *args)
    def ClearTexData(self, *args)->None:
        from . import impl
        return impl.ImFontAtlas_ClearTexData(self, *args)
    def ClearFonts(self, *args)->None:
        from . import impl
        return impl.ImFontAtlas_ClearFonts(self, *args)
    def Clear(self, *args)->None:
        from . import impl
        return impl.ImFontAtlas_Clear(self, *args)
    def Build(self, *args)->ctypes.c_bool:
        from . import impl
        return impl.ImFontAtlas_Build(self, *args)
    def GetTexDataAsAlpha8(self, *args)->None:
        from . import impl
        return impl.ImFontAtlas_GetTexDataAsAlpha8(self, *args)
    def GetTexDataAsRGBA32(self, *args)->None:
        from . import impl
        return impl.ImFontAtlas_GetTexDataAsRGBA32(self, *args)
    def IsBuilt(self, *args)->ctypes.c_bool:
        from . import impl
        return impl.ImFontAtlas_IsBuilt(self, *args)
    def SetTexID(self, *args)->None:
        from . import impl
        return impl.ImFontAtlas_SetTexID(self, *args)
    def GetGlyphRangesDefault(self, *args)->ctypes.c_void_p:
        from . import impl
        return impl.ImFontAtlas_GetGlyphRangesDefault(self, *args)
    def GetGlyphRangesKorean(self, *args)->ctypes.c_void_p:
        from . import impl
        return impl.ImFontAtlas_GetGlyphRangesKorean(self, *args)
    def GetGlyphRangesJapanese(self, *args)->ctypes.c_void_p:
        from . import impl
        return impl.ImFontAtlas_GetGlyphRangesJapanese(self, *args)
    def GetGlyphRangesChineseFull(self, *args)->ctypes.c_void_p:
        from . import impl
        return impl.ImFontAtlas_GetGlyphRangesChineseFull(self, *args)
    def GetGlyphRangesChineseSimplifiedCommon(self, *args)->ctypes.c_void_p:
        from . import impl
        return impl.ImFontAtlas_GetGlyphRangesChineseSimplifiedCommon(self, *args)
    def GetGlyphRangesCyrillic(self, *args)->ctypes.c_void_p:
        from . import impl
        return impl.ImFontAtlas_GetGlyphRangesCyrillic(self, *args)
    def GetGlyphRangesThai(self, *args)->ctypes.c_void_p:
        from . import impl
        return impl.ImFontAtlas_GetGlyphRangesThai(self, *args)
    def GetGlyphRangesVietnamese(self, *args)->ctypes.c_void_p:
        from . import impl
        return impl.ImFontAtlas_GetGlyphRangesVietnamese(self, *args)
    def AddCustomRectRegular(self, *args)->ctypes.c_int32:
        from . import impl
        return impl.ImFontAtlas_AddCustomRectRegular(self, *args)
    def AddCustomRectFontGlyph(self, *args)->ctypes.c_int32:
        from . import impl
        return impl.ImFontAtlas_AddCustomRectFontGlyph(self, *args)
    def GetCustomRectByIndex(self, *args)->ImFontAtlasCustomRect:
        from . import impl
        return impl.ImFontAtlas_GetCustomRectByIndex(self, *args)
    def CalcCustomRectUV(self, *args)->None:
        from . import impl
        return impl.ImFontAtlas_CalcCustomRectUV(self, *args)
    def GetMouseCursorTexData(self, *args)->ctypes.c_bool:
        from . import impl
        return impl.ImFontAtlas_GetMouseCursorTexData(self, *args)
class ImGuiIO(ctypes.Structure):
    _fields_=[
        ("ConfigFlags", ctypes.c_int32), # Int32Type: int
        ("BackendFlags", ctypes.c_int32), # Int32Type: int
        ("DisplaySize", ImVec2), # ImVec2WrapType: ImVec2
        ("DeltaTime", ctypes.c_float), # FloatType: float
        ("IniSavingRate", ctypes.c_float), # FloatType: float
        ("IniFilename", ctypes.c_void_p), # CStringType: const char *
        ("LogFilename", ctypes.c_void_p), # CStringType: const char *
        ("MouseDoubleClickTime", ctypes.c_float), # FloatType: float
        ("MouseDoubleClickMaxDist", ctypes.c_float), # FloatType: float
        ("MouseDragThreshold", ctypes.c_float), # FloatType: float
        ("KeyMap", ctypes.c_int32 * 22), # ArrayType: int[22]
        ("KeyRepeatDelay", ctypes.c_float), # FloatType: float
        ("KeyRepeatRate", ctypes.c_float), # FloatType: float
        ("UserData", ctypes.c_void_p), # PointerType: void*
        ("_Fonts", ctypes.c_void_p), # PointerToStructType: ImFontAtlas*
        ("FontGlobalScale", ctypes.c_float), # FloatType: float
        ("FontAllowUserScaling", ctypes.c_bool), # BoolType: bool
        ("FontDefault", ctypes.c_void_p), # PointerToStructType: ImFont*
        ("DisplayFramebufferScale", ImVec2), # ImVec2WrapType: ImVec2
        ("ConfigDockingNoSplit", ctypes.c_bool), # BoolType: bool
        ("ConfigDockingWithShift", ctypes.c_bool), # BoolType: bool
        ("ConfigDockingAlwaysTabBar", ctypes.c_bool), # BoolType: bool
        ("ConfigDockingTransparentPayload", ctypes.c_bool), # BoolType: bool
        ("ConfigViewportsNoAutoMerge", ctypes.c_bool), # BoolType: bool
        ("ConfigViewportsNoTaskBarIcon", ctypes.c_bool), # BoolType: bool
        ("ConfigViewportsNoDecoration", ctypes.c_bool), # BoolType: bool
        ("ConfigViewportsNoDefaultParent", ctypes.c_bool), # BoolType: bool
        ("MouseDrawCursor", ctypes.c_bool), # BoolType: bool
        ("ConfigMacOSXBehaviors", ctypes.c_bool), # BoolType: bool
        ("ConfigInputTextCursorBlink", ctypes.c_bool), # BoolType: bool
        ("ConfigDragClickToInputText", ctypes.c_bool), # BoolType: bool
        ("ConfigWindowsResizeFromEdges", ctypes.c_bool), # BoolType: bool
        ("ConfigWindowsMoveFromTitleBarOnly", ctypes.c_bool), # BoolType: bool
        ("ConfigMemoryCompactTimer", ctypes.c_float), # FloatType: float
        ("BackendPlatformName", ctypes.c_void_p), # CStringType: const char *
        ("BackendRendererName", ctypes.c_void_p), # CStringType: const char *
        ("BackendPlatformUserData", ctypes.c_void_p), # PointerType: void*
        ("BackendRendererUserData", ctypes.c_void_p), # PointerType: void*
        ("BackendLanguageUserData", ctypes.c_void_p), # PointerType: void*
        ("GetClipboardTextFn", ctypes.c_void_p), # PointerType: void**
        ("SetClipboardTextFn", ctypes.c_void_p), # PointerType: void**
        ("ClipboardUserData", ctypes.c_void_p), # PointerType: void*
        ("MousePos", ImVec2), # ImVec2WrapType: ImVec2
        ("MouseDown", ctypes.c_bool * 5), # ArrayType: bool[5]
        ("MouseWheel", ctypes.c_float), # FloatType: float
        ("MouseWheelH", ctypes.c_float), # FloatType: float
        ("MouseHoveredViewport", ctypes.c_uint32), # UInt32Type: unsigned int
        ("KeyCtrl", ctypes.c_bool), # BoolType: bool
        ("KeyShift", ctypes.c_bool), # BoolType: bool
        ("KeyAlt", ctypes.c_bool), # BoolType: bool
        ("KeySuper", ctypes.c_bool), # BoolType: bool
        ("KeysDown", ctypes.c_bool * 512), # ArrayType: bool[512]
        ("NavInputs", ctypes.c_float * 20), # ArrayType: float[20]
        ("WantCaptureMouse", ctypes.c_bool), # BoolType: bool
        ("WantCaptureKeyboard", ctypes.c_bool), # BoolType: bool
        ("WantTextInput", ctypes.c_bool), # BoolType: bool
        ("WantSetMousePos", ctypes.c_bool), # BoolType: bool
        ("WantSaveIniSettings", ctypes.c_bool), # BoolType: bool
        ("NavActive", ctypes.c_bool), # BoolType: bool
        ("NavVisible", ctypes.c_bool), # BoolType: bool
        ("Framerate", ctypes.c_float), # FloatType: float
        ("MetricsRenderVertices", ctypes.c_int32), # Int32Type: int
        ("MetricsRenderIndices", ctypes.c_int32), # Int32Type: int
        ("MetricsRenderWindows", ctypes.c_int32), # Int32Type: int
        ("MetricsActiveWindows", ctypes.c_int32), # Int32Type: int
        ("MetricsActiveAllocations", ctypes.c_int32), # Int32Type: int
        ("MouseDelta", ImVec2), # ImVec2WrapType: ImVec2
        ("WantCaptureMouseUnlessPopupClose", ctypes.c_bool), # BoolType: bool
        ("KeyMods", ctypes.c_int32), # Int32Type: int
        ("KeyModsPrev", ctypes.c_int32), # Int32Type: int
        ("MousePosPrev", ImVec2), # ImVec2WrapType: ImVec2
        ("MouseClickedPos", ImVec2 * 5), # ArrayType: ImVec2[5]
        ("MouseClickedTime", ctypes.c_double * 5), # ArrayType: double[5]
        ("MouseClicked", ctypes.c_bool * 5), # ArrayType: bool[5]
        ("MouseDoubleClicked", ctypes.c_bool * 5), # ArrayType: bool[5]
        ("MouseClickedCount", ctypes.c_uint16 * 5), # ArrayType: unsigned short[5]
        ("MouseClickedLastCount", ctypes.c_uint16 * 5), # ArrayType: unsigned short[5]
        ("MouseReleased", ctypes.c_bool * 5), # ArrayType: bool[5]
        ("MouseDownOwned", ctypes.c_bool * 5), # ArrayType: bool[5]
        ("MouseDownOwnedUnlessPopupClose", ctypes.c_bool * 5), # ArrayType: bool[5]
        ("MouseDownDuration", ctypes.c_float * 5), # ArrayType: float[5]
        ("MouseDownDurationPrev", ctypes.c_float * 5), # ArrayType: float[5]
        ("MouseDragMaxDistanceAbs", ImVec2 * 5), # ArrayType: ImVec2[5]
        ("MouseDragMaxDistanceSqr", ctypes.c_float * 5), # ArrayType: float[5]
        ("KeysDownDuration", ctypes.c_float * 512), # ArrayType: float[512]
        ("KeysDownDurationPrev", ctypes.c_float * 512), # ArrayType: float[512]
        ("NavInputsDownDuration", ctypes.c_float * 20), # ArrayType: float[20]
        ("NavInputsDownDurationPrev", ctypes.c_float * 20), # ArrayType: float[20]
        ("PenPressure", ctypes.c_float), # FloatType: float
        ("AppFocusLost", ctypes.c_bool), # BoolType: bool
        ("InputQueueSurrogate", ctypes.c_uint16), # UInt16Type: unsigned short
        ("InputQueueCharacters", ImVector), # ImVector: ImVector
    ]

    @property
    def Fonts(self)->'ImFontAtlas':
        return ctypes.cast(ctypes.c_void_p(self._Fonts), ctypes.POINTER(ImFontAtlas))[0]

class ImGuiContext(ctypes.Structure):
    pass

class ImDrawCmd(ctypes.Structure):
    _fields_=[
        ("ClipRect", ImVec4), # ImVec4WrapType: ImVec4
        ("TextureId", ctypes.c_void_p), # PointerType: void*
        ("VtxOffset", ctypes.c_uint32), # UInt32Type: unsigned int
        ("IdxOffset", ctypes.c_uint32), # UInt32Type: unsigned int
        ("ElemCount", ctypes.c_uint32), # UInt32Type: unsigned int
        ("UserCallback", ctypes.c_void_p), # TypedefType: ImDrawCallback
        ("UserCallbackData", ctypes.c_void_p), # PointerType: void*
    ]

class ImDrawData(ctypes.Structure):
    _fields_=[
        ("Valid", ctypes.c_bool), # BoolType: bool
        ("CmdListsCount", ctypes.c_int32), # Int32Type: int
        ("TotalIdxCount", ctypes.c_int32), # Int32Type: int
        ("TotalVtxCount", ctypes.c_int32), # Int32Type: int
        ("CmdLists", ctypes.c_void_p), # PointerType: ImDrawList**
        ("DisplayPos", ImVec2), # ImVec2WrapType: ImVec2
        ("DisplaySize", ImVec2), # ImVec2WrapType: ImVec2
        ("FramebufferScale", ImVec2), # ImVec2WrapType: ImVec2
        ("OwnerViewport", ctypes.c_void_p), # PointerToStructType: ImGuiViewport*
    ]

class ImDrawListSplitter(ctypes.Structure):
    _fields_=[
        ("_Current", ctypes.c_int32), # Int32Type: int
        ("_Count", ctypes.c_int32), # Int32Type: int
        ("_Channels", ImVector), # ImVector: ImVector
    ]

class ImDrawCmdHeader(ctypes.Structure):
    _fields_=[
        ("ClipRect", ImVec4), # ImVec4WrapType: ImVec4
        ("TextureId", ctypes.c_void_p), # PointerType: void*
        ("VtxOffset", ctypes.c_uint32), # UInt32Type: unsigned int
    ]

class ImDrawList(ctypes.Structure):
    _fields_=[
        ("CmdBuffer", ImVector), # ImVector: ImVector
        ("IdxBuffer", ImVector), # ImVector: ImVector
        ("VtxBuffer", ImVector), # ImVector: ImVector
        ("Flags", ctypes.c_int32), # Int32Type: int
        ("_VtxCurrentIdx", ctypes.c_uint32), # UInt32Type: unsigned int
        ("_Data", ctypes.c_void_p), # PointerType: ImDrawListSharedData*
        ("_OwnerName", ctypes.c_void_p), # CStringType: const char *
        ("_VtxWritePtr", ctypes.c_void_p), # PointerType: ImDrawVert*
        ("_IdxWritePtr", ctypes.c_void_p), # PointerType: unsigned short*
        ("_ClipRectStack", ImVector), # ImVector: ImVector
        ("_TextureIdStack", ImVector), # ImVector: ImVector
        ("_Path", ImVector), # ImVector: ImVector
        ("_CmdHeader", ImDrawCmdHeader), # StructType: ImDrawCmdHeader
        ("_Splitter", ImDrawListSplitter), # StructType: ImDrawListSplitter
        ("_FringeScale", ctypes.c_float), # FloatType: float
    ]

class ImGuiViewport(ctypes.Structure):
    _fields_=[
        ("ID", ctypes.c_uint32), # UInt32Type: unsigned int
        ("Flags", ctypes.c_int32), # Int32Type: int
        ("Pos", ImVec2), # ImVec2WrapType: ImVec2
        ("Size", ImVec2), # ImVec2WrapType: ImVec2
        ("WorkPos", ImVec2), # ImVec2WrapType: ImVec2
        ("WorkSize", ImVec2), # ImVec2WrapType: ImVec2
        ("DpiScale", ctypes.c_float), # FloatType: float
        ("ParentViewportId", ctypes.c_uint32), # UInt32Type: unsigned int
        ("DrawData", ctypes.c_void_p), # PointerToStructType: ImDrawData*
        ("RendererUserData", ctypes.c_void_p), # PointerType: void*
        ("PlatformUserData", ctypes.c_void_p), # PointerType: void*
        ("PlatformHandle", ctypes.c_void_p), # PointerType: void*
        ("PlatformHandleRaw", ctypes.c_void_p), # PointerType: void*
        ("PlatformRequestMove", ctypes.c_bool), # BoolType: bool
        ("PlatformRequestResize", ctypes.c_bool), # BoolType: bool
        ("PlatformRequestClose", ctypes.c_bool), # BoolType: bool
    ]

    def GetCenter(self, *args)->Tuple[float, float]:
        from . import impl
        return impl.ImGuiViewport_GetCenter(self, *args)
    def GetWorkCenter(self, *args)->Tuple[float, float]:
        from . import impl
        return impl.ImGuiViewport_GetWorkCenter(self, *args)
class ImGuiStyle(ctypes.Structure):
    pass

class ImGuiWindowClass(ctypes.Structure):
    pass

from typing import Iterable, Type, Tuple
import ctypes


def iterate(data: ctypes.c_void_p, t: Type[ctypes.Structure], count: int)->Iterable[ctypes.Structure]:
    p = ctypes.cast(data, ctypes.POINTER(t))
    for i in range(count):
        yield p[i]


class ImVector(ctypes.Structure):
    _fields_ = (
        ('Size', ctypes.c_int),
        ('Capacity', ctypes.c_int),
        ('Data', ctypes.c_void_p),
    )

    def each(self, t: Type[ctypes.Structure])->Iterable[ctypes.Structure]:
        return iterate(self.Data, t, self.Size)

