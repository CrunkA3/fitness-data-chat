import { ActivityChart } from "@/components/dashboard/ActivityChart";
import { StatsCard } from "@/components/dashboard/StatsCard";
import { Header } from "@/components/layout/Header";
import { Sidebar } from "@/components/layout/Sidebar";
import { Activity, Clock, Flame, TrendingUp } from "lucide-react";

export default function DashboardPage() {
  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar />
      <div className="flex flex-col flex-1 overflow-hidden">
        <Header title="Dashboard" />
        <main className="flex-1 overflow-y-auto p-6">
          <div className="max-w-7xl mx-auto">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">
              Activity Overview
            </h2>

            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
              <StatsCard
                title="Total Activities"
                value="0"
                icon={<Activity className="h-5 w-5" />}
                description="All time"
                color="blue"
              />
              <StatsCard
                title="Total Distance"
                value="0 km"
                icon={<TrendingUp className="h-5 w-5" />}
                description="All time"
                color="green"
              />
              <StatsCard
                title="Total Time"
                value="0 hrs"
                icon={<Clock className="h-5 w-5" />}
                description="All time"
                color="orange"
              />
              <StatsCard
                title="Calories Burned"
                value="0"
                icon={<Flame className="h-5 w-5" />}
                description="All time"
                color="red"
              />
            </div>

            {/* Charts */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <ActivityChart title="Distance Over Time" type="distance" />
              <ActivityChart title="Heart Rate Trends" type="heartRate" />
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
