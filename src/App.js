import { useState } from 'react';
import React from "react";
import './App.css';



function App() {
 
  const [news,setNews]=useState("");
  const [data, setData] = useState("");
  const handleClick = async () => {
    setNews(news);
    setData("");
    const response = await fetch("http://localhost:5000/data", {
      method: "POST",
      // mode: 'no-cors',  
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ arg: news })
    })
    const jsonData = await response.json();
    console.log(jsonData);
    setData(jsonData);
  };


  return (
    <div className="App text-center p-3 " >
      <h2>Fakespeare</h2>
      <h3>True be or not True be.....</h3>
      <form>
      <input  className='p-3' type='text' onChange={(val)=>setNews(val.target.value)}/>
        <button
        type="button" onClick={handleClick} className="btn btn-outline-dark m-5 ">Search</button>
      {data.length>0 && 
      <div className='text-center'>
        <p className='display-9 text-dark'>{news}</p>
        <p className='display-4 text-dark'>{data}</p>
        </div>
      }
      </form> 
      
    </div>
  );
}

export default App;
