from matplotlib.lines import Line2D

class Zplane_Object():
    def __init__(self):
        self.original_object = None
        self.conjugate_object = None

    def set_original_object(self, original:Line2D):
        self.original_object = original

    def get_original_object(self) -> Line2D:
        return self.original_object

    def set_conjugate_object(self, conjugate:Line2D):
        self.conjugate_object = conjugate
        
    def get_conjugate_object(self) -> Line2D:
        return self.conjugate_object
    
    def remove(self):
        self.original_object.remove()
        if self.conjugate_object:
            self.conjugate_object.remove()