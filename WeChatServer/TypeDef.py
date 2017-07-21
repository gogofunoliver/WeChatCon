class TypeDef(object):
    Undefined = "Undefined"

    OP_Read = "查询"
    OP_Write = "记录"
    OP_Check = "查询"
    OP_Remove = "删除"
    OP_WeatherSub = "天气订阅"
    OP_WeatherChk = "天气查询"
    OP_WeatherUnSub = "取消订阅"


    SystemEvent = [ "subscribe",
                      "unsubscribe"
                      "LOCATION",
    ]

    CustEvent = [ "CLICK", "VIEW"]

    Event_SUB = "subscribe"
    Event_UnSub = "unsubscribe"
    Event_Foody = "FOODY"
    Event_Tavel = "TRAVEL"
    Event_Ma_Eat = "MA_CHI"
    Event_Ma_Sleep = "MA_SLEEP"

