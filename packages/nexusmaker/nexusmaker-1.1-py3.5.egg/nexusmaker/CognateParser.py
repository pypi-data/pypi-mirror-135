
class CognateParser(object):
    
    UNIQUE_IDENTIFIER = "u_"
    
    def __init__(self, strict=True, uniques=True):
        """
        Parses cognates. 
        
        - strict (default=True):  remove dubious cognates (?)
        - uniques (default=True): non-cognate items get unique states
        """
        self.uniques = uniques
        self.strict = strict
        
        self.unique_id = 0
        
    def get_next_unique(self):
        if not self.uniques: 
            return []
        self.unique_id = self.unique_id + 1
        return ["%s%d" % (self.UNIQUE_IDENTIFIER, self.unique_id)]
    
    def parse_cognate(self, value):
        raw = value
        if value is None:
            return self.get_next_unique()
        elif value == '':
            return self.get_next_unique()
        elif str(value).lower() == 's': # error
            return self.get_next_unique()
        elif str(value).lower() == 'x': # error
            return self.get_next_unique()
        elif isinstance(value, str):
            if value.startswith(","):
                raise ValueError("Possible broken combined cognate %r" % raw)
            value = value.replace('.', ',').replace("/", ",")
            # parse out subcognates
            value = [v.strip() for v in value.split(",")]
            
            if self.strict:
                # remove dubious cognates
                value = [v for v in value if '?' not in v]
                # exit if all are dubious, setting to unique state
                if len(value) == 0:
                    return self.get_next_unique()
            else:
                value = [v.replace("?", "") for v in value]
            
            # remove any empty things in the list
            value = [v for v in value if len(v) > 0]
            return value
        else:
            raise ValueError("%s" % type(value))