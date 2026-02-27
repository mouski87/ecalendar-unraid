import { useEffect, useState } from "react";
import { choresApi } from "../api";
import type { Chore } from "../api";
import { format } from "date-fns";

export function Chores() {
  const [chores, setChores] = useState<Chore[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCompleted, setShowCompleted] = useState(false);

  const load = () => choresApi.list({ completed: showCompleted ? undefined : false }).then(setChores).finally(() => setLoading(false));

  useEffect(() => {
    load();
  }, [showCompleted]);

  const toggle = async (c: Chore) => {
    await choresApi.update(c.id, { completed: !c.completed });
    load();
  };

  const add = async () => {
    const title = prompt("Chore title");
    if (!title) return;
    await choresApi.create({ title });
    load();
  };

  const del = async (id: number) => {
    if (!confirm("Delete?")) return;
    await choresApi.delete(id);
    load();
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <div className="flex items-center justify-between mb-2">
        <h2 className="font-semibold text-lg">Chores</h2>
        <div className="flex gap-2">
          <label className="text-sm flex items-center gap-1">
            <input type="checkbox" checked={showCompleted} onChange={(e) => setShowCompleted(e.target.checked)} />
            Show done
          </label>
          <button onClick={add} className="px-2 py-1 bg-indigo-600 text-white rounded text-sm hover:bg-indigo-700">
            Add
          </button>
        </div>
      </div>
      <ul className="space-y-2">
        {chores.map((c) => (
          <li
            key={c.id}
            className="flex items-center gap-2 p-2 rounded bg-slate-100 dark:bg-slate-800"
          >
            <input
              type="checkbox"
              checked={c.completed}
              onChange={() => toggle(c)}
              className="rounded"
            />
            <span className={c.completed ? "line-through text-slate-500" : ""}>
              {c.title}
              {c.due_date && (
                <span className="text-xs ml-1 text-slate-400">
                  {format(new Date(c.due_date), "MMM d")}
                </span>
              )}
            </span>
            <button onClick={() => del(c.id)} className="ml-auto text-red-500 text-sm">
              ×
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
