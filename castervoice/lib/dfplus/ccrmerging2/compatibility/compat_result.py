'''
compatible: a boolean

TODO: --- this needs to be reworked so that it works with merging an ordered group of rules 

'''
class CompatibilityResult(object):
    def __init__(self, compatible, incompatible_specs=None):
        self._compatible = compatible
        self._incompatible_specs = incompatible_specs
    
    def is_compatible(self):
        return self._compatible
    
    def incompatible_specs(self):
        if self._incompatible_specs is None: return []
        return list(self._incompatible_specs)