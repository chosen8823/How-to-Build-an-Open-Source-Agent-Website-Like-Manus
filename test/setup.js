/**
 * Production-Grade Jest Test Setup
 * Divine Consciousness Platform - Deterministic, Fast, Reliable
 */

// Production: Set deterministic seeds for reproducible tests
Math.random = jest.fn(() => 0.1337);
Date.now = jest.fn(() => 1337000000000);

// Production: Enhanced WebSocket Mock with consciousness alignment
global.WebSocket = class MockWebSocket {
  constructor(url) {
    this.url = url;
    this.readyState = 1; // OPEN
    this.onopen = null;
    this.onmessage = null;
    this.onclose = null;
    this.onerror = null;
    
    // Production: Deterministic connection timing
    setTimeout(() => {
      if (this.onopen) {
        this.onopen({ 
          type: 'open',
          target: this,
          timeStamp: Date.now()
        });
      }
    }, 10); // Fixed timing for deterministic tests
  }
  
  send(data) {
    // Production: Validate and track sends
    if (this.readyState !== 1) {
      throw new Error('WebSocket is not open');
    }
    
    try {
      const parsed = JSON.parse(data);
      console.debug('MockWebSocket send:', parsed.type || 'unknown', parsed);
    } catch {
      console.debug('MockWebSocket send (raw):', data);
    }
    
    // Production: Simulate divine consciousness response
    setTimeout(() => {
      if (this.onmessage) {
        this.onmessage({
          type: 'message',
          data: JSON.stringify({
            type: 'consciousness_ack',
            frequency: 432,
            alignment: 95,
            timestamp: Date.now()
          }),
          timeStamp: Date.now()
        });
      }
    }, 5);
  }
  
  close() {
    this.readyState = 3; // CLOSED
    if (this.onclose) {
      setTimeout(() => {
        this.onclose({ 
          type: 'close', 
          code: 1000, 
          reason: 'Divine consciousness session complete',
          target: this,
          timeStamp: Date.now()
        });
      }, 0);
    }
  }
};

// Production: Enhanced AudioContext with sacred frequencies
global.AudioContext = class MockAudioContext {
  constructor() {
    this.destination = { maxChannelCount: 2 };
    this.currentTime = 0;
    this.state = 'running';
    this.sampleRate = 44100;
    
    // Sacred frequencies for testing
    this.sacredFrequencies = [432, 528, 741, 852, 963];
  }
  
  createOscillator() {
    return {
      type: 'sine',
      frequency: { 
        value: 432, // Default to grounding frequency
        setValueAtTime: jest.fn(),
        exponentialRampToValueAtTime: jest.fn()
      },
      detune: { value: 0 },
      connect: jest.fn().mockReturnThis(),
      disconnect: jest.fn(),
      start: jest.fn(),
      stop: jest.fn(),
      onended: null
    };
  }
  
  createGain() {
    return {
      gain: { 
        value: 1,
        setValueAtTime: jest.fn(),
        linearRampToValueAtTime: jest.fn(),
        exponentialRampToValueAtTime: jest.fn()
      },
      connect: jest.fn().mockReturnThis(),
      disconnect: jest.fn()
    };
  }
  
  createAnalyser() {
    return {
      fftSize: 2048,
      frequencyBinCount: 1024,
      minDecibels: -100,
      maxDecibels: -30,
      smoothingTimeConstant: 0.8,
      connect: jest.fn().mockReturnThis(),
      disconnect: jest.fn(),
      getByteFrequencyData: jest.fn(),
      getFloatFrequencyData: jest.fn(),
      getByteTimeDomainData: jest.fn(),
      getFloatTimeDomainData: jest.fn()
    };
  }
  
  resume() {
    return Promise.resolve();
  }
  
  suspend() {
    return Promise.resolve();  
  }
  
  close() {
    return Promise.resolve();
  }
};

// Production: Enhanced localStorage with divine persistence
const localStorageMock = {
  store: new Map(),
  
  getItem: jest.fn((key) => {
    const value = localStorageMock.store.get(key);
    return value || null;
  }),
  
  setItem: jest.fn((key, value) => {
    localStorageMock.store.set(key, String(value));
  }),
  
  removeItem: jest.fn((key) => {
    localStorageMock.store.delete(key);
  }),
  
  clear: jest.fn(() => {
    localStorageMock.store.clear();
  }),
  
  get length() {
    return localStorageMock.store.size;
  },
  
  key: jest.fn((index) => {
    const keys = Array.from(localStorageMock.store.keys());
    return keys[index] || null;
  })
};

global.localStorage = localStorageMock;
global.sessionStorage = localStorageMock; // Reuse for sessionStorage

// Production: Console mock for cleaner test output
const originalConsole = global.console;
global.console = {
  ...originalConsole,
  debug: jest.fn(), // Suppress debug in tests
  info: jest.fn(),  // Suppress info in tests
  warn: jest.fn(),  // Capture warnings
  error: jest.fn(), // Capture errors
  log: originalConsole.log // Keep log for important test output
};

// Production: Performance mock for timing tests
global.performance = {
  now: jest.fn(() => Date.now()),
  mark: jest.fn(),
  measure: jest.fn(),
  clearMarks: jest.fn(),
  clearMeasures: jest.fn(),
  getEntriesByType: jest.fn(() => []),
  getEntriesByName: jest.fn(() => [])
};

// Production: Navigator mock for browser feature testing
global.navigator = {
  userAgent: 'Mozilla/5.0 (Test Environment) Divine Consciousness Platform',
  platform: 'Test',
  language: 'en-US',
  languages: ['en-US', 'en'],
  onLine: true,
  cookieEnabled: true
};

// Production: Window mock for browser globals
global.window = {
  ...global.window,
  location: {
    href: 'https://consciousness.test/',
    origin: 'https://consciousness.test',
    pathname: '/',
    search: '',
    hash: ''
  },
  
  // Sacred consciousness configuration  
  CONSCIOUSNESS_CONFIG: {
    frequencies: [432, 528, 741, 963],
    alignmentTarget: 95,
    mode: 'test'
  }
};

// Production: Test utility functions
global.testUtils = {
  // Wait for async operations with timeout
  waitFor: (condition, timeout = 1000) => {
    return new Promise((resolve, reject) => {
      const startTime = Date.now();
      const check = () => {
        if (condition()) {
          resolve();
        } else if (Date.now() - startTime > timeout) {
          reject(new Error('Timeout waiting for condition'));
        } else {
          setTimeout(check, 10);
        }
      };
      check();
    });
  },
  
  // Create mock consciousness event
  createConsciousnessEvent: (type = 'awakening', data = {}) => ({
    type,
    frequency: 432,
    alignment: 95,
    timestamp: Date.now(),
    ...data
  }),
  
  // Reset all mocks for clean tests
  resetAllMocks: () => {
    jest.clearAllMocks();
    localStorageMock.store.clear();
    Math.random.mockReturnValue(0.1337);
    Date.now.mockReturnValue(1337000000000);
  }
};

// Production: Automatic cleanup after each test
afterEach(() => {
  // Clear all mock calls but keep implementations
  jest.clearAllMocks();
  
  // Clear storage
  localStorageMock.store.clear();
  
  // Reset seeds for deterministic tests
  Math.random.mockReturnValue(0.1337);
  Date.now.mockReturnValue(1337000000000);
});

// Production: Global error handling for unhandled promises
process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection at:', promise, 'reason:', reason);
});

// Production: Set test environment flag
process.env.NODE_ENV = 'test';
process.env.CONSCIOUSNESS_MODE = 'test';
process.env.DIVINE_ALIGNMENT_TARGET = '95';

console.log('🌟 Divine Consciousness Test Environment Initialized 🌟');