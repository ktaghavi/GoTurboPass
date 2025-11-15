import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { authAPI, geoAPI, studentAPI } from "../utils/api";

export default function EnrollmentPage() {
  const navigate = useNavigate();

  const [counties, setCounties] = useState([]);
  const [courts, setCourts] = useState([]);

  const [form, setForm] = useState({
    // Auth
    email: "",
    password: "",

    // Personal
    firstName: "",
    lastName: "",
    dob: "",
    phone: "",

    // Address
    street: "",
    city: "",
    state: "CA",
    zip: "",

    // DL
    dlNumber: "",
    dlState: "CA",
    dlClass: "C",
    gender: "MALE",

    // Marketing
    howFound: "ONLINE",

    // Court / citation
    countyId: "",
    courtId: "",
    caseNumber: "",
    docketNumber: "",
    certificateDueDate: "",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Load counties on mount
  useEffect(() => {
    geoAPI
      .getCounties()
      .then((data) => setCounties(data))
      .catch((err) => {
        console.error(err);
        setError("Failed to load counties");
      });
  }, []);

  // Load courts when county changes
  useEffect(() => {
    if (!form.countyId) {
      setCourts([]);
      setForm((prev) => ({ ...prev, courtId: "" }));
      return;
    }

    geoAPI
      .getCourtsByCounty(form.countyId)
      .then((data) => setCourts(data))
      .catch((err) => {
        console.error(err);
        setError("Failed to load courts");
      });
  }, [form.countyId]);

  function handleChange(e) {
    const { name, value } = e.target;
    setForm((prev) => ({
      ...prev,
      [name]: value,
    }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      // 1) Register user (email + password)
      const registerRes = await authAPI.register({
        email: form.email,
        password: form.password,
      });

      const userId = registerRes.userId;
      if (!userId) {
        throw new Error("Registration succeeded but no userId returned");
      }

      // store for later flows if needed
      window.localStorage.setItem("userId", String(userId));

      // 2) Enroll (profile + citation)
      const payload = {
        userId,
        firstName: form.firstName,
        lastName: form.lastName,
        dob: form.dob,
        phone: form.phone,
        street: form.street,
        city: form.city,
        state: form.state,
        zip: form.zip,
        dlNumber: form.dlNumber,
        dlState: form.dlState,
        dlClass: form.dlClass,
        gender: form.gender,
        howFound: form.howFound,
        countyId: Number(form.countyId),
        courtId: Number(form.courtId),
        caseNumber: form.caseNumber,
        docketNumber: form.docketNumber || undefined,
        certificateDueDate: form.certificateDueDate,
      };

      const enrollRes = await studentAPI.enroll(payload);

      // 3) Go straight to payment "paywall" screen
      navigate("/payment", {
        state: {
          userId,
          citationId: enrollRes.citationId,
          profileId: enrollRes.profileId,
        },
      });
    } catch (err) {
      console.error(err);
      setError(err.message || "Registration / enrollment failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-slate-100 flex items-center justify-center">
      <div className="bg-white shadow-md rounded-lg p-6 md:p-8 w-full max-w-2xl">
        <h1 className="text-2xl font-semibold mb-2 text-center">
          California Traffic School Registration
        </h1>
        <p className="text-sm text-slate-600 mb-6 text-center">
          Create your account and enter your court / citation details to get started.
        </p>

        {error && (
          <p className="mb-4 text-sm text-red-600 text-center">{error}</p>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">

          {/* Auth section */}
          <section>
            <h2 className="text-lg font-medium mb-3">Account Info</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-1">Email</label>
                <input
                  type="email"
                  name="email"
                  value={form.email}
                  onChange={handleChange}
                  required
                  className="w-full border rounded px-3 py-2 text-sm focus:outline-none focus:ring focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Password</label>
                <input
                  type="password"
                  name="password"
                  value={form.password}
                  onChange={handleChange}
                  required
                  className="w-full border rounded px-3 py-2 text-sm focus:outline-none focus:ring focus:ring-blue-500"
                />
              </div>
            </div>
          </section>

          {/* Personal Info */}
          <section>
            <h2 className="text-lg font-medium mb-3">Personal Info</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-1">First Name</label>
                <input
                  name="firstName"
                  value={form.firstName}
                  onChange={handleChange}
                  required
                  className="w-full border rounded px-3 py-2 text-sm focus:outline-none focus:ring focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Last Name</label>
                <input
                  name="lastName"
                  value={form.lastName}
                  onChange={handleChange}
                  required
                  className="w-full border rounded px-3 py-2 text-sm focus:outline-none focus:ring focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Date of Birth</label>
                <input
                  type="date"
                  name="dob"
                  value={form.dob}
                  onChange={handleChange}
                  required
                  className="w-full border rounded px-3 py-2 text-sm focus:outline-none focus:ring focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Phone</label>
                <input
                  name="phone"
                  value={form.phone}
                  onChange={handleChange}
                  required
                  className="w-full border rounded px-3 py-2 text-sm focus:outline-none focus:ring focus:ring-blue-500"
                />
              </div>
            </div>
          </section>

          {/* Address */}
          <section>
            <h2 className="text-lg font-medium mb-3">Address</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="md:col-span-2">
                <label className="block text-sm font-medium mb-1">Street</label>
                <input
                  name="street"
                  value={form.street}
                  onChange={handleChange}
                  required
                  className="w-full border rounded px-3 py-2 text-sm focus:outline-none focus:ring focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">City</label>
                <input
                  name="city"
                  value={form.city}
                  onChange={handleChange}
                  required
                  className="w-full border rounded px-3 py-2 text-sm focus:outline-none focus:ring focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">State</label>
                <input
                  name="state"
                  value={form.state}
                  onChange={handleChange}
                  maxLength={2}
                  required
                  className="w-full border rounded px-3 py-2 text-sm focus:outline-none focus:ring focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">ZIP</label>
                <input
                  name="zip"
                  value={form.zip}
                  onChange={handleChange}
                  required
                  className="w-full border rounded px-3 py-2 text-sm focus:outline-none focus:ring focus:ring-blue-500"
                />
              </div>
            </div>
          </section>

          {/* DL */}
          <section>
            <h2 className="text-lg font-medium mb-3">Driver License</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="md:col-span-2">
                <label className="block text-sm font-medium mb-1">DL Number</label>
                <input
                  name="dlNumber"
                  value={form.dlNumber}
                  onChange={handleChange}
                  required
                  className="w-full border rounded px-3 py-2 text-sm focus:outline-none focus:ring focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">DL State</label>
                <input
                  name="dlState"
                  value={form.dlState}
                  onChange={handleChange}
                  maxLength={2}
                  required
                  className="w-full border rounded px-3 py-2 text-sm focus:outline-none focus:ring focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">DL Class</label>
                <select
                  name="dlClass"
                  value={form.dlClass}
                  onChange={handleChange}
                  required
                  className="w-full border rounded px-3 py-2 text-sm focus:outline-none focus:ring focus:ring-blue-500"
                >
                  <option value="A">A</option>
                  <option value="B">B</option>
                  <option value="C">C</option>
                  <option value="M">M</option>
                  <option value="OTHER">Other</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Gender</label>
                <select
                  name="gender"
                  value={form.gender}
                  onChange={handleChange}
                  className="w-full border rounded px-3 py-2 text-sm focus:outline-none focus:ring focus:ring-blue-500"
                >
                  <option value="MALE">Male</option>
                  <option value="FEMALE">Female</option>
                  <option value="NONBINARY">Non-binary</option>
                </select>
              </div>
            </div>
          </section>

          {/* Court & citation */}
          <section>
            <h2 className="text-lg font-medium mb-3">Court & Citation</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-1">County</label>
                <select
                  name="countyId"
                  value={form.countyId}
                  onChange={handleChange}
                  required
                  className="w-full border rounded px-3 py-2 text-sm focus:outline-none focus:ring focus:ring-blue-500"
                >
                  <option value="">Select county</option>
                  {counties.map((c) => (
                    <option key={c.id} value={c.id}>
                      {c.name}
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Court</label>
                <select
                  name="courtId"
                  value={form.courtId}
                  onChange={handleChange}
                  required
                  disabled={!form.countyId}
                  className="w-full border rounded px-3 py-2 text-sm focus:outline-none focus:ring focus:ring-blue-500 disabled:bg-slate-100"
                >
                  <option value="">Select court</option>
                  {courts.map((court) => (
                    <option key={court.id} value={court.id}>
                      {court.name}
                      {court.dmv_code && ` (${court.dmv_code})`}
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Case Number</label>
                <input
                  name="caseNumber"
                  value={form.caseNumber}
                  onChange={handleChange}
                  required
                  className="w-full border rounded px-3 py-2 text-sm focus:outline-none focus:ring focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">
                  Docket Number (optional)
                </label>
                <input
                  name="docketNumber"
                  value={form.docketNumber}
                  onChange={handleChange}
                  className="w-full border rounded px-3 py-2 text-sm focus:outline-none focus:ring focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">
                  Certificate Due Date
                </label>
                <input
                  type="date"
                  name="certificateDueDate"
                  value={form.certificateDueDate}
                  onChange={handleChange}
                  required
                  className="w-full border rounded px-3 py-2 text-sm focus:outline-none focus:ring focus:ring-blue-500"
                />
              </div>
            </div>
          </section>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 rounded transition disabled:opacity-60"
          >
            {loading ? "Submitting…" : "Continue to Payment"}
          </button>
        </form>
      </div>
    </div>
  );
}
