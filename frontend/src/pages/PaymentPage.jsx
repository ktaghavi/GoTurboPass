import React from "react";
import { useLocation } from "react-router-dom";

export default function PaymentPage() {
  const location = useLocation();
  const { userId, citationId, profileId } = location.state || {};

  return (
    <div className="min-h-screen bg-slate-100 flex items-center justify-center">
      <div className="bg-white shadow-md rounded-lg p-6 md:p-8 w-full max-w-lg">
        <h1 className="text-2xl font-semibold mb-4 text-center">
          Secure Checkout
        </h1>

        <p className="text-sm text-slate-600 mb-4 text-center">
          You&apos;re almost done! Complete your payment to begin your online
          traffic school course.
        </p>

        <div className="text-sm text-slate-700 mb-6 space-y-1">
          {userId && <p>User ID: {userId}</p>}
          {profileId && <p>Profile ID: {profileId}</p>}
          {citationId && <p>Citation ID: {citationId}</p>}
        </div>

        <button
          className="w-full bg-green-600 hover:bg-green-700 text-white font-medium py-2 rounded transition"
          onClick={() => alert("Payment integration goes here")}
        >
          Pay Now ($5.00)
        </button>
      </div>
    </div>
  );
}
