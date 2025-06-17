import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import ClerkTestPage from './page';

jest.mock('@clerk/nextjs', () => ({
  SignIn: () => <div>SignIn Component</div>,
  SignUp: () => <div>SignUp Component</div>,
  UserButton: () => <div>UserButton Component</div>,
  useUser: () => ({ isSignedIn: false, user: null }),
}));

describe('ClerkTestPage', () => {
  it('renders Clerk test page with sign in by default', () => {
    render(<ClerkTestPage />);
    expect(screen.getByText('Clerk Test Page')).toBeInTheDocument();
    expect(screen.getByText('SignIn Component')).toBeInTheDocument();
    expect(screen.queryByText('SignUp Component')).not.toBeInTheDocument();
    expect(screen.getByText('UserButton Component')).toBeInTheDocument();
    expect(screen.getByText(/Status:/)).toBeInTheDocument();
    expect(screen.getByText('Signed Out')).toBeInTheDocument();
  });

  it('shows SignUp component when Sign Up button is clicked', () => {
    render(<ClerkTestPage />);
    fireEvent.click(screen.getByText('Sign Up'));
    expect(screen.getByText('SignUp Component')).toBeInTheDocument();
    expect(screen.queryByText('SignIn Component')).not.toBeInTheDocument();
  });
});