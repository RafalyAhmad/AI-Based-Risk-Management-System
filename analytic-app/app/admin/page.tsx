export default function AdminDashboard() {
  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-800 mb-6">Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {/* Cards for overview */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold text-gray-700">Total Areas</h2>
          <p className="text-3xl font-bold text-blue-600">25</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold text-gray-700">Active Alerts</h2>
          <p className="text-3xl font-bold text-red-600">12</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold text-gray-700">News Articles</h2>
          <p className="text-3xl font-bold text-green-600">156</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold text-gray-700">Community Reports</h2>
          <p className="text-3xl font-bold text-purple-600">89</p>
        </div>
      </div>
      {/* Add more dashboard content here */}
      <div className="mt-8 bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-2xl font-semibold text-gray-800 mb-4">Recent Activity</h2>
        <ul className="space-y-2">
          <li className="text-gray-600">New crime report in Area A</li>
          <li className="text-gray-600">News article updated for Area B</li>
          <li className="text-gray-600">User John Doe logged in</li>
        </ul>
      </div>
    </div>
  );
}