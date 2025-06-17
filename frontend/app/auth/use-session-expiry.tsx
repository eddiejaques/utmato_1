import { useEffect, useState } from "react";
import { useSession, useAuth, useSignIn } from "@clerk/nextjs";

interface UseSessionExpiryResult {
  isExpired: boolean;
  isExpiringSoon: boolean;
  secondsToExpiry: number | null;
  reauthenticate: () => void;
}

const EXPIRY_SOON_THRESHOLD = 60; // seconds

export function useSessionExpiry(): UseSessionExpiryResult {
  const { session } = useSession();
  const { signOut } = useAuth();
  const { signIn } = useSignIn();
  const [secondsToExpiry, setSecondsToExpiry] = useState<number | null>(null);
  const [isExpired, setIsExpired] = useState(false);
  const [isExpiringSoon, setIsExpiringSoon] = useState(false);

  useEffect(() => {
    if (!session) return;
    const exp = session.expirationTime ? new Date(session.expirationTime).getTime() : null;
    if (!exp) return;
    const interval = setInterval(() => {
      const now = Date.now();
      const seconds = Math.floor((exp - now) / 1000);
      setSecondsToExpiry(seconds);
      setIsExpired(seconds <= 0);
      setIsExpiringSoon(seconds > 0 && seconds <= EXPIRY_SOON_THRESHOLD);
    }, 1000);
    return () => clearInterval(interval);
  }, [session]);

  const reauthenticate = () => {
    signOut();
    signIn?.();
  };

  return {
    isExpired,
    isExpiringSoon,
    secondsToExpiry,
    reauthenticate,
  };
} 