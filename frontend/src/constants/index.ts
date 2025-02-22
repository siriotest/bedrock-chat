import { GenerationParams } from '../@types/bot';

export const EDGE_GENERATION_PARAMS = {
  maxTokens: {
    MAX: 4096,
    MIN: 1,
    STEP: 1,
  },
  temperature: {
    MAX: 1,
    MIN: 0,
    STEP: 0.05,
  },
  topP: {
    MAX: 1,
    MIN: 0,
    STEP: 0.001,
  },
  topK: {
    MAX: 500,
    MIN: 0,
    STEP: 1,
  },
};

export const EDGE_MISTRAL_GENERATION_PARAMS = {
  maxTokens: {
    MAX: 8192,
    MIN: 1,
    STEP: 1,
  },
  temperature: {
    MAX: 1,
    MIN: 0,
    STEP: 0.05,
  },
  topP: {
    MAX: 1,
    MIN: 0,
    STEP: 0.001,
  },
  topK: {
    MAX: 200,
    MIN: 0,
    STEP: 1,
  },
};

export const DEFAULT_GENERATION_CONFIG: GenerationParams = {
  maxTokens: 2000,
  topK: 128,
  topP: 0.999,
  temperature: 0.6,
  stopSequences: ['Human: ', 'Assistant: '],
};

export const DEFAULT_MISTRAL_GENERATION_CONFIG: GenerationParams = {
  maxTokens: 4096,
  topK: 50,
  topP: 0.9,
  temperature: 0.5,
  stopSequences: ['[INST]', '[/INST]'],
};

export const SyncStatus = {
  QUEUED: 'QUEUED',
  FAILED: 'FAILED',
  RUNNING: 'RUNNING',
  SUCCEEDED: 'SUCCEEDED',
} as const;

export const TooltipDirection = {
  LEFT: 'left',
  RIGHT: 'right',
} as const;

export type Direction =
  (typeof TooltipDirection)[keyof typeof TooltipDirection];

export const PostStreamingStatus = {
  START: 'START',
  BODY: 'BODY',
  STREAMING: 'STREAMING',
  STREAMING_END: 'STREAMING_END',
  AGENT_THINKING: 'AGENT_THINKING',
  AGENT_TOOL_RESULT: 'AGENT_TOOL_RESULT',
  AGENT_RELATED_DOCUMENT: 'AGENT_RELATED_DOCUMENT',
  ERROR: 'ERROR',
  END: 'END',
} as const;

export const GUARDRAILS_FILTERS_THRESHOLD = {
  MAX: 3,
  MIN: 0,
  STEP: 1,
};

export const GUARDRAILS_CONTECTUAL_GROUNDING_THRESHOLD = {
  MAX: 0.99,
  MIN: 0,
  STEP: 0.01,
};

export const AVAILABLE_MODEL_KEYS = [
  'claude-v3-opus',
  'claude-v3-sonnet',
  'claude-v3.5-sonnet',
  'claude-v3.5-sonnet-v2',
  'claude-v3-haiku',
  'claude-v3.5-haiku',
  'mistral-7b-instruct',
  'mixtral-8x7b-instruct',
  'mistral-large',
  'amazon-nova-pro',
  'amazon-nova-lite',
  'amazon-nova-micro',
] as const;
