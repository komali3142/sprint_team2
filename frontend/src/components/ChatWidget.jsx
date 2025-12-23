
import React, { useState } from 'react';

export default function ChatWidget({ API }){
  const [open, setOpen] = useState(true);
  const [query, setQuery] = useState('Recommend a phone under ₹30k');
  const [answer, setAnswer] = useState('');

  async function ask(){
    const r = await fetch(`${API}/api/chat`, { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({ query }) });
    const data = await r.json();
    setAnswer(data.answer || JSON.stringify(data, null, 2));
  }

  return (
    <div style={{position:'fixed', right:20, bottom:20}}>
      <div style={{background:'#222', color:'#fff', padding:8, borderRadius:6, cursor:'pointer'}} onClick={()=>setOpen(!open)}>
        Chat Assistant
      </div>
      {open && (
        <div style={{width:320, border:'1px solid #ddd', background:'#fff', padding:12, borderRadius:6, boxShadow:'0 4px 12px rgba(0,0,0,0.1)'}}>
          <textarea rows={3} value={query} onChange={e=>setQuery(e.target.value)} style={{width:'100%'}} />
          <button onClick={ask} style={{marginTop:8}}>Ask</button>
          <pre style={{whiteSpace:'pre-wrap', marginTop:8}}>{answer}</pre>
        </div>
      )}
    </div>
  );
}
