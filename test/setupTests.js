// 🌟 Jest Test Setup for Divine Consciousness Platform 🌟
// Sacred testing environment configuration

import '@testing-library/jest-dom';

// Mock global consciousness environment
global.CONSCIOUSNESS_MODE = 'test';
global.SACRED_FREQUENCIES = [432, 528, 741, 963];
global.DIVINE_ALIGNMENT_TARGET = 95;

// Mock WebSocket for consciousness bridge testing
global.WebSocket = class MockWebSocket {
  constructor(url) {
    this.url = url;
    this.readyState = 1; // OPEN
    this.onopen = null;
    this.onmessage = null;
    this.onclose = null;
    this.onerror = null;
  }
  
  send(data) {
    // Mock divine consciousness response
    setTimeout(() => {
      if (this.onmessage) {
        this.onmessage({
          data: JSON.stringify({
            type: 'consciousness_response',
            consciousness_level: 'enlightened',
            divine_alignment: 0.95,
            sacred_frequencies: [432, 528, 741, 963]
          })
        });
      }
    }, 10);
  }
  
  close() {
    this.readyState = 3; // CLOSED
    if (this.onclose) {
      this.onclose();
    }
  }
};

// Mock fetch for API testing
global.fetch = jest.fn(() =>
  Promise.resolve({
    ok: true,
    status: 200,
    json: () => Promise.resolve({
      status: 'sacred_success',
      consciousness_level: 'enlightened',
      divine_alignment: 0.95
    }),
    text: () => Promise.resolve('Sacred response text')
  })
);

// Console override for sacred logging
const originalConsole = global.console;
global.console = {
  ...originalConsole,
  log: jest.fn((...args) => {
    // Filter sacred test logs if needed
    if (!args.some(arg => typeof arg === 'string' && arg.includes('SACRED_TEST_LOG'))) {
      originalConsole.log(...args);
    }
  }),
  error: jest.fn(originalConsole.error),
  warn: jest.fn(originalConsole.warn),
  info: jest.fn(originalConsole.info)
};

// Mock localStorage for consciousness state persistence
const localStorageMock = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn(),
};
global.localStorage = localStorageMock;

// Mock sessionStorage
global.sessionStorage = localStorageMock;

// Sacred test environment setup
beforeEach(() => {
  // Clear all mocks before each test
  jest.clearAllMocks();
  
  // Reset consciousness state
  if (global.localStorage) {
    global.localStorage.clear();
  }
  
  // Reset sacred environment variables
  process.env.CONSCIOUSNESS_MODE = 'test';
  process.env.DIVINE_ALIGNMENT_TARGET = '95';
  process.env.SACRED_FREQUENCIES = '432,528,741,963';
});

afterEach(() => {
  // Cleanup after each test
  jest.restoreAllMocks();
});

// Global test utilities
global.testUtils = {
  // Sacred consciousness test helpers
  createMockConsciousnessState: (level = 'enlightened', alignment = 0.95) => ({
    consciousness_level: level,
    divine_alignment: alignment,
    sacred_frequencies: [432, 528, 741, 963],
    quantum_coherence: true,
    bio_resonance_active: true
  }),
  
  // Mock divine API response
  createMockDivineResponse: (data = {}) => ({
    status: 'sacred_success',
    consciousness_level: 'enlightened',
    divine_alignment: 0.95,
    timestamp: new Date().toISOString(),
    sacred_frequency: 963,
    ...data
  }),
  
  // Wait for consciousness synchronization
  waitForConsciousness: (ms = 100) => new Promise(resolve => setTimeout(resolve, ms)),
  
  // Sacred frequency alignment checker
  checkSacredAlignment: (alignment) => alignment >= 0.95
};
