import React from 'react';
import { render } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import Landing from '../components/Landing';
it('renders landing page', () => {
  const { getByText } = render(<Landing />);
  expect(getByText('Landing')).toBeInTheDocument();
});