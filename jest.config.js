module.exports = {
  testEnvironment: 'node',
  testMatch: ['**/src/**/*.test.js'],
  transform: {
    '^.+\\.jsx?$': 'babel-jest'
  },
  collectCoverage: true,
  coverageDirectory: 'coverage',
  verbose: true
};