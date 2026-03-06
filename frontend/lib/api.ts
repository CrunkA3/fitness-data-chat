import axios from "axios";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Types
export interface ChatMessageRequest {
  message: string;
  user_id?: number;
}

export interface ChatMessageResponse {
  response: string;
  chart_data: Record<string, unknown> | null;
}

export interface Activity {
  id: number;
  name: string | null;
  activity_type: string | null;
  start_date: string | null;
  distance_km: number;
  duration_minutes: number;
}

export interface AnalyticsSummary {
  total_activities: number;
  total_distance_km: number;
  total_duration_hours: number;
  avg_heart_rate: number | null;
  activity_types: Record<string, number>;
  recent_activities: Activity[];
}

// Chat API
export async function sendChatMessage(
  message: string,
  userId: number = 1
): Promise<ChatMessageResponse> {
  const response = await apiClient.post<ChatMessageResponse>("/api/chat", {
    message,
    user_id: userId,
  });
  return response.data;
}

export async function getChatHistory(userId: number = 1): Promise<unknown[]> {
  const response = await apiClient.get<unknown[]>("/api/chat/history", {
    params: { user_id: userId },
  });
  return response.data;
}

// Analytics API
export async function getAnalyticsSummary(
  userId: number = 1
): Promise<AnalyticsSummary> {
  const response = await apiClient.get<AnalyticsSummary>(
    "/api/analytics/summary",
    {
      params: { user_id: userId },
    }
  );
  return response.data;
}

// Strava API
export async function getStravaAuthUrl(): Promise<{ auth_url: string }> {
  const response = await apiClient.get<{ auth_url: string }>(
    "/api/strava/auth"
  );
  return response.data;
}

export async function syncStravaActivities(
  userId: number = 1
): Promise<{ status: string; synced_count: number }> {
  const response = await apiClient.post<{
    status: string;
    synced_count: number;
  }>("/api/strava/sync", { user_id: userId });
  return response.data;
}

// Garmin API
export async function connectGarmin(
  email: string,
  password: string,
  userId: number = 1
): Promise<{ status: string; message: string }> {
  const response = await apiClient.post<{ status: string; message: string }>(
    "/api/garmin/auth",
    {
      email,
      password,
      user_id: userId,
    }
  );
  return response.data;
}

export async function syncGarminActivities(
  userId: number = 1
): Promise<{ status: string; synced_count: number }> {
  const response = await apiClient.post<{
    status: string;
    synced_count: number;
  }>("/api/garmin/sync", { user_id: userId });
  return response.data;
}

// SSE Streaming
export function streamChatMessage(
  message: string,
  onChunk: (chunk: string) => void,
  onDone: () => void,
  onError: (error: string) => void,
  userId: number = 1
): () => void {
  const controller = new AbortController();

  fetch(`${API_URL}/api/chat/stream`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, user_id: userId }),
    signal: controller.signal,
  })
    .then((response) => {
      const reader = response.body?.getReader();
      if (!reader) return;

      const decoder = new TextDecoder();

      const read = (): void => {
        reader
          .read()
          .then(({ done, value }) => {
            if (done) {
              onDone();
              return;
            }

            const text = decoder.decode(value);
            const lines = text.split("\n");

            for (const line of lines) {
              if (line.startsWith("data: ")) {
                const data = line.slice(6);
                if (data === "[DONE]") {
                  onDone();
                  return;
                }
                try {
                  const parsed = JSON.parse(data) as {
                    chunk?: string;
                    error?: string;
                  };
                  if (parsed.error) {
                    onError(parsed.error);
                  } else if (parsed.chunk) {
                    onChunk(parsed.chunk);
                  }
                } catch {
                  // SSE lines that aren't valid JSON (e.g. empty keep-alive lines) are
                  // safely ignored — they carry no payload data.
                }
              }
            }

            read();
          })
          .catch((err: unknown) => {
            if (err instanceof Error && err.name !== "AbortError") {
              onError(err.message);
            }
          });
      };

      read();
    })
    .catch((err: unknown) => {
      if (err instanceof Error && err.name !== "AbortError") {
        onError(err.message);
      }
    });

  return () => controller.abort();
}
