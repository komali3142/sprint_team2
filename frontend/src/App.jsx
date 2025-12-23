
import React, { useEffect, useState } from 'react';
import LoginBox from './components/LoginBox.jsx';
import ChatWidget from './components/ChatWidget.jsx';

const API = 'http://localhost:8000';

function App(){
  const [products, setProducts] = useState([]);
  const [cart, setCart] = useState([]);
  const [token, setToken] = useState(localStorage.getItem('token') || '');

  useEffect(()=>{
    fetch(`${API}/api/products`)
      .then(r=>r.json()).then(setProducts);
  },[]);

  function addToCart(p){
    setCart(prev => {
      const existing = prev.find(i=> i.product_id === p.product_id);
      if (existing){
        return prev.map(i=> i.product_id===p.product_id ? {...i, quantity: i.quantity+1} : i);
      }
      return [...prev, { product_id: p.product_id, product_name: p.product_name, sku: p.sku, unit_price: Number(p.price), quantity: 1 }];
    });
  }

  async function checkout(){
    if(!token){ alert('Please login first'); return; }
    const payload = {
      user_id: 0, // backend uses token's sub
      items: cart,
      shipping_address_id: null,
      billing_address_id: null
    };
    const r = await fetch(`${API}/api/orders/checkout`, { method:'POST', headers:{'Content-Type':'application/json','Authorization':`Bearer ${token}`}, body: JSON.stringify(payload)});
    if(!r.ok){ const t=await r.text(); alert('Checkout failed: '+t); return; }
    const data = await r.json();
    alert('Order created: '+data.order_number);
    setCart([]);
  }

  return (
    <div style={{fontFamily:'system-ui', padding:20}}>
      <h1>FastAPI RAG Cart</h1>
      <LoginBox API={API} token={token} onToken={t=>{localStorage.setItem('token', t); setToken(t);}} />

      <h2>Products</h2>
      <div style={{display:'grid', gridTemplateColumns:'repeat(3, 1fr)', gap:16}}>
        {products.map(p=> (
          <div key={p.product_id} style={{border:'1px solid #ddd', padding:12}}>
            <div style={{fontWeight:600}}>{p.product_name}</div>
            <div>₹ {p.price}</div>
            <div style={{fontSize:12, color:'#555'}}>{p.description}</div>
            <button onClick={()=>addToCart(p)} style={{marginTop:8}}>Add to cart</button>
          </div>
        ))}
      </div>

      <h2 style={{marginTop:24}}>Cart</h2>
      {cart.length===0 ? <div>No items yet.</div> : (
        <div>
          {cart.map((it,i)=> (
            <div key={i} style={{display:'flex', gap:8}}>
              <div>{it.product_name}</div>
              <div>x {it.quantity}</div>
              <div>₹ {Number(it.unit_price)*it.quantity}</div>
            </div>
          ))}
          <button onClick={checkout} style={{marginTop:8}}>Checkout</button>
        </div>
      )}

      <ChatWidget API={API} />
    </div>
  );
}
export default App;
