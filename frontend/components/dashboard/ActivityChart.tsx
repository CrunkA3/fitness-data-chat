"use client";

import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

interface ActivityChartProps {
  title: string;
  type: "distance" | "heartRate" | "duration";
}

// Sample data for demonstration
const distanceData = [
  { date: "Mon", value: 5.2 },
  { date: "Tue", value: 0 },
  { date: "Wed", value: 8.1 },
  { date: "Thu", value: 3.5 },
  { date: "Fri", value: 0 },
  { date: "Sat", value: 12.0 },
  { date: "Sun", value: 6.3 },
];

const heartRateData = [
  { date: "Mon", value: 145 },
  { date: "Tue", value: 0 },
  { date: "Wed", value: 152 },
  { date: "Thu", value: 138 },
  { date: "Fri", value: 0 },
  { date: "Sat", value: 158 },
  { date: "Sun", value: 143 },
];

const dataMap = {
  distance: { data: distanceData, label: "Distance (km)", color: "#3b82f6" },
  heartRate: { data: heartRateData, label: "Avg Heart Rate (bpm)", color: "#ef4444" },
  duration: { data: distanceData, label: "Duration (min)", color: "#10b981" },
};

export function ActivityChart({ title, type }: ActivityChartProps) {
  const { data, label, color } = dataMap[type];

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
      <h3 className="text-base font-semibold text-gray-900 mb-4">{title}</h3>
      <ResponsiveContainer width="100%" height={200}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
          <XAxis
            dataKey="date"
            tick={{ fontSize: 12, fill: "#9ca3af" }}
            axisLine={false}
            tickLine={false}
          />
          <YAxis
            tick={{ fontSize: 12, fill: "#9ca3af" }}
            axisLine={false}
            tickLine={false}
          />
          <Tooltip
            contentStyle={{
              borderRadius: "8px",
              border: "1px solid #e5e7eb",
              boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
            }}
            labelStyle={{ fontSize: 12 }}
            itemStyle={{ fontSize: 12 }}
          />
          <Line
            type="monotone"
            dataKey="value"
            stroke={color}
            strokeWidth={2}
            dot={{ fill: color, strokeWidth: 0, r: 4 }}
            activeDot={{ r: 6 }}
            name={label}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
