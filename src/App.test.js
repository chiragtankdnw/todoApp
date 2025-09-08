import { render, screen } from '@testing-library/react';
import App from './App';

test('renders todo app with add task button', () => {
  render(<App />);
  const addTaskButton = screen.getByText(/add task/i);
  expect(addTaskButton).toBeInTheDocument();
});

test('renders complete and incomplete tabs', () => {
  render(<App />);
  const completeTab = screen.getByText('Complete');
  const incompleteTab = screen.getByText('Incomplete');
  expect(completeTab).toBeInTheDocument();
  expect(incompleteTab).toBeInTheDocument();
});
