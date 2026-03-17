export default function NewsMonitorPage() {
  const news = [
    { id: 1, title: 'Crime Increase in Area A', source: 'Local News', date: '2023-10-01', area: 'Area A' },
    { id: 2, title: 'Theft Reported in Area B', source: 'Online Media', date: '2023-10-02', area: 'Area B' },
    { id: 3, title: 'Police Action in Area C', source: 'Government Report', date: '2023-10-03', area: 'Area C' },
    // Add more news as needed
  ];

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-800 mb-6">News Monitor</h1>
      <div className="bg-white p-6 rounded-lg shadow-md">
        <ul className="space-y-4">
          {news.map((item) => (
            <li key={item.id} className="border-b pb-4">
              <h2 className="text-xl font-semibold text-gray-800">{item.title}</h2>
              <p className="text-gray-600">Source: {item.source} | Date: {item.date} | Area: {item.area}</p>
              <button className="mt-2 bg-blue-500 text-white px-3 py-1 rounded">View Details</button>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}