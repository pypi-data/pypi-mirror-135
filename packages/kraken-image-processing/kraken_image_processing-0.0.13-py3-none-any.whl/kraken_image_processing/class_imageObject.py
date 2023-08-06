
import uuid

class ImageObject:
    def __init__(self):

        a=2

    
    def load(self, record):

        if isinstance(record, list) and len(record) == 1:
            record = record[0]

        if not record:
            return

        if not isinstance(record, dict):
            return None
            
        for k in record.keys():
            value = record.get(k, None)
            self.set(k, value)
        
        #self._normalize_type()
        #self._normalize_id()

        return True

    def dump(self):
        record = {}
        keys = [i for i in self.__dict__.keys() if i[:1] != '_']

        for k in keys:
            value = self.get(k)
            if type(value) is type(self):
                value = value.record
            record[k] = value
        return record

    def get(self, key):

        # Normalize key
        norm_key = key
        #norm_key = self._normalize_key(key)

        value = getattr(self, norm_key, None)
        #value = self._record.get(norm_key, None)

        return value


    def set(self, key, value):

        

        # Normalize key
        norm_key = key
        #norm_key = self._normalize_key(key)
        norm_value = value
        #norm_value = self._normalize_value(norm_key, value)
        setattr(self, norm_key, norm_value)

        return
