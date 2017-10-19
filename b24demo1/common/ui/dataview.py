from sqlalchemy import func
# fastest query result counting than q.count
def row_count(q):
    count_q = q.statement.with_only_columns([func.count()]).order_by(None)
    count = q.session.execute(count_q).scalar()
    return count

class DataView(object):
    def __init__(self,query,limit=0,offset=0,asdict=False):
        self.query =  query
        self.limit = int(limit)
        self.offset = int(offset)
        self.asdict = asdict

        # show all record if any offset or limit equal -1
        if self.offset==-1 or self.limit==-1:
            self.offset=0
            self.limit=0

        #if self.query is list:
        if isinstance(self.query, list):
            self.offset = 0
            #self.limit = 0 #len(limit)

    @property
    def count(self):
        if isinstance(self.query, list):
            return 0;
        if not hasattr(self,'_count'):
            self._count = row_count(self.query)
        return self._count

    @property
    def result(self):
        #if self.query is list:
        #if isinstance(self.query, list):
        #    return self.query;
        if not hasattr(self,'_result'):
            if self.limit:
                self._result = self.query.limit(self.limit).offset(self.offset).all()
            else:
                self._result = self.query.all()
            if self.asdict:
                self._result = [x._asdict() for x in self._result]
        return self._result

    @property
    def result_count(self):
        return len(self.result)


    @property
    def remain(self):
        return self.count-self.offset-self.result_count
