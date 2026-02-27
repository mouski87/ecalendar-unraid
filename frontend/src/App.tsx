import { Calendar } from "./components/Calendar";
import { Chores } from "./components/Chores";
import { TodoLists } from "./components/TodoLists";
import { Weather } from "./components/Weather";

function App() {
  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-900 text-slate-900 dark:text-slate-100">
      <header className="border-b border-slate-200 dark:border-slate-700 px-4 py-3">
        <h1 className="text-xl font-bold">eCalendar</h1>
      </header>

      <main className="grid grid-cols-1 lg:grid-cols-3 gap-6 p-4">
        <section className="lg:col-span-2">
          <Calendar />
        </section>

        <aside className="space-y-6">
          <Weather city="London" />
          <Chores />
          <TodoLists />
        </aside>
      </main>
    </div>
  );
}

export default App;
