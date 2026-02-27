import { useEffect, useState } from "react";
import {
  format,
  startOfMonth,
  endOfMonth,
  startOfWeek,
  endOfWeek,
  addDays,
  addMonths,
  subMonths,
  isSameMonth,
  isSameDay,
  parseISO,
} from "date-fns";
import { eventsApi } from "../api";
import type { Event } from "../api";

export function Calendar() {
  const [month, setMonth] = useState(new Date());
  const [events, setEvents] = useState<Event[]>([]);
  const [selected, setSelected] = useState<Date | null>(null);
  const [detail, setDetail] = useState<Event | null>(null);

  const start = startOfMonth(month);
  const end = endOfMonth(month);
  const startCal = startOfWeek(start);
  const endCal = endOfWeek(end);

  useEffect(() => {
    eventsApi.list(start.toISOString(), end.toISOString()).then(setEvents);
  }, [month]);

  const days: Date[] = [];
  let d = startCal;
  while (d <= endCal) {
    days.push(d);
    d = addDays(d, 1);
  }

  const dayEvents = (date: Date) =>
    events.filter((e) => {
      const s = parseISO(e.start);
      const ed = parseISO(e.end);
      return isSameDay(s, date) || isSameDay(ed, date) || (s <= date && ed >= date);
    });

  const openEvent = (e: Event) => {
    setDetail(e);
    setSelected(null);
  };

  const addEvent = async (date: Date) => {
    const title = prompt("Event title");
    if (!title) return;
    const start = new Date(date);
    start.setHours(9, 0, 0, 0);
    const end = new Date(date);
    end.setHours(10, 0, 0, 0);
    await eventsApi.create({
      title,
      start: start.toISOString(),
      end: end.toISOString(),
    });
    setDetail(null);
    setSelected(null);
    eventsApi.list(startOfMonth(month).toISOString(), endOfMonth(month).toISOString()).then(setEvents);
  };

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <button onClick={() => setMonth(subMonths(month, 1))} className="px-2 py-1 rounded hover:bg-slate-200 dark:hover:bg-slate-700">
          ←
        </button>
        <h2 className="font-semibold text-lg">{format(month, "MMMM yyyy")}</h2>
        <button onClick={() => setMonth(addMonths(month, 1))} className="px-2 py-1 rounded hover:bg-slate-200 dark:hover:bg-slate-700">
          →
        </button>
      </div>

      <div className="grid grid-cols-7 gap-1 text-center text-sm">
        {["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].map((d) => (
          <div key={d} className="font-medium text-slate-500 py-1">{d}</div>
        ))}
        {days.map((day) => {
          const evs = dayEvents(day);
          const inMonth = isSameMonth(day, month);
          return (
            <div
              key={day.toISOString()}
              onClick={() => {
                setSelected(day);
                setDetail(null);
              }}
              className={`min-h-[80px] p-1 rounded cursor-pointer border ${
                inMonth ? "bg-white dark:bg-slate-800" : "bg-slate-100 dark:bg-slate-900 text-slate-400"
              } ${selected && isSameDay(day, selected) ? "ring-2 ring-indigo-500" : ""}`}
            >
              <div className="text-right text-xs">{format(day, "d")}</div>
              {evs.slice(0, 2).map((e) => (
                <div
                  key={e.id}
                  onClick={(ev) => {
                    ev.stopPropagation();
                    openEvent(e);
                  }}
                  className="text-xs truncate px-1 py-0.5 rounded bg-indigo-100 dark:bg-indigo-900/50 text-indigo-800 dark:text-indigo-200"
                >
                  {e.title}
                </div>
              ))}
              {evs.length > 2 && <div className="text-xs text-slate-400">+{evs.length - 2}</div>}
            </div>
          );
        })}
      </div>

      {(selected || detail) && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50" onClick={() => { setDetail(null); setSelected(null); }}>
          <div className="bg-white dark:bg-slate-800 rounded-lg p-4 max-w-md w-full mx-4" onClick={(e) => e.stopPropagation()}>
            {detail ? (
              <>
                <h3 className="font-semibold text-lg">{detail.title}</h3>
                <p className="text-slate-600 dark:text-slate-400 mt-1">{detail.description}</p>
                <p className="text-sm mt-2">
                  {format(parseISO(detail.start), "PPp")} – {format(parseISO(detail.end), "PPp")}
                </p>
              </>
            ) : selected ? (
              <>
                <h3 className="font-semibold">{format(selected, "EEEE, MMM d")}</h3>
                <p className="text-sm text-slate-500 mt-1">
                  {dayEvents(selected).length} event(s)
                </p>
                <button
                  onClick={() => addEvent(selected)}
                  className="mt-4 px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700"
                >
                  Add event
                </button>
              </>
            ) : null}
          </div>
        </div>
      )}
    </div>
  );
}
