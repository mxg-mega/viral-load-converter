# models/hbvl_model.py
from models.base_model import BaseModel
from config import Config

class HBVLModel(BaseModel):
    def __init__(self, result):
        super().__init__(result, self.conversion_constant)
        
    @property
    def conversion_constant(self):
        return Config.get_constant("HBVL_CONSTANT")
    
    @conversion_constant.setter
    def conversion_constant(self, value):
        # Validation
        if not isinstance(value, (float, int)):
            raise TypeError("Constant must be a number")
        if value <= 0:
            raise ValueError("Constant must be greater than 0")
        Config.set_constant("HBVL_CONSTANT", float(value))