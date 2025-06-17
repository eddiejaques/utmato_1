import React, { ReactNode } from "react";
import { useRequireAuth } from "./use-require-auth";

interface RequireAuthProps {
  children: ReactNode;
  requiredRole?: string;
}

export function RequireAuth({ children, requiredRole }: RequireAuthProps) {
  const { isLoading, isAuthenticated, hasRequiredRole, error } = useRequireAuth({ requiredRole });

  if (isLoading) {
    return <div className="flex items-center justify-center h-32">Loading...</div>;
  }
  if (!isAuthenticated) {
    return <div className="text-red-500">You must be signed in to view this page.</div>;
  }
  if (!hasRequiredRole) {
    return <div className="text-red-500">You do not have permission to view this page.</div>;
  }
  if (error) {
    return <div className="text-red-500">{error}</div>;
  }
  return <>{children}</>;
} 