from b24demo1.core.database.generator import *

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)