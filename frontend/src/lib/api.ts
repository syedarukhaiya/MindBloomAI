import type {
  AuthResponse,
  User,
  Mood,
  DiaryEntry,
  Story,
  Circle,
  FutureLetter,
  GratitudeCapsule,
  SmallWin,
} from "../types/api";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api/v1";

class APIClient {
  private token: string | null = null;

  setToken(token: string | null) {
    this.token = token;
  }

  private getHeaders(): Record<string, string> {
    const headers: Record<string, string> = {
      "Content-Type": "application/json",
    };
    if (this.token) {
      headers["Authorization"] = `Bearer ${this.token}`;
    }
    return headers;
  }

  private async request<T>(
    method: string,
    path: string,
    body?: unknown
  ): Promise<T> {
    const response = await fetch(`${API_BASE_URL}${path}`, {
      method,
      headers: this.getHeaders(),
      body: body ? JSON.stringify(body) : undefined,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.detail || "API request failed");
    }

    if (response.status === 204) {
      return null as T;
    }

    return response.json();
  }

  // Auth
  async register(email: string, username: string, password: string): Promise<AuthResponse> {
    return this.request("POST", "/auth/register", { email, username, password });
  }

  async login(email: string, password: string): Promise<AuthResponse> {
    return this.request("POST", "/auth/login", { email, password });
  }

  async getMe(): Promise<User> {
    return this.request("GET", "/auth/me");
  }

  // Moods
  async getMoods(): Promise<Mood[]> {
    return this.request("GET", "/moods");
  }

  async createMood(mood: string, stress?: number, energy?: number, context?: string): Promise<Mood> {
    return this.request("POST", "/moods", { mood, stress, energy, context });
  }

  // Diary
  async getDiaryEntries(): Promise<DiaryEntry[]> {
    return this.request("GET", "/diary");
  }

  async createDiaryEntry(title: string, content: string): Promise<DiaryEntry> {
    return this.request("POST", "/diary", { title, content });
  }

  async getDiaryEntry(id: number): Promise<DiaryEntry> {
    return this.request("GET", `/diary/${id}`);
  }

  // Circles
  async getCircles(skip?: number, limit?: number): Promise<Circle[]> {
    const params = new URLSearchParams();
    if (skip !== undefined) params.append("skip", skip.toString());
    if (limit !== undefined) params.append("limit", limit.toString());
    return this.request("GET", `/circles?${params}`);
  }

  async getMyCircles(): Promise<Circle[]> {
    return this.request("GET", "/circles/my-circles");
  }

  async getCircle(id: number): Promise<Circle> {
    return this.request("GET", `/circles/${id}`);
  }

  async createCircle(name: string, description: string, topic: string, max_participants?: number): Promise<Circle> {
    return this.request("POST", "/circles", { name, description, topic, max_participants });
  }

  async joinCircle(id: number): Promise<{ message: string }> {
    return this.request("POST", `/circles/${id}/join`);
  }

  async leaveCircle(id: number): Promise<{ message: string }> {
    return this.request("POST", `/circles/${id}/leave`);
  }

  // Stories
  async getStories(skip?: number, limit?: number, category?: string): Promise<Story[]> {
    const params = new URLSearchParams();
    if (skip !== undefined) params.append("skip", skip.toString());
    if (limit !== undefined) params.append("limit", limit.toString());
    if (category) params.append("category", category);
    return this.request("GET", `/stories?${params}`);
  }

  async getFeaturedStories(): Promise<Story[]> {
    return this.request("GET", "/stories/featured");
  }

  async getStory(id: number): Promise<Story> {
    return this.request("GET", `/stories/${id}`);
  }

  async createStory(content: string, category: string, is_anonymous?: boolean): Promise<Story> {
    return this.request("POST", "/stories", { content, category, is_anonymous });
  }

  async addStoryReaction(storyId: number, reaction_type: string): Promise<{ message: string }> {
    return this.request("POST", `/stories/${storyId}/reactions`, { reaction_type });
  }

  async reportStory(storyId: number, reason: string): Promise<{ message: string }> {
    return this.request("POST", `/stories/${storyId}/report`, { reason });
  }

  // Future Letters
  async getFutureLetters(): Promise<FutureLetter[]> {
    return this.request("GET", "/future-letters");
  }

  async createFutureLetter(
    content: string,
    scheduled_for: string,
    recipient?: string
  ): Promise<FutureLetter> {
    return this.request("POST", "/future-letters", { content, scheduled_for, recipient });
  }

  // Gratitude Capsules
  async getGratitudeCapsules(): Promise<GratitudeCapsule[]> {
    return this.request("GET", "/gratitude-capsules");
  }

  async createGratitudeCapsule(
    title: string,
    content: string,
    media_url?: string
  ): Promise<GratitudeCapsule> {
    return this.request("POST", "/gratitude-capsules", { title, content, media_url });
  }

  // Small Wins
  async getSmallWins(): Promise<SmallWin[]> {
    return this.request("GET", "/small-wins");
  }

  async createSmallWin(
    content: string,
    is_anonymous?: boolean,
    visibility?: string
  ): Promise<SmallWin> {
    return this.request("POST", "/small-wins", { content, is_anonymous, visibility });
  }

  // Garden
  async getGarden() {
    return this.request("GET", "/garden");
  }

  // Wellbeing
  async getWellbeingInsights() {
    return this.request("GET", "/wellbeing/insights");
  }

  async getPreferences() {
    return this.request("GET", "/preferences");
  }

  async chatWithBloom(message: string, conversation_id?: number, listener_mode?: boolean, language?: string) {
    return this.request("POST", "/bloom/chat", {
      message,
      conversation_id,
      listener_mode,
      language,
    });
  }

  async getRecommendedActivities() {
    return this.request("GET", "/recommendations");
  }

  async completeActivity(activityId: number) {
    return this.request("POST", `/activities/${activityId}/complete`);
  }
}

export const apiClient = new APIClient();
