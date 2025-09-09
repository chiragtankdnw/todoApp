import React from 'react';
import { render, screen } from '@testing-library/react';
import Modal from './Modal';

const defaultProps = {
  activeItem: {
    title: 'Test Todo',
    description: 'Test Description',
    completed: false
  },
  toggle: jest.fn(),
  onSave: jest.fn()
};

test('renders Modal component with title', () => {
  render(<Modal {...defaultProps} />);
  const modalElement = screen.getByText(/todo item/i);
  expect(modalElement).toBeInTheDocument();
});

test('renders input fields correctly', () => {
  render(<Modal {...defaultProps} />);
  const titleInput = screen.getByPlaceholderText(/enter todo title/i);
  const descInput = screen.getByPlaceholderText(/enter todo description/i);
  expect(titleInput).toBeInTheDocument();
  expect(descInput).toBeInTheDocument();
  expect(titleInput.value).toBe('Test Todo');
  expect(descInput.value).toBe('Test Description');
});