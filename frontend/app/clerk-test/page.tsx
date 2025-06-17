"use client";
import { SignIn, SignUp, UserButton, useUser } from "@clerk/nextjs";

export default function ClerkTestPage() {
  const { isLoaded, isSignedIn, user } = useUser();

  if (!isLoaded) return <div>Loading...</div>;

  return (
    <div className="max-w-md mx-auto py-8">
      <h1 className="text-2xl font-bold mb-4">Clerk Test Page</h1>
      {!isSignedIn ? (
        <>
          <div className="mb-4">
            <SignIn />
          </div>
          <div className="mb-4">
            <SignUp />
          </div>
        </>
      ) : (
        <div className="mb-4">
          <UserButton />
          <p className="mt-4">
            Welcome, <strong>{user?.firstName || user?.fullName || user?.username || "User"}</strong>!
          </p>
          <p className="text-sm text-gray-600">
            Email: {user?.primaryEmailAddress?.emailAddress}
          </p>
          {/* Remove the JSON debug output if not needed */}
        </div>
      )}
    </div>
  );
}