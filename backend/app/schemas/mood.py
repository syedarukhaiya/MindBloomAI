from datetime import datetime
from pydantic import BaseModel,ConfigDict,Field
class MoodCreate(BaseModel): mood:str=Field(min_length=1,max_length=50); note:str|None=None; stress:int|None=Field(None,ge=1,le=5); energy:int|None=Field(None,ge=1,le=5); context:str|None=Field(None,max_length=200)
class MoodResponse(BaseModel): model_config=ConfigDict(from_attributes=True); id:int; user_id:int; mood:str; note:str|None; stress:int|None; energy:int|None; context:str|None; created_at:datetime
