from typing import Union, Optional
from pydantic import BaseModel

class Node(BaseModel):
    type: str  
    value: Optional[Union[int, str]] = None
    left: Optional['Node'] = None  
    right: Optional['Node'] = None  

    class Config:
        orm_mode = True
        validate_assignment = True
        arbitrary_types_allowed = True

    def to_dict(self):
        return {
            "type": self.type,
            "value": self.value,
            "left": self.left.to_dict() if self.left else None,
            "right": self.right.to_dict() if self.right else None
        }
