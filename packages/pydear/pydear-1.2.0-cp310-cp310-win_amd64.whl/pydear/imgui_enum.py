from enum import IntEnum

class ImGuiWindowFlags_(IntEnum):
    NONE = 0x0
    NoTitleBar = 0x1
    NoResize = 0x2
    NoMove = 0x4
    NoScrollbar = 0x8
    NoScrollWithMouse = 0x10
    NoCollapse = 0x20
    AlwaysAutoResize = 0x40
    NoBackground = 0x80
    NoSavedSettings = 0x100
    NoMouseInputs = 0x200
    MenuBar = 0x400
    HorizontalScrollbar = 0x800
    NoFocusOnAppearing = 0x1000
    NoBringToFrontOnFocus = 0x2000
    AlwaysVerticalScrollbar = 0x4000
    AlwaysHorizontalScrollbar = 0x8000
    AlwaysUseWindowPadding = 0x10000
    NoNavInputs = 0x40000
    NoNavFocus = 0x80000
    UnsavedDocument = 0x100000
    NoDocking = 0x200000
    NoNav = 0xc0000
    NoDecoration = 0x2b
    NoInputs = 0xc0200
    NavFlattened = 0x800000
    ChildWindow = 0x1000000
    Tooltip = 0x2000000
    Popup = 0x4000000
    Modal = 0x8000000
    ChildMenu = 0x10000000
    DockNodeHost = 0x20000000

class ImGuiInputTextFlags_(IntEnum):
    NONE = 0x0
    CharsDecimal = 0x1
    CharsHexadecimal = 0x2
    CharsUppercase = 0x4
    CharsNoBlank = 0x8
    AutoSelectAll = 0x10
    EnterReturnsTrue = 0x20
    CallbackCompletion = 0x40
    CallbackHistory = 0x80
    CallbackAlways = 0x100
    CallbackCharFilter = 0x200
    AllowTabInput = 0x400
    CtrlEnterForNewLine = 0x800
    NoHorizontalScroll = 0x1000
    AlwaysOverwrite = 0x2000
    ReadOnly = 0x4000
    Password = 0x8000
    NoUndoRedo = 0x10000
    CharsScientific = 0x20000
    CallbackResize = 0x40000
    CallbackEdit = 0x80000
    AlwaysInsertMode = 0x2000

class ImGuiTreeNodeFlags_(IntEnum):
    NONE = 0x0
    Selected = 0x1
    Framed = 0x2
    AllowItemOverlap = 0x4
    NoTreePushOnOpen = 0x8
    NoAutoOpenOnLog = 0x10
    DefaultOpen = 0x20
    OpenOnDoubleClick = 0x40
    OpenOnArrow = 0x80
    Leaf = 0x100
    Bullet = 0x200
    FramePadding = 0x400
    SpanAvailWidth = 0x800
    SpanFullWidth = 0x1000
    NavLeftJumpsBackHere = 0x2000
    CollapsingHeader = 0x1a

class ImGuiPopupFlags_(IntEnum):
    NONE = 0x0
    MouseButtonLeft = 0x0
    MouseButtonRight = 0x1
    MouseButtonMiddle = 0x2
    MouseButtonMask_ = 0x1f
    MouseButtonDefault_ = 0x1
    NoOpenOverExistingPopup = 0x20
    NoOpenOverItems = 0x40
    AnyPopupId = 0x80
    AnyPopupLevel = 0x100
    AnyPopup = 0x180

class ImGuiSelectableFlags_(IntEnum):
    NONE = 0x0
    DontClosePopups = 0x1
    SpanAllColumns = 0x2
    AllowDoubleClick = 0x4
    Disabled = 0x8
    AllowItemOverlap = 0x10

class ImGuiComboFlags_(IntEnum):
    NONE = 0x0
    PopupAlignLeft = 0x1
    HeightSmall = 0x2
    HeightRegular = 0x4
    HeightLarge = 0x8
    HeightLargest = 0x10
    NoArrowButton = 0x20
    NoPreview = 0x40
    HeightMask_ = 0x1e

class ImGuiTabBarFlags_(IntEnum):
    NONE = 0x0
    Reorderable = 0x1
    AutoSelectNewTabs = 0x2
    TabListPopupButton = 0x4
    NoCloseWithMiddleMouseButton = 0x8
    NoTabListScrollingButtons = 0x10
    NoTooltip = 0x20
    FittingPolicyResizeDown = 0x40
    FittingPolicyScroll = 0x80
    FittingPolicyMask_ = 0xc0
    FittingPolicyDefault_ = 0x40

class ImGuiTabItemFlags_(IntEnum):
    NONE = 0x0
    UnsavedDocument = 0x1
    SetSelected = 0x2
    NoCloseWithMiddleMouseButton = 0x4
    NoPushId = 0x8
    NoTooltip = 0x10
    NoReorder = 0x20
    Leading = 0x40
    Trailing = 0x80

class ImGuiTableFlags_(IntEnum):
    NONE = 0x0
    Resizable = 0x1
    Reorderable = 0x2
    Hideable = 0x4
    Sortable = 0x8
    NoSavedSettings = 0x10
    ContextMenuInBody = 0x20
    RowBg = 0x40
    BordersInnerH = 0x80
    BordersOuterH = 0x100
    BordersInnerV = 0x200
    BordersOuterV = 0x400
    BordersH = 0x180
    BordersV = 0x600
    BordersInner = 0x280
    BordersOuter = 0x500
    Borders = 0x780
    NoBordersInBody = 0x800
    NoBordersInBodyUntilResize = 0x1000
    SizingFixedFit = 0x2000
    SizingFixedSame = 0x4000
    SizingStretchProp = 0x6000
    SizingStretchSame = 0x8000
    NoHostExtendX = 0x10000
    NoHostExtendY = 0x20000
    NoKeepColumnsVisible = 0x40000
    PreciseWidths = 0x80000
    NoClip = 0x100000
    PadOuterX = 0x200000
    NoPadOuterX = 0x400000
    NoPadInnerX = 0x800000
    ScrollX = 0x1000000
    ScrollY = 0x2000000
    SortMulti = 0x4000000
    SortTristate = 0x8000000
    SizingMask_ = 0xe000

class ImGuiTableColumnFlags_(IntEnum):
    NONE = 0x0
    Disabled = 0x1
    DefaultHide = 0x2
    DefaultSort = 0x4
    WidthStretch = 0x8
    WidthFixed = 0x10
    NoResize = 0x20
    NoReorder = 0x40
    NoHide = 0x80
    NoClip = 0x100
    NoSort = 0x200
    NoSortAscending = 0x400
    NoSortDescending = 0x800
    NoHeaderLabel = 0x1000
    NoHeaderWidth = 0x2000
    PreferSortAscending = 0x4000
    PreferSortDescending = 0x8000
    IndentEnable = 0x10000
    IndentDisable = 0x20000
    IsEnabled = 0x1000000
    IsVisible = 0x2000000
    IsSorted = 0x4000000
    IsHovered = 0x8000000
    WidthMask_ = 0x18
    IndentMask_ = 0x30000
    StatusMask_ = 0xf000000
    NoDirectResize_ = 0x40000000

class ImGuiTableRowFlags_(IntEnum):
    NONE = 0x0
    Headers = 0x1

class ImGuiTableBgTarget_(IntEnum):
    NONE = 0x0
    RowBg0 = 0x1
    RowBg1 = 0x2
    CellBg = 0x3

class ImGuiFocusedFlags_(IntEnum):
    NONE = 0x0
    ChildWindows = 0x1
    RootWindow = 0x2
    AnyWindow = 0x4
    NoPopupHierarchy = 0x8
    DockHierarchy = 0x10
    RootAndChildWindows = 0x3

class ImGuiHoveredFlags_(IntEnum):
    NONE = 0x0
    ChildWindows = 0x1
    RootWindow = 0x2
    AnyWindow = 0x4
    NoPopupHierarchy = 0x8
    DockHierarchy = 0x10
    AllowWhenBlockedByPopup = 0x20
    AllowWhenBlockedByActiveItem = 0x80
    AllowWhenOverlapped = 0x100
    AllowWhenDisabled = 0x200
    RectOnly = 0x1a0
    RootAndChildWindows = 0x3

class ImGuiDockNodeFlags_(IntEnum):
    NONE = 0x0
    KeepAliveOnly = 0x1
    NoDockingInCentralNode = 0x4
    PassthruCentralNode = 0x8
    NoSplit = 0x10
    NoResize = 0x20
    AutoHideTabBar = 0x40

class ImGuiDragDropFlags_(IntEnum):
    NONE = 0x0
    SourceNoPreviewTooltip = 0x1
    SourceNoDisableHover = 0x2
    SourceNoHoldToOpenOthers = 0x4
    SourceAllowNullID = 0x8
    SourceExtern = 0x10
    SourceAutoExpirePayload = 0x20
    AcceptBeforeDelivery = 0x400
    AcceptNoDrawDefaultRect = 0x800
    AcceptNoPreviewTooltip = 0x1000
    AcceptPeekOnly = 0xc00

class ImGuiDataType_(IntEnum):
    S8 = 0x0
    U8 = 0x1
    S16 = 0x2
    U16 = 0x3
    S32 = 0x4
    U32 = 0x5
    S64 = 0x6
    U64 = 0x7
    Float = 0x8
    Double = 0x9
    COUNT = 0xa

class ImGuiDir_(IntEnum):
    NONE = -0x1
    Left = 0x0
    Right = 0x1
    Up = 0x2
    Down = 0x3
    COUNT = 0x4

class ImGuiSortDirection_(IntEnum):
    NONE = 0x0
    Ascending = 0x1
    Descending = 0x2

class ImGuiKey_(IntEnum):
    Tab = 0x0
    LeftArrow = 0x1
    RightArrow = 0x2
    UpArrow = 0x3
    DownArrow = 0x4
    PageUp = 0x5
    PageDown = 0x6
    Home = 0x7
    End = 0x8
    Insert = 0x9
    Delete = 0xa
    Backspace = 0xb
    Space = 0xc
    Enter = 0xd
    Escape = 0xe
    KeyPadEnter = 0xf
    A = 0x10
    C = 0x11
    V = 0x12
    X = 0x13
    Y = 0x14
    Z = 0x15
    COUNT = 0x16

class ImGuiKeyModFlags_(IntEnum):
    NONE = 0x0
    Ctrl = 0x1
    Shift = 0x2
    Alt = 0x4
    Super = 0x8

class ImGuiNavInput_(IntEnum):
    Activate = 0x0
    Cancel = 0x1
    Input = 0x2
    Menu = 0x3
    DpadLeft = 0x4
    DpadRight = 0x5
    DpadUp = 0x6
    DpadDown = 0x7
    LStickLeft = 0x8
    LStickRight = 0x9
    LStickUp = 0xa
    LStickDown = 0xb
    FocusPrev = 0xc
    FocusNext = 0xd
    TweakSlow = 0xe
    TweakFast = 0xf
    KeyLeft_ = 0x10
    KeyRight_ = 0x11
    KeyUp_ = 0x12
    KeyDown_ = 0x13
    COUNT = 0x14
    InternalStart_ = 0x10

class ImGuiConfigFlags_(IntEnum):
    NONE = 0x0
    NavEnableKeyboard = 0x1
    NavEnableGamepad = 0x2
    NavEnableSetMousePos = 0x4
    NavNoCaptureKeyboard = 0x8
    NoMouse = 0x10
    NoMouseCursorChange = 0x20
    DockingEnable = 0x40
    ViewportsEnable = 0x400
    DpiEnableScaleViewports = 0x4000
    DpiEnableScaleFonts = 0x8000
    IsSRGB = 0x100000
    IsTouchScreen = 0x200000

class ImGuiBackendFlags_(IntEnum):
    NONE = 0x0
    HasGamepad = 0x1
    HasMouseCursors = 0x2
    HasSetMousePos = 0x4
    RendererHasVtxOffset = 0x8
    PlatformHasViewports = 0x400
    HasMouseHoveredViewport = 0x800
    RendererHasViewports = 0x1000

class ImGuiCol_(IntEnum):
    Text = 0x0
    TextDisabled = 0x1
    WindowBg = 0x2
    ChildBg = 0x3
    PopupBg = 0x4
    Border = 0x5
    BorderShadow = 0x6
    FrameBg = 0x7
    FrameBgHovered = 0x8
    FrameBgActive = 0x9
    TitleBg = 0xa
    TitleBgActive = 0xb
    TitleBgCollapsed = 0xc
    MenuBarBg = 0xd
    ScrollbarBg = 0xe
    ScrollbarGrab = 0xf
    ScrollbarGrabHovered = 0x10
    ScrollbarGrabActive = 0x11
    CheckMark = 0x12
    SliderGrab = 0x13
    SliderGrabActive = 0x14
    Button = 0x15
    ButtonHovered = 0x16
    ButtonActive = 0x17
    Header = 0x18
    HeaderHovered = 0x19
    HeaderActive = 0x1a
    Separator = 0x1b
    SeparatorHovered = 0x1c
    SeparatorActive = 0x1d
    ResizeGrip = 0x1e
    ResizeGripHovered = 0x1f
    ResizeGripActive = 0x20
    Tab = 0x21
    TabHovered = 0x22
    TabActive = 0x23
    TabUnfocused = 0x24
    TabUnfocusedActive = 0x25
    DockingPreview = 0x26
    DockingEmptyBg = 0x27
    PlotLines = 0x28
    PlotLinesHovered = 0x29
    PlotHistogram = 0x2a
    PlotHistogramHovered = 0x2b
    TableHeaderBg = 0x2c
    TableBorderStrong = 0x2d
    TableBorderLight = 0x2e
    TableRowBg = 0x2f
    TableRowBgAlt = 0x30
    TextSelectedBg = 0x31
    DragDropTarget = 0x32
    NavHighlight = 0x33
    NavWindowingHighlight = 0x34
    NavWindowingDimBg = 0x35
    ModalWindowDimBg = 0x36
    COUNT = 0x37

class ImGuiStyleVar_(IntEnum):
    Alpha = 0x0
    DisabledAlpha = 0x1
    WindowPadding = 0x2
    WindowRounding = 0x3
    WindowBorderSize = 0x4
    WindowMinSize = 0x5
    WindowTitleAlign = 0x6
    ChildRounding = 0x7
    ChildBorderSize = 0x8
    PopupRounding = 0x9
    PopupBorderSize = 0xa
    FramePadding = 0xb
    FrameRounding = 0xc
    FrameBorderSize = 0xd
    ItemSpacing = 0xe
    ItemInnerSpacing = 0xf
    IndentSpacing = 0x10
    CellPadding = 0x11
    ScrollbarSize = 0x12
    ScrollbarRounding = 0x13
    GrabMinSize = 0x14
    GrabRounding = 0x15
    TabRounding = 0x16
    ButtonTextAlign = 0x17
    SelectableTextAlign = 0x18
    COUNT = 0x19

class ImGuiButtonFlags_(IntEnum):
    NONE = 0x0
    MouseButtonLeft = 0x1
    MouseButtonRight = 0x2
    MouseButtonMiddle = 0x4
    MouseButtonMask_ = 0x7
    MouseButtonDefault_ = 0x1

class ImGuiColorEditFlags_(IntEnum):
    NONE = 0x0
    NoAlpha = 0x2
    NoPicker = 0x4
    NoOptions = 0x8
    NoSmallPreview = 0x10
    NoInputs = 0x20
    NoTooltip = 0x40
    NoLabel = 0x80
    NoSidePreview = 0x100
    NoDragDrop = 0x200
    NoBorder = 0x400
    AlphaBar = 0x10000
    AlphaPreview = 0x20000
    AlphaPreviewHalf = 0x40000
    HDR = 0x80000
    DisplayRGB = 0x100000
    DisplayHSV = 0x200000
    DisplayHex = 0x400000
    Uint8 = 0x800000
    Float = 0x1000000
    PickerHueBar = 0x2000000
    PickerHueWheel = 0x4000000
    InputRGB = 0x8000000
    InputHSV = 0x10000000
    DefaultOptions_ = 0xa900000
    DisplayMask_ = 0x700000
    DataTypeMask_ = 0x1800000
    PickerMask_ = 0x6000000
    InputMask_ = 0x18000000
    RGB = 0x100000
    HSV = 0x200000
    HEX = 0x400000

class ImGuiSliderFlags_(IntEnum):
    NONE = 0x0
    AlwaysClamp = 0x10
    Logarithmic = 0x20
    NoRoundToFormat = 0x40
    NoInput = 0x80
    InvalidMask_ = 0x7000000f
    ClampOnInput = 0x10

class ImGuiMouseButton_(IntEnum):
    Left = 0x0
    Right = 0x1
    Middle = 0x2
    COUNT = 0x5

class ImGuiMouseCursor_(IntEnum):
    NONE = -0x1
    Arrow = 0x0
    TextInput = 0x1
    ResizeAll = 0x2
    ResizeNS = 0x3
    ResizeEW = 0x4
    ResizeNESW = 0x5
    ResizeNWSE = 0x6
    Hand = 0x7
    NotAllowed = 0x8
    COUNT = 0x9

class ImGuiCond_(IntEnum):
    NONE = 0x0
    Always = 0x1
    Once = 0x2
    FirstUseEver = 0x4
    Appearing = 0x8

class ImDrawFlags_(IntEnum):
    NONE = 0x0
    Closed = 0x1
    RoundCornersTopLeft = 0x10
    RoundCornersTopRight = 0x20
    RoundCornersBottomLeft = 0x40
    RoundCornersBottomRight = 0x80
    RoundCornersNone = 0x100
    RoundCornersTop = 0x30
    RoundCornersBottom = 0xc0
    RoundCornersLeft = 0x50
    RoundCornersRight = 0xa0
    RoundCornersAll = 0xf0
    RoundCornersDefault_ = 0xf0
    RoundCornersMask_ = 0x1f0

class ImDrawListFlags_(IntEnum):
    NONE = 0x0
    AntiAliasedLines = 0x1
    AntiAliasedLinesUseTex = 0x2
    AntiAliasedFill = 0x4
    AllowVtxOffset = 0x8

class ImFontAtlasFlags_(IntEnum):
    NONE = 0x0
    NoPowerOfTwoHeight = 0x1
    NoMouseCursors = 0x2
    NoBakedLines = 0x4

class ImGuiViewportFlags_(IntEnum):
    NONE = 0x0
    IsPlatformWindow = 0x1
    IsPlatformMonitor = 0x2
    OwnedByApp = 0x4
    NoDecoration = 0x8
    NoTaskBarIcon = 0x10
    NoFocusOnAppearing = 0x20
    NoFocusOnClick = 0x40
    NoInputs = 0x80
    NoRendererClear = 0x100
    TopMost = 0x200
    Minimized = 0x400
    NoAutoMerge = 0x800
    CanHostOtherWindows = 0x1000

class ImDrawCornerFlags_(IntEnum):
    NONE = 0x100
    TopLeft = 0x10
    TopRight = 0x20
    BotLeft = 0x40
    BotRight = 0x80
    All = 0xf0
    Top = 0x30
    Bot = 0xc0
    Left = 0x50
    Right = 0xa0

