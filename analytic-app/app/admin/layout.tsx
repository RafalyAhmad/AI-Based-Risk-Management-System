import Link from 'next/link';
import { ReactNode } from 'react';

const menuItems = [
  { name: 'Dashboard', href: '/admin' },
  { name: 'Area', href: '/admin/area' },
  { name: 'News Monitor', href: '/admin/news-monitor' },
  { name: 'Data & Source', href: '/admin/data-source' },
  { name: 'Community', href: '/admin/community' },
  { name: 'User Management', href: '/admin/user-management' },
];

export default function AdminLayout({ children }: { children: ReactNode }) {
  return (
    <div className="flex min-h-screen bg-gray-100">
      {/* Sidebar */}
      <aside className="w-64 bg-white shadow-md">
        <div className="p-6">
          <h1 className="text-2xl font-bold text-gray-800">Admin Dashboard</h1>
          <p className="text-sm text-gray-600">Crime Analysis System</p>
        </div>
        <nav className="mt-6">
          <ul>
            {menuItems.map((item) => (
              <li key={item.name}>
                <Link
                  href={item.href}
                  className="block px-6 py-3 text-gray-700 hover:bg-gray-200 hover:text-gray-900"
                >
                  {item.name}
                </Link>
              </li>
            ))}
          </ul>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="flex-1 p-6">
        {children}
      </main>
    </div>
  );
}