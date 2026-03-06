import Link from "next/link";
import { Activity } from "lucide-react";

interface HeaderProps {
  title: string;
}

export function Header({ title }: HeaderProps) {
  return (
    <header className="bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between">
      <div className="flex items-center gap-3">
        <Link href="/" className="flex items-center gap-2">
          <Activity className="h-6 w-6 text-blue-600" />
          <span className="font-bold text-gray-900">FitChat</span>
        </Link>
        <span className="text-gray-300">/</span>
        <h1 className="text-gray-900 font-semibold">{title}</h1>
      </div>
      <div className="flex items-center gap-3">
        <button className="text-sm text-gray-600 hover:text-gray-900 transition-colors">
          Connect Strava
        </button>
        <button className="text-sm text-gray-600 hover:text-gray-900 transition-colors">
          Connect Garmin
        </button>
      </div>
    </header>
  );
}
