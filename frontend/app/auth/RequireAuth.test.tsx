import React from "react";
import { render, screen } from "@testing-library/react";
import { RequireAuth } from "./RequireAuth";

jest.mock("./use-require-auth", () => ({
  useRequireAuth: jest.fn(),
}));

const mockUseRequireAuth = require("./use-require-auth").useRequireAuth;

describe("RequireAuth", () => {
  it("shows loading spinner when loading", () => {
    mockUseRequireAuth.mockReturnValue({ isLoading: true });
    render(<RequireAuth>secret</RequireAuth>);
    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });

  it("shows sign-in message when not authenticated", () => {
    mockUseRequireAuth.mockReturnValue({ isLoading: false, isAuthenticated: false });
    render(<RequireAuth>secret</RequireAuth>);
    expect(screen.getByText(/must be signed in/i)).toBeInTheDocument();
  });

  it("shows unauthorized message when lacking role", () => {
    mockUseRequireAuth.mockReturnValue({ isLoading: false, isAuthenticated: true, hasRequiredRole: false });
    render(<RequireAuth requiredRole="admin">secret</RequireAuth>);
    expect(screen.getByText(/do not have permission/i)).toBeInTheDocument();
  });

  it("renders children when authenticated and authorized", () => {
    mockUseRequireAuth.mockReturnValue({ isLoading: false, isAuthenticated: true, hasRequiredRole: true });
    render(<RequireAuth>secret</RequireAuth>);
    expect(screen.getByText("secret")).toBeInTheDocument();
  });

  it("shows error message if error is present", () => {
    mockUseRequireAuth.mockReturnValue({ isLoading: false, isAuthenticated: true, hasRequiredRole: true, error: "Some error" });
    render(<RequireAuth>secret</RequireAuth>);
    expect(screen.getByText(/some error/i)).toBeInTheDocument();
  });
}); 