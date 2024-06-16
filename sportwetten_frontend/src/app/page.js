import BettingList from './betting_list.js';
import TopBar from './top_bar.js';

export default function Home() {
  return (
    <main>
      <TopBar />

      <div className="flex min-h-screen flex-col items-center  p-24">
        <BettingList />
      </div>

      <footer className="bg-white rounded-lg shadow m-4 dark:bg-gray-100">
          <div className="w-full mx-auto max-w-screen-xl p-4 md:flex md:items-center md:justify-between">
            <span className="text-sm text-gray-500 sm:text-center dark:text-gray-400"><a href="https://www.flaticon.com/free-icons/betting" title="betting icon" className="hover:underline">Betting icon created by Freepik - Flaticon</a>
            </span>
          </div>
      </footer>

    </main>
    
  );
}
