import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth, useUser } from "@clerk/nextjs";

interface UseRequireAuthOptions {
  requiredRole?: string;
}

interface UseRequireAuthResult {
  isLoading: boolean;
  isAuthenticated: boolean;
  hasRequiredRole: boolean;
  error?: string;
}

export function useRequireAuth(options?: UseRequireAuthOptions): UseRequireAuthResult {
  const { isLoaded, isSignedIn } = useAuth();
  const { user, isLoaded: isUserLoaded } = useUser();
  const router = useRouter();

  const requiredRole = options?.requiredRole;
  const hasRequiredRole = requiredRole
    ? user?.publicMetadata?.role === requiredRole
    : true;

  useEffect(() => {
    if (!isLoaded || !isUserLoaded) return;
    if (!isSignedIn) {
      router.replace("/sign-in");
    } else if (requiredRole && !hasRequiredRole) {
      router.replace("/unauthorized");
    }
  }, [isLoaded, isUserLoaded, isSignedIn, hasRequiredRole, requiredRole, router]);

  return {
    isLoading: !isLoaded || !isUserLoaded,
    isAuthenticated: !!isSignedIn,
    hasRequiredRole,
    error: !isSignedIn
      ? "User not authenticated"
      : requiredRole && !hasRequiredRole
      ? "User lacks required role"
      : undefined,
  };
} 