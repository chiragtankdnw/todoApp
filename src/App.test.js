import { render, screen } from '@testing-library/react';
import App from './App';

test('renders todo app title', () => {
  render(<App />);
  const titleElement = screen.getByText(/copilot's Todo App/i);
  expect(titleElement).toBeInTheDocument();
});

test('renders dark mode toggle button', () => {
  render(<App />);
  const toggleButton = screen.getByRole('button', { name: /toggle dark mode/i });
  expect(toggleButton).toBeInTheDocument();
});

test('renders add task button', () => {
  render(<App />);
  const addButton = screen.getByRole('button', { name: /add task/i });
  expect(addButton).toBeInTheDocument();
});
