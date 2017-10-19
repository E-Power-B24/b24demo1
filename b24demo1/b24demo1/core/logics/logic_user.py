from b24demo1.core.logics.logic_base import LogicBase
from b24demo1.core.models import User
from passlib.apps import custom_app_context as pwd_context

def hash_password(password):
    return pwd_context.encrypt(password)
def verify_password(password1, password2):
    return pwd_context.verify(password1,password2)


class UserLogic(LogicBase):
    def __init__(self):
        self.__classname__=User

    def authenticate(self, name, password):
        user = self.actives().filter(User.name==name.lower()).first()
        if user:
            verify = verify_password(name.lower()+str(password), user.password)
            if not verify:
                return None

        return user
    def add(self, obj):
        obj.name = obj.name.lower()
        obj.password = hash_password(obj.name + obj.password)
        LogicBase().add(obj)

    # def change_password(self, obj):
    #     obj.password = hash_password(obj.name + obj.password)
    #     return True
