from TypeDef import TypeDef


class WeChatEventHanlder(object):
    @staticmethod
    def onSub():
        return "Thanks for subscribing our channel. We aim to eat everywhere and travel to everywhere you want " \
               "without any language specifications."

    @staticmethod
    def onFoody():
        return "No Food to eat..."

    @staticmethod
    def onTravel():
        return "I don't know where you want to go"

    @staticmethod
    def onMaEat():
        return "吃吃吃"

    @staticmethod
    def onMaSleep():
        return "睡睡睡"



class EventRouter(object):
    __sys_event = { TypeDef.Event_SUB: WeChatEventHanlder.onSub,
    }

    __self_func = {TypeDef.Event_Foody: WeChatEventHanlder.onFoody,
                 TypeDef.Event_Tavel: WeChatEventHanlder.onTravel,
                 TypeDef.Event_Ma_Eat: WeChatEventHanlder.onMaEat,
                 TypeDef.Event_Ma_Sleep: WeChatEventHanlder.onMaSleep,
    }

    @staticmethod
    def get_envent_func(event, key_value):
        func = ""
        if event in TypeDef.SystemEvent:
            func = EventRouter.__sys_event.get(event, TypeDef.Undefined)
        elif event in TypeDef.CustEvent:
            func = EventRouter.__self_func.get(key_value, EventRouter.undefined_event)
        return func

    @staticmethod
    def undefined_event():
        return TypeDef.Undefined
