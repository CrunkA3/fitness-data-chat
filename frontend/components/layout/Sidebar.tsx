"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Activity, BarChart3, MessageSquare, Settings } from "lucide-react";

const navItems = [
  { href: "/chat", icon: MessageSquare, label: "Chat" },
  { href: "/dashboard", icon: BarChart3, label: "Dashboard" },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-16 bg-gray-900 flex flex-col items-center py-4 gap-2">
      <Link href="/" className="p-3 mb-4">
        <Activity className="h-6 w-6 text-white" />
      </Link>
      {navItems.map(({ href, icon: Icon, label }) => (
        <Link
          key={href}
          href={href}
          title={label}
          className={`p-3 rounded-xl transition-colors ${
            pathname === href
              ? "bg-blue-600 text-white"
              : "text-gray-400 hover:text-white hover:bg-gray-800"
          }`}
        >
          <Icon className="h-5 w-5" />
        </Link>
      ))}
      <div className="flex-1" />
      <Link
        href="/settings"
        title="Settings"
        className="p-3 text-gray-400 hover:text-white hover:bg-gray-800 rounded-xl transition-colors"
      >
        <Settings className="h-5 w-5" />
      </Link>
    </aside>
  );
}
