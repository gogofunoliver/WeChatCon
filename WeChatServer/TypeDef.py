class TypeDef(object):
    Undefined = "Undefined"

    OP_Read = "查询"
    OP_Write = "记录"
    OP_Check = "查询"
    OP_Remove = "删除"
    OP_Joke = "段子"
    OP_CheckArticle = "文章"
    OP_WeatherSub = "天气订阅"
    OP_WeatherChk = "天气查询"
    OP_WeatherUnSub = "取消订阅"
    OP_HistoryArticle = "历史文章"
    OP_Create_VM = "创建虚拟机"
    OP_Delete_VM = "删除所有虚拟机"

    Event_Location = "LOCATION"
    Event_SUB = "subscribe"
    Event_UnSub = "unsubscribe"
    Event_Foody = "Foody"
    Event_Tavel = "Tourist"
    Event_Ma_Eat = "MA_CHI"
    Event_Ma_Sleep = "MA_SLEEP"
    Event_Ma_Joke = "MA_JOKE"
    Event_History = "History"
    Event_HistoryAlert = "HistoryAlert"
    Event_ApplyVM = "ApplyVM"
    Event_RemoveVM = "RemoveVM"
    Event_About_Me = "About_Me"
    Event_SetZH = "SetZH"
    Event_SetEN = "SetEN"
    Event_SetCT = "SetCT"

    LANG = Event_SetZH

    SystemEvent = [ Event_SUB,
                    Event_UnSub,
                    Event_Location,
    ]

    CustEvent = [ "CLICK", "VIEW"]

    sex_dict = { 1: "Male",
                 2: "Female",
                 0: "Unknown",
                }

    digital =  { "一": 1, "二" : 2, "三":3, "四" : 4, "五" : 5, "六" : 6, "七" : 7, "八" : 8, "九":9 }

    UserMap = {
        "Oliver" : "oHBF6wUHaE4L2yUfhKMBqcrjoi0g",
        "Jesse" : "bbbbbbbb"
    }