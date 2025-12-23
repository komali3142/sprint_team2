
import React, { useState } from 'react';

export default function LoginBox({ API, token, onToken }){
  const [email, setEmail] = useState('komali@example.com');
  const [password, setPassword] = useState('Password@123');
  const [name, setName] = useState('Komali');

  async function register(){
    const r = await fetch(`${API}/api/auth/register`, { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({ name, email, password }) });
    const data = await r.json();
    if(data.access_token){ onToken(data.access_token); }
    else alert('Register failed');
  }
  async function login(){
    const r = await fetch(`${API}/api/auth/login`, { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({ email, password, name:'' }) });
    const data = await r.json();
    if(data.access_token){ onToken(data.access_token); }
    else alert('Login failed');
  }
  return (
    <div style={{display:'flex', gap:8, alignItems:'center', marginBottom:16}}>
      <input value={email} onChange={e=>setEmail(e.target.value)} placeholder='email' />
      <input type='password' value={password} onChange={e=>setPassword(e.target.value)} placeholder='password' />
      {token ? (<span style={{color:'green'}}>Logged in</span>) : (
        <>
          <button onClick={login}>Login</button>
          <button onClick={register}>Register</button>
        </>
      )}
    </div>
  );
}
