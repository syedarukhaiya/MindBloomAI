from datetime import datetime
from sqlalchemy import DateTime,ForeignKey,Integer,String,Text,Boolean,func
from sqlalchemy.orm import Mapped,mapped_column
from app.db.database import Base
class Conversation(Base):
 __tablename__="conversations"
 id:Mapped[int]=mapped_column(Integer,primary_key=True)
 user_id:Mapped[int]=mapped_column(ForeignKey("users.id"),index=True,nullable=False)
 title:Mapped[str]=mapped_column(String(200),default="Talk with Bloom",nullable=False)
 listener_mode:Mapped[bool]=mapped_column(Boolean,default=False,nullable=False)
 language:Mapped[str]=mapped_column(String(30),default="English",nullable=False)
 created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now(),nullable=False)
class Message(Base):
 __tablename__="messages"
 id:Mapped[int]=mapped_column(Integer,primary_key=True)
 conversation_id:Mapped[int]=mapped_column(ForeignKey("conversations.id"),index=True,nullable=False)
 role:Mapped[str]=mapped_column(String(20),nullable=False)
 content:Mapped[str]=mapped_column(Text,nullable=False)
 risk_level:Mapped[str]=mapped_column(String(20),default="NORMAL",nullable=False)
 created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now(),nullable=False)
class AIMemory(Base):
 __tablename__="ai_memory"
 id:Mapped[int]=mapped_column(Integer,primary_key=True)
 user_id:Mapped[int]=mapped_column(ForeignKey("users.id"),index=True,nullable=False)
 memory:Mapped[str]=mapped_column(Text,nullable=False)
 source:Mapped[str]=mapped_column(String(50),default="user_approved",nullable=False)
 created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now(),nullable=False)
class UserPreference(Base):
 __tablename__="user_preferences"
 id:Mapped[int]=mapped_column(Integer,primary_key=True)
 user_id:Mapped[int]=mapped_column(ForeignKey("users.id"),unique=True,index=True,nullable=False)
 language:Mapped[str]=mapped_column(String(30),default="English",nullable=False)
 tone:Mapped[str]=mapped_column(String(30),default="warm",nullable=False)
 memory_enabled:Mapped[bool]=mapped_column(Boolean,default=True,nullable=False)
 reminders_enabled:Mapped[bool]=mapped_column(Boolean,default=True,nullable=False)
 quiet_hours:Mapped[str|None]=mapped_column(String(30))
class TrustedContact(Base):
 __tablename__="trusted_contacts"
 id:Mapped[int]=mapped_column(Integer,primary_key=True)
 user_id:Mapped[int]=mapped_column(ForeignKey("users.id"),index=True,nullable=False)
 name:Mapped[str]=mapped_column(String(120),nullable=False)
 relation:Mapped[str]=mapped_column(String(60),nullable=False)
 phone:Mapped[str|None]=mapped_column(String(40))
 email:Mapped[str|None]=mapped_column(String(255))
 consent_to_share:Mapped[bool]=mapped_column(Boolean,default=False,nullable=False)
class SafetyEvent(Base):
 __tablename__="safety_events"
 id:Mapped[int]=mapped_column(Integer,primary_key=True)
 user_id:Mapped[int]=mapped_column(ForeignKey("users.id"),index=True,nullable=False)
 risk_level:Mapped[str]=mapped_column(String(20),nullable=False)
 source:Mapped[str]=mapped_column(String(30),default="precheck",nullable=False)
 created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now(),nullable=False)
class Activity(Base):
 __tablename__="wellbeing_activities"
 id:Mapped[int]=mapped_column(Integer,primary_key=True)
 slug:Mapped[str]=mapped_column(String(100),unique=True,nullable=False)
 title:Mapped[str]=mapped_column(String(150),nullable=False)
 description:Mapped[str]=mapped_column(Text,nullable=False)
 category:Mapped[str]=mapped_column(String(60),nullable=False)
 duration_seconds:Mapped[int]=mapped_column(Integer,default=60,nullable=False)
class ActivityCompletion(Base):
 __tablename__="activity_completions"
 id:Mapped[int]=mapped_column(Integer,primary_key=True)
 user_id:Mapped[int]=mapped_column(ForeignKey("users.id"),index=True,nullable=False)
 activity_id:Mapped[int]=mapped_column(ForeignKey("wellbeing_activities.id"),index=True,nullable=False)
 completed_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now(),nullable=False)
class SupportResource(Base):
 __tablename__="support_resources"
 id:Mapped[int]=mapped_column(Integer,primary_key=True)
 name:Mapped[str]=mapped_column(String(200),nullable=False)
 category:Mapped[str]=mapped_column(String(80),nullable=False)
 description:Mapped[str]=mapped_column(Text,nullable=False)
 url:Mapped[str|None]=mapped_column(String(500))
 phone:Mapped[str|None]=mapped_column(String(60))
 language:Mapped[str]=mapped_column(String(50),default="English",nullable=False)
 location:Mapped[str|None]=mapped_column(String(120))
 verified:Mapped[bool]=mapped_column(Boolean,default=True,nullable=False)
 demo_only:Mapped[bool]=mapped_column(Boolean,default=False,nullable=False)
