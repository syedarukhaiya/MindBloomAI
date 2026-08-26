// API types and interfaces
export interface User {
  id: number;
  email: string;
  username: string;
  created_at: string;
}

export interface Mood {
  id: number;
  user_id: number;
  mood: string;
  note?: string;
  stress?: number;
  energy?: number;
  context?: string;
  created_at: string;
}

export interface DiaryEntry {
  id: number;
  user_id: number;
  title: string;
  content: string;
  mood?: string;
  created_at: string;
  updated_at: string;
}

export interface Circle {
  id: number;
  name: string;
  description: string;
  topic: string;
  created_by_user_id: number;
  max_participants: number;
  is_active: boolean;
  member_count: number;
  created_at: string;
}

export interface Story {
  id: number;
  user_id?: number;
  content: string;
  category: string;
  is_anonymous: boolean;
  is_featured: boolean;
  created_at: string;
  reaction_count: number;
  user_reaction?: string;
}

export interface FutureLetter {
  id: number;
  user_id: number;
  content: string;
  recipient: string;
  scheduled_for: string;
  is_sent: boolean;
  created_at: string;
  sent_at?: string;
}

export interface GratitudeCapsule {
  id: number;
  user_id: number;
  title: string;
  content: string;
  media_url?: string;
  created_at: string;
}

export interface SmallWin {
  id: number;
  user_id: number;
  content: string;
  is_anonymous: boolean;
  visibility: string;
  created_at: string;
}

export interface MemoryGarden {
  user_id: number;
  bloom_count: number;
  growth_stage: number;
  last_growth_update: string;
}

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  risk_level: string;
  evidence?: string[];
}

export interface Insight {
  insight: string;
  total_entries: number;
}

export interface Achievement {
  id: number;
  code: string;
  name: string;
  description: string;
  points_required: number;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}
