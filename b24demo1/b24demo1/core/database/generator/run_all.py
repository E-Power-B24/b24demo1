from b24demo1.core import models
# models.current_user = lambda :'migrate'

print 'Load init schema ...'
import b24demo1.core.database.generator.init_schema


print 'Load init user ...'
import b24demo1.core.database.generator.init_users

print 'Load init exchange_rate ...'
import b24demo1.core.database.generator.init_exchange_rate

print 'Run all success ... !'