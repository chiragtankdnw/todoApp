import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import App from '../App';

// Mock localStorage
const localStorageMock = {
  getItem: jest.fn(() => null),
  setItem: jest.fn(),
  clear: jest.fn(),
};
Object.defineProperty(window, 'localStorage', { value: localStorageMock });

// Mock matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: jest.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: jest.fn(),
    removeListener: jest.fn(),
    addEventListener: jest.fn(),
    removeEventListener: jest.fn(),
    dispatchEvent: jest.fn(),
  })),
});

describe('Dark Mode Toggle', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    document.body.className = '';
  });

  test('renders dark mode toggle button', () => {
    render(<App />);
    const toggleButton = screen.getByRole('button', { name: /toggle dark mode/i });
    expect(toggleButton).toBeInTheDocument();
    expect(toggleButton).toHaveTextContent('Dark Mode');
  });

  test('toggles between light and dark mode when clicked', () => {
    render(<App />);
    const toggleButton = screen.getByRole('button', { name: /toggle dark mode/i });
    
    // Initially should be in light mode
    expect(toggleButton).toHaveTextContent('Dark Mode');
    
    // Click to switch to dark mode
    fireEvent.click(toggleButton);
    expect(toggleButton).toHaveTextContent('Light Mode');
    
    // Click to switch back to light mode
    fireEvent.click(toggleButton);
    expect(toggleButton).toHaveTextContent('Dark Mode');
  });
});