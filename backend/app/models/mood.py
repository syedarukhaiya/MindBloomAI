from datetime import datetime
from sqlalchemy import DateTime,ForeignKey,Integer,String,Text,func
from sqlalchemy.orm import Mapped,mapped_column
from app.db.database import Base
class MoodEntry(Base):
 __tablename__="mood_entries"
 id:Mapped[int]=mapped_column(Integer,primary_key=True,index=True)
 user_id:Mapped[int]=mapped_column(ForeignKey("users.id"),index=True,nullable=False)
 mood:Mapped[str]=mapped_column(String(50),nullable=False)
 note:Mapped[str|None]=mapped_column(Text)
 stress:Mapped[int|None]=mapped_column(Integer)
 energy:Mapped[int|None]=mapped_column(Integer)
 context:Mapped[str|None]=mapped_column(String(200))
 created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now(),nullable=False)
