import React from 'react';
import { render, screen } from '@testing-library/react';
import Modal from './Modal';

test('renders Modal component', () => {
    render(<Modal />);
    const modalElement = screen.getByText(/modal content/i);
    expect(modalElement).toBeInTheDocument();
});

test('closes Modal on close button click', () => {
    const { getByText } = render(<Modal />);
    const closeButton = getByText(/close/i);
    closeButton.click();
    const modalElement = screen.queryByText(/modal content/i);
    expect(modalElement).not.toBeInTheDocument();
});