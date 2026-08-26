from datetime import datetime
from pydantic import BaseModel,ConfigDict,Field
class ReminderCreate(BaseModel): title:str=Field(min_length=1,max_length=150); message:str|None=None; reminder_time:datetime
class ReminderResponse(BaseModel): model_config=ConfigDict(from_attributes=True); id:int; user_id:int; title:str; message:str|None; reminder_time:datetime; is_active:bool; created_at:datetime
