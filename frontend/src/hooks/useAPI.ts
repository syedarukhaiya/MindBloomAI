import { useState, useCallback, useEffect } from "react";
import { apiClient } from "../lib/api";
import type { Mood, DiaryEntry, Circle, Story, User } from "../types/api";

export function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadUser = useCallback(async () => {
    try {
      const token = localStorage.getItem("mindbloom_token");
      if (!token) {
        setUser(null);
        setLoading(false);
        return;
      }
      apiClient.setToken(token);
      const userData = await apiClient.getMe();
      setUser(userData);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load user");
      setUser(null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadUser();
  }, [loadUser]);

  const login = useCallback(
    async (email: string, password: string) => {
      setLoading(true);
      try {
        const response = await apiClient.login(email, password);
        localStorage.setItem("mindbloom_token", response.access_token);
        apiClient.setToken(response.access_token);
        await loadUser();
        return true;
      } catch (err) {
        setError(err instanceof Error ? err.message : "Login failed");
        return false;
      } finally {
        setLoading(false);
      }
    },
    [loadUser]
  );

  const register = useCallback(
    async (email: string, username: string, password: string) => {
      setLoading(true);
      try {
        const response = await apiClient.register(email, username, password);
        localStorage.setItem("mindbloom_token", response.access_token);
        apiClient.setToken(response.access_token);
        await loadUser();
        return true;
      } catch (err) {
        setError(err instanceof Error ? err.message : "Registration failed");
        return false;
      } finally {
        setLoading(false);
      }
    },
    [loadUser]
  );

  const logout = useCallback(() => {
    localStorage.removeItem("mindbloom_token");
    apiClient.setToken(null);
    setUser(null);
  }, []);

  return { user, loading, error, login, register, logout, loadUser };
}

export function useMoods() {
  const [moods, setMoods] = useState<Mood[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadMoods = useCallback(async () => {
    setLoading(true);
    try {
      const data = await apiClient.getMoods();
      setMoods(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load moods");
    } finally {
      setLoading(false);
    }
  }, []);

  const addMood = useCallback(
    async (mood: string, stress?: number, energy?: number, context?: string) => {
      try {
        const newMood = await apiClient.createMood(mood, stress, energy, context);
        setMoods((prev) => [newMood, ...prev]);
        return newMood;
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to create mood");
        throw err;
      }
    },
    []
  );

  useEffect(() => {
    loadMoods();
  }, [loadMoods]);

  return { moods, loading, error, addMood, loadMoods };
}

export function useDiary() {
  const [entries, setEntries] = useState<DiaryEntry[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadEntries = useCallback(async () => {
    setLoading(true);
    try {
      const data = await apiClient.getDiaryEntries();
      setEntries(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load diary");
    } finally {
      setLoading(false);
    }
  }, []);

  const addEntry = useCallback(async (title: string, content: string) => {
    try {
      const newEntry = await apiClient.createDiaryEntry(title, content);
      setEntries((prev) => [newEntry, ...prev]);
      return newEntry;
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create entry");
      throw err;
    }
  }, []);

  useEffect(() => {
    loadEntries();
  }, [loadEntries]);

  return { entries, loading, error, addEntry, loadEntries };
}

export function useCircles() {
  const [circles, setCircles] = useState<Circle[]>([]);
  const [myCircles, setMyCircles] = useState<Circle[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadCircles = useCallback(async () => {
    setLoading(true);
    try {
      const [allCircles, userCircles] = await Promise.all([
        apiClient.getCircles(),
        apiClient.getMyCircles(),
      ]);
      setCircles(allCircles);
      setMyCircles(userCircles);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load circles");
    } finally {
      setLoading(false);
    }
  }, []);

  const joinCircle = useCallback(async (id: number) => {
    try {
      await apiClient.joinCircle(id);
      await loadCircles();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to join circle");
      throw err;
    }
  }, [loadCircles]);

  const leaveCircle = useCallback(async (id: number) => {
    try {
      await apiClient.leaveCircle(id);
      await loadCircles();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to leave circle");
      throw err;
    }
  }, [loadCircles]);

  useEffect(() => {
    loadCircles();
  }, [loadCircles]);

  return { circles, myCircles, loading, error, joinCircle, leaveCircle, loadCircles };
}

export function useStories() {
  const [stories, setStories] = useState<Story[]>([]);
  const [featuredStories, setFeaturedStories] = useState<Story[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadStories = useCallback(async (category?: string) => {
    setLoading(true);
    try {
      const [allStories, featured] = await Promise.all([
        apiClient.getStories(0, 50, category),
        apiClient.getFeaturedStories(),
      ]);
      setStories(allStories);
      setFeaturedStories(featured);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load stories");
    } finally {
      setLoading(false);
    }
  }, []);

  const addStory = useCallback(
    async (content: string, category: string, is_anonymous?: boolean) => {
      try {
        const newStory = await apiClient.createStory(content, category, is_anonymous);
        setStories((prev) => [newStory, ...prev]);
        return newStory;
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to create story");
        throw err;
      }
    },
    []
  );

  useEffect(() => {
    loadStories();
  }, [loadStories]);

  return { stories, featuredStories, loading, error, addStory, loadStories };
}
