export default function DataSourcePage() {
  const sources = [
    { id: 1, name: 'Police Database', type: 'API', status: 'Active' },
    { id: 2, name: 'News Aggregator', type: 'RSS Feed', status: 'Active' },
    { id: 3, name: 'Community Reports', type: 'User Input', status: 'Active' },
    // Add more sources as needed
  ];

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-800 mb-6">Data & Source Management</h1>
      <div className="bg-white p-6 rounded-lg shadow-md">
        <table className="w-full table-auto">
          <thead>
            <tr className="bg-gray-200">
              <th className="px-4 py-2 text-left">Source Name</th>
              <th className="px-4 py-2 text-left">Type</th>
              <th className="px-4 py-2 text-left">Status</th>
              <th className="px-4 py-2 text-left">Actions</th>
            </tr>
          </thead>
          <tbody>
            {sources.map((source) => (
              <tr key={source.id} className="border-b">
                <td className="px-4 py-2">{source.name}</td>
                <td className="px-4 py-2">{source.type}</td>
                <td className="px-4 py-2">
                  <span className={`px-2 py-1 rounded ${source.status === 'Active' ? 'bg-green-200 text-green-800' : 'bg-red-200 text-red-800'}`}>
                    {source.status}
                  </span>
                </td>
                <td className="px-4 py-2">
                  <button className="bg-blue-500 text-white px-3 py-1 rounded mr-2">Edit</button>
                  <button className="bg-red-500 text-white px-3 py-1 rounded">Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}