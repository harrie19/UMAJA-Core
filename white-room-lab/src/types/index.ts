export type FormType = 
  | 'bubble'
  | 'human'
  | 'bugs_bunny'
  | 'turbine'
  | 'dna'
  | 'neural_network'
  | 'molecule'
  | 'city'
  | 'galaxy'
  | 'tool'
  | 'vehicle';

export interface TransformConfig {
  duration: number;        // milliseconds
  easing: string;          // 'easeInOut', 'spring', etc.
  intermediateSteps: number;
}

export interface ParsedCommand {
  intent: 'build' | 'transform' | 'simulate' | 'analyze' | 'query';
  target?: string;
  parameters?: Record<string, any>;
  confidence: number;
}

export interface PermissionRequest {
  id: string;
  action: string;
  details: {
    tool?: string;
    size?: string;
    source?: string;
    risk: 'low' | 'medium' | 'high';
  };
  timestamp: number;
}

export interface Message {
  id: string;
  content: string;
  sender: 'user' | 'ai';
  timestamp: number;
}

export interface SystemMetrics {
  fps: number;
  objectCount: number;
  physicsActive: boolean;
  currentForm: FormType;
  activeSimulations: number;
}
