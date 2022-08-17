from datetime import datetime
from pydantic import BaseModel,EmailStr
from typing import Optional,Union
class BaseResponse(BaseModel):
    status:str="success"
    msg:Optional[Union[str,dict]]
    data:Optional[Union[list,dict]]

class BaseSchema(BaseModel):
    def get(self):
        return BaseResponse(data=self.dict()).dict()

class UserRegisterResponse(BaseSchema):
    id:int
    username:str
    email:Optional[EmailStr]

class CheckinResponse(BaseSchema):
    user_id:str
    username:str
    check_in:datetime
    check_out:Optional[datetime]