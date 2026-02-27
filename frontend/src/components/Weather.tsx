import { useEffect, useState } from "react";
import { weatherApi } from "../api";
import type { Weather as WeatherType } from "../api";

export function Weather({ city = "London" }: { city?: string }) {
  const [w, setW] = useState<WeatherType | null>(null);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    weatherApi.get(city).then(setW).catch((e) => setErr(e.message));
  }, [city]);

  if (err) return <div className="text-red-500 text-sm">Weather: {err}</div>;
  if (!w) return <div className="text-slate-500 text-sm">Loading weather...</div>;

  return (
    <div className="rounded-lg bg-slate-100 dark:bg-slate-800 p-3 text-sm">
      <div className="font-medium text-slate-600 dark:text-slate-400">{w.city}</div>
      <div className="text-2xl font-bold">{Math.round(w.temp)}°</div>
      <div className="text-slate-500">{w.description}</div>
      <div className="mt-1 text-xs text-slate-400">
        Feels {Math.round(w.feels_like)}° · {w.humidity}% humidity · {w.wind_speed} m/s
      </div>
    </div>
  );
}
