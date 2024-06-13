'use client'

import CurrencyInput from 'react-currency-input-field';
import { useState, useEffect } from 'react';

function BettingListEntry ({ entry, onDelete, onChange }) {
    const [betResult, setBetResult] = useState(0);
    
    const [betAmount, setBetAmount] = useState(0);

    const [entryState, setEntryState] = useState(0);

    const [betWon, setBetWon] = useState(false);
    
    function handleStartOnClick() {
        setEntryState(1);
        setBetAmount(0);
    }

    function handleSubmitOnClick() {

        /* no backend -> use demo data instead
        postBody = {
            teama: entry.team_a,
            teamb: entry.team_b,
            wettbetrag: betAmount,
            wette: betResult === 0 ? "a" : betResult === 1 ? "b" : "t"
        };
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(postBody)
        };
        fetch('http://localhost:5000/Year', requestOptions)
        .then(response => response.json())
        .then(data => {
            setEntryState(2);
            // @Sören hier die values für state=2 setzen.
        });
        */
        
        let bettingResult = betResult === 0 ? "a" : betResult === 1 ? "b" : "t";
        if (entry.win === bettingResult) setBetWon(true); // bet won
        else setBetWon(false); // bet lost
        setEntryState(2);
        
        


    }

    function handleDoneOnClick() {

        setEntryState(0);
    }

    return (
        
        <div className="border-slate-400 border-4 rounded-2xl mb-3 p-2">
            {entryState == 0  &&
                <div onClick={handleStartOnClick} className='hover:text-blue-600 cursor-pointer flex flex-col max-w-sm mx-auto'>
                    <div className="flex space-x-2 ">
                        <div className="">
                            {entry.team_a}
                        </div>
                        <div className="grow-0">
                            VS
                        </div>
                        <div className="">
                            {entry.team_b}
                        </div>
                    </div>
                </div>
            }
            {entryState == 1 && 
                
                <div className='flex flex-col max-w-sm mx-auto'>
                    <div className="flex space-x-2 mb-5 mt-1">
                        <div className="">
                            {entry.team_a}
                        </div>
                        <div className="grow-0">
                            VS
                        </div>
                        <div className="">
                            {entry.team_b}
                        </div>
                    </div>
                    <div className='relative z-0 w-full mb-5 group'>
                        
                        <CurrencyInput className="block py-2.5 px-0 w-full text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none focus:outline-none focus:ring-0 focus:border-blue-600 peer"
                            prefix="€"
                            id="betting_input"
                            name="input-name"
                            placeholder=' '
                            decimalsLimit={2}
                            onValueChange={(value, name, values) => setBetAmount(values.float)}
                            allowNegativeValue={false}
                            
                        />
                        <label htmlFor="betting_input" className="peer-focus:font-medium absolute text-sm text-gray-500  duration-300 transform -translate-y-6 scale-75 top-3 -z-10 origin-[0] peer-focus:start-0 rtl:peer-focus:translate-x-1/4 rtl:peer-focus:left-auto peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-6">Wettbetrag</label>

                    </div>

                    <div className='mb-5'>
                        {`Wettmultiplikator: ${entry.multiplier}x`}
                    </div>
                    <div className='mb-5'>
                        {`Möglicher Gewinn: ${entry.multiplier*betAmount ? (entry.multiplier*betAmount).toFixed(2) : 0}`}
                    </div>

                    

                    <div className="flex items-center mb-4">
                        <input checked={betResult === 0} onChange={(e) => setBetResult(0)} id="default-radio-1" type="radio" value="" name="bet-result" className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 focus:ring-2 "/>
                        <label htmlFor="default-radio-1" className="ms-2 text-sm font-medium text-gray-900">{`${entry.team_a} gewinnt`}</label>
                    </div>
                    <div className="flex items-center mb-4">
                        <input checked={betResult === 1} onChange={(e) => setBetResult(1)} id="default-radio-2" type="radio" value="" name="bet-result" className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 focus:ring-2 "/>
                        <label htmlFor="default-radio-2" className="ms-2 text-sm font-medium text-gray-900">{`${entry.team_b} gewinnt`}</label>
                    </div>
                    <div className="flex items-center mb-5">
                        <input checked={betResult === 2} onChange={(e) => setBetResult(2)} id="default-radio-3" type="radio" value="" name="bet-result" className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 focus:ring-2 "/>
                        <label htmlFor="default-radio-3" className="ms-2 text-sm font-medium text-gray-900">Unentschieden</label>
                    </div>

                    <button type="button" onClick={handleSubmitOnClick} className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2">
                        Submit
                    </button>
                
                </div>
                
            }

            {entryState == 2 && 
                
                <div className='flex flex-col max-w-sm mx-auto'>
                    <div className='mb-5'>
                        Sie haben €{betWon ? (betAmount*entry.multiplier).toFixed(2) : (0).toFixed(2)} gewonnen.
                    </div>
                    
                    <button type="button" onClick={handleDoneOnClick} className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2">
                        Done
                    </button>
                    
                </div>
            }

           
            
        </div>
       
    )
}



export default function BettingList() {
    
    const [entries, setEntries] = useState([
        { id: 0, team_a: "Eintracht Frankfurt", team_b: "Bayern", multiplier: 2.2, win:"b" },
        { id: 1, team_a: "Union Berlin", team_b: "Hertha", multiplier: 3.0, win:"a" },
        { id: 2, team_a: "Mönchengladbach", team_b: "Hoffenheim", multiplier: 1.5, win:"t" },
        { id: 3, team_a: "Bochum", team_b: "Mainz", multiplier: 1.2, win:"a" },
        { id: 4, team_a: "Augsburg", team_b: "Freiburg", multiplier: 2.4, win:"b" },
        { id: 5, team_a: "Wolfsburg", team_b: "Werder Bremen", multiplier: 2.7, win:"b" },
        { id: 6, team_a: "Dortmund", team_b: "Leverkusen", multiplier: 1.9, win:"t" },
        { id: 7, team_a: "VfB Stuttgart", team_b: "RB Leipzig", multiplier: 2.5, win:"b" },
        { id: 8, team_a: "Köln", team_b: "Schalke", multiplier: 2.6, win:"a" }
    ]);
    

    /* no backend -> use demo data instead
    const [entries, setEntries] = useState([])
    useEffect(() => {
        fetch('http://localhost:5000/Year')
          .then((res) => {
            i = 0
            return res.json().forEach(element => {
                element.id = i++
            });
          })
          .then((data) => {
            console.log(data);
            setEntries(data);
          });
      }, []);
    */



    const handleDelete = (id) => {
        setEntries(entries.filter(entry => entry.id !== id));
    };

    const handleChange = (id, value) => {
        setEntries(entries.map(entry => entry.id === id ? { ...entry, value } : entry));
    };


    return (
        <div>
            {entries.map(entry => (
                <BettingListEntry 
                    key={1} 
                    entry={entry} 
                    onDelete={() => handleDelete(entry.id)} 
                    onChange={handleChange}
                />
            ))}
        </div>
    )
}