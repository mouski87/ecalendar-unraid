import { useEffect, useState } from "react";
import { listsApi } from "../api";
import type { TodoList, TodoItem } from "../api";

export function TodoLists() {
  const [lists, setLists] = useState<TodoList[]>([]);
  const [items, setItems] = useState<Record<number, TodoItem[]>>({});
  const [selected, setSelected] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);

  const loadLists = () =>
    listsApi.list().then((l) => {
      setLists(l);
      setSelected((prev) => (l.length && !prev ? l[0].id : prev));
    });
  const loadItems = (id: number) => listsApi.items(id).then((i) => setItems((prev) => ({ ...prev, [id]: i })));

  useEffect(() => {
    loadLists().finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    if (selected) loadItems(selected);
  }, [selected]);

  const addList = async () => {
    const title = prompt("List name");
    if (!title) return;
    const l = await listsApi.create({ title });
    setLists((prev) => [...prev, l]);
    setSelected(l.id);
  };

  const addItem = async () => {
    if (!selected) return;
    const title = prompt("Item");
    if (!title) return;
    await listsApi.addItem(selected, title);
    loadItems(selected);
  };

  const toggleItem = async (listId: number, item: TodoItem) => {
    await listsApi.updateItem(listId, item.id, { completed: !item.completed });
    loadItems(listId);
  };

  const delItem = async (listId: number, itemId: number) => {
    await listsApi.deleteItem(listId, itemId);
    loadItems(listId);
  };


  if (loading) return <div>Loading...</div>;

  const currentItems = selected ? items[selected] ?? [] : [];

  return (
    <div>
      <div className="flex items-center justify-between mb-2">
        <h2 className="font-semibold text-lg">Lists</h2>
        <button onClick={addList} className="px-2 py-1 bg-indigo-600 text-white rounded text-sm hover:bg-indigo-700">
          New list
        </button>
      </div>
      <div className="flex gap-2 mb-2 overflow-x-auto pb-2">
        {lists.map((l) => (
          <button
            key={l.id}
            onClick={() => setSelected(l.id)}
            className={`px-3 py-1 rounded text-sm whitespace-nowrap ${selected === l.id ? "bg-indigo-600 text-white" : "bg-slate-200 dark:bg-slate-700"}`}
          >
            {l.title}
          </button>
        ))}
      </div>
      {selected && (
        <>
          <div className="flex justify-between mb-2">
            <span className="text-sm text-slate-500">{lists.find((l) => l.id === selected)?.title}</span>
            <button onClick={addItem} className="text-indigo-600 text-sm">+ Add</button>
          </div>
          <ul className="space-y-1">
            {currentItems.map((i) => (
              <li key={i.id} className="flex items-center gap-2 p-1">
                <input
                  type="checkbox"
                  checked={i.completed}
                  onChange={() => toggleItem(selected, i)}
                />
                <span className={i.completed ? "line-through text-slate-500" : ""}>{i.title}</span>
                <button onClick={() => delItem(selected, i.id)} className="ml-auto text-red-500">×</button>
              </li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
}
