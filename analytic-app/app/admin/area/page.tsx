export default function AreaPage() {
  const areas = [
    { id: 1, name: 'Area A', crimeRate: 'High', population: 50000 },
    { id: 2, name: 'Area B', crimeRate: 'Medium', population: 75000 },
    { id: 3, name: 'Area C', crimeRate: 'Low', population: 30000 },
    // Add more areas as needed
  ];

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-800 mb-6">Area Management</h1>
      <div className="bg-white p-6 rounded-lg shadow-md">
        <table className="w-full table-auto">
          <thead>
            <tr className="bg-gray-200">
              <th className="px-4 py-2 text-left">Area Name</th>
              <th className="px-4 py-2 text-left">Crime Rate</th>
              <th className="px-4 py-2 text-left">Population</th>
              <th className="px-4 py-2 text-left">Actions</th>
            </tr>
          </thead>
          <tbody>
            {areas.map((area) => (
              <tr key={area.id} className="border-b">
                <td className="px-4 py-2">{area.name}</td>
                <td className="px-4 py-2">{area.crimeRate}</td>
                <td className="px-4 py-2">{area.population}</td>
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