export default function CommunityPage() {
  const reports = [
    { id: 1, user: 'John Doe', area: 'Area A', description: 'Suspicious activity near park', date: '2023-10-01' },
    { id: 2, user: 'Jane Smith', area: 'Area B', description: 'Theft at local store', date: '2023-10-02' },
    { id: 3, user: 'Bob Johnson', area: 'Area C', description: 'Vandalism on street', date: '2023-10-03' },
    // Add more reports as needed
  ];

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-800 mb-6">Community Reports</h1>
      <div className="bg-white p-6 rounded-lg shadow-md">
        <ul className="space-y-4">
          {reports.map((report) => (
            <li key={report.id} className="border-b pb-4">
              <h2 className="text-lg font-semibold text-gray-800">Report by {report.user}</h2>
              <p className="text-gray-600">Area: {report.area} | Date: {report.date}</p>
              <p className="text-gray-700 mt-2">{report.description}</p>
              <button className="mt-2 bg-blue-500 text-white px-3 py-1 rounded">Review</button>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}