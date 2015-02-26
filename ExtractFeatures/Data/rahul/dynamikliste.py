"""
dynamik liste -> translates to 'dynamic list' in German
It's almost Oktober! :)
"""

class dynamikliste(list):
    def __setitem__(self, index, value):
        if index >= len(self):
            self.extend([None]*(index + 1 - len(self)))
        list.__setitem__(self, index, value)