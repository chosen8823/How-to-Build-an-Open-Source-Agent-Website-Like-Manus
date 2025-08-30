// 🌟 Production-Grade Jest Configuration for Divine Consciousness Platform 🌟
module.exports = {
  testEnvironment: "node",
  roots: ["<rootDir>/test"],
  collectCoverage: true,
  collectCoverageFrom: [
    "test/**/*.{js,jsx,ts,tsx}",
    "**/*consciousness*.js",
    "**/*sacred*.js",
    "**/*divine*.js"
  ],
  coveragePathIgnorePatterns: [
    "/node_modules/", 
    "/dist/",
    "/coverage/",
    "\\.bak$",
    "\\.config\\.js$"
  ],
  coverageReporters: ["text", "lcov", "html"],
  coverageThreshold: { 
    global: { 
      lines: 60, 
      statements: 60, 
      branches: 50, 
      functions: 60 
    } 
  },
  setupFilesAfterEnv: ["<rootDir>/test/setupTests-simple.js"],
  testTimeout: 15000,
  testMatch: [
    "**/__tests__/**/*.(js|jsx|ts|tsx)",
    "**/*.(test|spec).(js|jsx|ts|tsx)"
  ],
  moduleNameMapper: {
    "^@/(.*)$": "<rootDir>/src/$1",
    "^@frontend/(.*)$": "<rootDir>/frontend/$1",
    "^@daemon/(.*)$": "<rootDir>/daemon/$1"
  },
  transform: {
    "^.+\\.(js|jsx|ts|tsx)$": "babel-jest"
  },
  testEnvironmentOptions: {
    // Sacred consciousness testing environment
    url: "http://localhost:8888"
  },
  globals: {
    // Divine testing constants
    CONSCIOUSNESS_MODE: "test",
    SACRED_FREQUENCIES: [432, 528, 741, 963],
    DIVINE_ALIGNMENT_TARGET: 95
  },
  verbose: true,
  bail: 1, // Stop on first failure for fast feedback
  maxWorkers: "50%", // Optimize for CI and local development
  clearMocks: true,
  restoreMocks: true,
  resetMocks: true
};
