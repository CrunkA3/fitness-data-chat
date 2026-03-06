import Link from "next/link";
import { Activity, BarChart3, MessageSquare } from "lucide-react";

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-gray-50 to-white">
      {/* Hero Section */}
      <div className="container mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <div className="flex justify-center mb-6">
            <Activity className="h-16 w-16 text-blue-600" />
          </div>
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            Fitness Data Chat
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto mb-8">
            Analyze your Strava and Garmin fitness data with an AI-powered chat
            interface. Ask questions, get insights, and visualize your training.
          </p>
          <div className="flex gap-4 justify-center">
            <Link
              href="/chat"
              className="bg-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
            >
              Start Chatting
            </Link>
            <Link
              href="/dashboard"
              className="bg-white text-blue-600 border border-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-blue-50 transition-colors"
            >
              View Dashboard
            </Link>
          </div>
        </div>

        {/* Features */}
        <div className="grid md:grid-cols-3 gap-8 max-w-4xl mx-auto">
          <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
            <MessageSquare className="h-10 w-10 text-blue-600 mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              AI-Powered Chat
            </h3>
            <p className="text-gray-600">
              Ask natural language questions about your training data. Get
              instant insights powered by GPT-4.
            </p>
          </div>
          <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
            <BarChart3 className="h-10 w-10 text-green-600 mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Visual Analytics
            </h3>
            <p className="text-gray-600">
              Interactive charts for distance trends, heart rate zones, and
              activity comparisons.
            </p>
          </div>
          <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
            <Activity className="h-10 w-10 text-orange-600 mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Multi-Platform Sync
            </h3>
            <p className="text-gray-600">
              Connect both Strava and Garmin to get a complete picture of your
              fitness journey.
            </p>
          </div>
        </div>

        {/* Example Queries */}
        <div className="mt-16 max-w-2xl mx-auto">
          <h2 className="text-2xl font-bold text-gray-900 text-center mb-8">
            Example Questions
          </h2>
          <div className="space-y-3">
            {[
              "Show me my running progress this month",
              "What's my average heart rate during cycling?",
              "Create a chart comparing my activities this week",
              "How many kilometers did I run last month?",
              "What are my best performing workouts?",
            ].map((query) => (
              <div
                key={query}
                className="bg-gray-50 border border-gray-200 rounded-lg px-4 py-3 text-gray-700"
              >
                &ldquo;{query}&rdquo;
              </div>
            ))}
          </div>
        </div>
      </div>
    </main>
  );
}
