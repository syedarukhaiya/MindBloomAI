from datetime import datetime
from pydantic import BaseModel,Field
class ChatRequest(BaseModel): message:str=Field(min_length=1,max_length=8000); conversation_id:int|None=None; listener_mode:bool=False; language:str="English"
class ChatResponse(BaseModel): conversation_id:int; message:str; risk_level:str; safety_escalation:bool=False; context_used:list[str]=[]; evidence:list[str]=[]; suggested_action:dict|None=None; provider:str
class ReflectionRequest(BaseModel): diary_entry_id:int
class SafetyRequest(BaseModel): message:str=Field(min_length=1,max_length=8000)
class ActivityComplete(BaseModel): activity_id:int
class PreferenceUpdate(BaseModel): language:str|None=None; tone:str|None=None; memory_enabled:bool|None=None; reminders_enabled:bool|None=None; quiet_hours:str|None=None
class ContactCreate(BaseModel): name:str; relation:str; phone:str|None=None; email:str|None=None; consent_to_share:bool=False
