from datetime import datetime
from pydantic import BaseModel,EmailStr
from typing import List, Optional,Union
class Base(BaseModel):
    status:str="success"
    msg:Optional[Union[str,dict]]
    data:Optional[Union[list,dict]]
    def get(self):
        return self.data.self.dict()

class BaseResponse(BaseModel):
    def get(self,*args, **kwargs):
        return Base(*args, **kwargs,data=self.dict()).dict()

class UserRegisterResponse(BaseResponse):
    id:int
    username:str
    email:Optional[EmailStr]

class CheckinResponse(BaseResponse):
    user_id:str
    username:str
    check_in:datetime
    check_out:Optional[datetime]
class History(BaseResponse):
    check_in:datetime
    check_out:Optional[datetime]
class HistoryResponse(BaseResponse):
    user_id:str
    history:list[History]
class ActivitySchema(BaseResponse):
    id:int
    name:str
    description:Optional[str]
class ActivityResponse(BaseResponse):
    user_id:str
    activity:list[ActivitySchema]
class CreateActivityResponse(BaseResponse):
    id:int
    user_id:str
    name:str
    description:Optional[str]
class UpdateActivityResponse(CreateActivityResponse):
    pass
class DeleteActivityResponse(CreateActivityResponse):
    pass