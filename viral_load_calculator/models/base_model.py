from math import log10


class BaseModel():
    def __init__(self, result, constant):
        if not isinstance(result, (float, int)):
            raise TypeError("Result has to be an Integer or float")
        self.result = result
        
        if not isinstance(constant, float):
            raise TypeError("Constant has to be a float")
        if constant == 0:
            raise ValueError("Constant cannot be zero")
        self.constant = constant
        
    @property
    def conversion_constant(self):
        # Force subclasses to implement this property
        raise NotImplementedError("Subclasses must implement `conversion_constant`")
        
    def convert_to_IU_per_ml(self):
        conversion = self.result / self.conversion_constant
        return conversion
    
    def get_value_log(self):
        return log10(self.result)