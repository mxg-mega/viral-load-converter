from .base_model import BaseModel
from config import Config


class HCVLModel(BaseModel):
    def __init__(self, result):
        super().__init__(result, self.conversion_constant)
        
    @property
    def conversion_constant(self):
        return Config.get_constant("HCVL_CONSTANT")
    
    @conversion_constant.setter
    def conversion_constant(self, value):
        if not isinstance(value, float):
            raise TypeError("Constant has to be a float")
        if value == 0:
            raise ValueError("Constant cannot be zero")
        Config.set_constant("HCVL_CONSTANT", float(value))
        