/**
 * UMAJA API Integration Layer
 * Connects White Room Lab to UMAJA Core backend
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://umaja-core-production.up.railway.app';
const GITHUB_API_BASE = 'https://api.github.com';

// Cache configuration
const CACHE_TTL = 60 * 1000; // 60 seconds
const cache = new Map<string, { data: any; timestamp: number }>();

/**
 * Generic fetch with caching and error handling
 */
async function cachedFetch<T>(url: string, options?: RequestInit): Promise<T> {
  const cacheKey = `${url}${JSON.stringify(options || {})}`;
  const cached = cache.get(cacheKey);
  
  if (cached && Date.now() - cached.timestamp < CACHE_TTL) {
    return cached.data as T;
  }

  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();
    cache.set(cacheKey, { data, timestamp: Date.now() });
    return data as T;
  } catch (error) {
    console.error(`API fetch error for ${url}:`, error);
    throw error;
  }
}

/**
 * GitHub API: Fetch Pull Requests
 */
export interface GitHubPR {
  id: number;
  number: number;
  title: string;
  state: 'open' | 'closed';
  merged_at: string | null;
  created_at: string;
  updated_at: string;
  user: {
    login: string;
    avatar_url: string;
  };
  comments: number;
  html_url: string;
}

export async function fetchGitHubPRs(owner: string = 'harrie19', repo: string = 'UMAJA-Core'): Promise<GitHubPR[]> {
  const url = `${GITHUB_API_BASE}/repos/${owner}/${repo}/pulls?state=all&per_page=100`;
  return cachedFetch<GitHubPR[]>(url);
}

/**
 * UMAJA Backend: Health Check
 */
export interface HealthStatus {
  status: string;
  timestamp: string;
  version?: string;
}

export async function fetchHealth(): Promise<HealthStatus> {
  try {
    const data = await cachedFetch<HealthStatus>(`${API_BASE_URL}/health`);
    return data;
  } catch (error) {
    return {
      status: 'offline',
      timestamp: new Date().toISOString(),
    };
  }
}

/**
 * UMAJA Backend: Daily Smile
 */
export interface DailySmile {
  smile: string;
  date: string;
  personality?: string;
  language?: string;
}

export async function fetchDailySmile(): Promise<DailySmile> {
  try {
    const data = await cachedFetch<DailySmile>(`${API_BASE_URL}/api/daily-smile`);
    return data;
  } catch (error) {
    return {
      smile: '😊 Connection to UMAJA Backend offline - using fallback',
      date: new Date().toISOString().split('T')[0],
      personality: 'System',
    };
  }
}

/**
 * UMAJA Backend: World Tour Status
 */
export interface WorldTourStatus {
  current_city?: string;
  cities_visited?: number;
  last_update?: string;
}

export async function fetchWorldTourStatus(): Promise<WorldTourStatus> {
  try {
    const data = await cachedFetch<WorldTourStatus>(`${API_BASE_URL}/worldtour/status`);
    return data;
  } catch (error) {
    return {
      current_city: 'Unknown',
      cities_visited: 0,
      last_update: new Date().toISOString(),
    };
  }
}

/**
 * Mock Energy Monitor Data (WebSocket simulation)
 */
export interface EnergyData {
  current_power: number;
  max_power: number;
  energy_type: 'renewable' | 'fossil' | 'mixed';
  timestamp: string;
  efficiency: number;
}

export function createMockEnergyStream(callback: (data: EnergyData) => void): () => void {
  const interval = setInterval(() => {
    const data: EnergyData = {
      current_power: 50 + Math.random() * 50, // 50-100W
      max_power: 100,
      energy_type: Math.random() > 0.3 ? 'renewable' : 'mixed',
      timestamp: new Date().toISOString(),
      efficiency: 0.7 + Math.random() * 0.25, // 70-95%
    };
    callback(data);
  }, 2000); // Update every 2 seconds

  return () => clearInterval(interval);
}

/**
 * Mock Vector Agent Data
 */
export interface VectorAgent {
  id: string;
  position: [number, number, number];
  velocity: [number, number, number];
  status: 'idle' | 'working' | 'communicating';
  color: string;
}

export function generateMockAgents(count: number = 10): VectorAgent[] {
  const statusOptions: VectorAgent['status'][] = ['idle', 'working', 'communicating'];
  const colorMap = {
    idle: '#888888',
    working: '#FFAA00',
    communicating: '#4FC3F7',
  };

  return Array.from({ length: count }, (_, i) => {
    const status = statusOptions[Math.floor(Math.random() * statusOptions.length)];
    return {
      id: `agent-${i}`,
      position: [
        (Math.random() - 0.5) * 10,
        (Math.random() - 0.5) * 10,
        (Math.random() - 0.5) * 10,
      ],
      velocity: [
        (Math.random() - 0.5) * 0.1,
        (Math.random() - 0.5) * 0.1,
        (Math.random() - 0.5) * 0.1,
      ],
      status,
      color: colorMap[status],
    };
  });
}

/**
 * World Tour Cities
 */
export interface City {
  name: string;
  country: string;
  lat: number;
  lng: number;
  visited: boolean;
  visit_date?: string;
}

export const WORLD_TOUR_CITIES: City[] = [
  { name: 'Berlin', country: 'Germany', lat: 52.52, lng: 13.405, visited: true, visit_date: '2025-12-01' },
  { name: 'Tokyo', country: 'Japan', lat: 35.6762, lng: 139.6503, visited: true, visit_date: '2025-12-15' },
  { name: 'New York', country: 'USA', lat: 40.7128, lng: -74.0060, visited: false },
  { name: 'London', country: 'UK', lat: 51.5074, lng: -0.1278, visited: false },
  { name: 'Sydney', country: 'Australia', lat: -33.8688, lng: 151.2093, visited: false },
  { name: 'São Paulo', country: 'Brazil', lat: -23.5505, lng: -46.6333, visited: false },
  { name: 'Mumbai', country: 'India', lat: 19.0760, lng: 72.8777, visited: false },
  { name: 'Cairo', country: 'Egypt', lat: 30.0444, lng: 31.2357, visited: false },
];

/**
 * Clear cache (useful for development)
 */
export function clearCache(): void {
  cache.clear();
}
