from datetime import datetime
from sqlalchemy import Boolean,DateTime,ForeignKey,Integer,String,Text,func
from sqlalchemy.orm import Mapped,mapped_column
from app.db.database import Base
class Reminder(Base):
 __tablename__="reminders"
 id:Mapped[int]=mapped_column(Integer,primary_key=True,index=True)
 user_id:Mapped[int]=mapped_column(ForeignKey("users.id"),index=True,nullable=False)
 title:Mapped[str]=mapped_column(String(150),nullable=False)
 message:Mapped[str|None]=mapped_column(Text)
 reminder_time:Mapped[datetime]=mapped_column(DateTime,nullable=False)
 is_active:Mapped[bool]=mapped_column(Boolean,default=True,nullable=False)
 created_at:Mapped[datetime]=mapped_column(DateTime,server_default=func.now(),nullable=False)
