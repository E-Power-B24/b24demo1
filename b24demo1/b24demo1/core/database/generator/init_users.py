from b24demo1.core.database.generator import *
from b24demo1.core.logics.logic_user import UserLogic
from b24demo1.core.models import User

user = User()
user.name = 'admin'
user.full_name = 'Administrator'
user.email = 'admin@gmail.com'
user.password = 'admin'
UserLogic().add(user)