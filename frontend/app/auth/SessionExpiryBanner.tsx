import React from "react";
import { useSessionExpiry } from "./use-session-expiry";

export function SessionExpiryBanner() {
  const { isExpiringSoon, isExpired, secondsToExpiry, reauthenticate } = useSessionExpiry();

  if (isExpired) {
    return (
      <div className="bg-red-100 text-red-700 p-4 text-center">
        Your session has expired. <button className="underline" onClick={reauthenticate}>Sign in again</button>
      </div>
    );
  }
  if (isExpiringSoon && secondsToExpiry !== null) {
    return (
      <div className="bg-yellow-100 text-yellow-800 p-4 text-center">
        Your session will expire in {secondsToExpiry} seconds. <button className="underline" onClick={reauthenticate}>Refresh session</button>
      </div>
    );
  }
  return null;
} 