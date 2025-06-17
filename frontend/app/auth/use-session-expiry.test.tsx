import { renderHook, act } from "@testing-library/react";
import { useSessionExpiry } from "./use-session-expiry";

jest.mock("@clerk/nextjs", () => ({
  useSession: jest.fn(),
  useAuth: () => ({ signOut: jest.fn() }),
  useSignIn: () => ({ signIn: jest.fn() }),
}));

const mockUseSession = require("@clerk/nextjs").useSession;

describe("useSessionExpiry", () => {
  beforeEach(() => {
    jest.useFakeTimers();
  });
  afterEach(() => {
    jest.useRealTimers();
  });

  it("detects expired session", () => {
    const now = Date.now();
    mockUseSession.mockReturnValue({ session: { expirationTime: new Date(now - 1000).toISOString() } });
    const { result } = renderHook(() => useSessionExpiry());
    act(() => {
      jest.advanceTimersByTime(2000);
    });
    expect(result.current.isExpired).toBe(true);
  });

  it("detects expiring soon session", () => {
    const now = Date.now();
    mockUseSession.mockReturnValue({ session: { expirationTime: new Date(now + 30 * 1000).toISOString() } });
    const { result } = renderHook(() => useSessionExpiry());
    act(() => {
      jest.advanceTimersByTime(2000);
    });
    expect(result.current.isExpiringSoon).toBe(true);
  });

  it("detects normal session", () => {
    const now = Date.now();
    mockUseSession.mockReturnValue({ session: { expirationTime: new Date(now + 120 * 1000).toISOString() } });
    const { result } = renderHook(() => useSessionExpiry());
    act(() => {
      jest.advanceTimersByTime(2000);
    });
    expect(result.current.isExpiringSoon).toBe(false);
    expect(result.current.isExpired).toBe(false);
  });
}); 