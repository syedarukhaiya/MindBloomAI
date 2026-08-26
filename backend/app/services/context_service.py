from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.mood import MoodEntry
from app.models.diary import DiaryEntry
from app.models.wellbeing import Message,AIMemory,UserPreference
def build_context(db:Session,user_id:int)->dict:
 moods=db.scalars(select(MoodEntry).where(MoodEntry.user_id==user_id).order_by(MoodEntry.created_at.desc()).limit(5)).all()
 diaries=db.scalars(select(DiaryEntry).where(DiaryEntry.user_id==user_id).order_by(DiaryEntry.created_at.desc()).limit(3)).all()
 memories=db.scalars(select(AIMemory).where(AIMemory.user_id==user_id).order_by(AIMemory.created_at.desc()).limit(5)).all()
 pref=db.scalar(select(UserPreference).where(UserPreference.user_id==user_id))
 recent=[m.mood for m in moods]
 themes=[]
 for d in diaries:
  for term in ["exam","placement","career","parent","lonely","sleep","stress","relationship","money"]:
   if term in d.content.lower() and term not in themes: themes.append(term)
 return {"recent_moods":recent,"recent_themes":themes[:5],"memories":[m.memory for m in memories],"language":pref.language if pref else "English","mood_trend":"mixed" if len(set(recent))>1 else (recent[0] if recent else "unknown")}
