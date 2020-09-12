import React from 'react'
import axios from 'axios'

export default function Buttons(props) {
    return (
        <div style={BtnStyle}>
            <button onClick={addToCart} value={props.id} style={cartBtn}>Add to Cart</button>
            <button onClick={addToWishList} value={props.id} style={wishBtn}>Add to Wishlist</button>
        </div>
    )
}

function addToCart(e){
    axios.post('http://localhost:8000/cart/upsert', {product_id:e.target.value, quantity:1})
    .then(res=>console.log(res.data))
    // alert('Added to Cart');
}

function addToWishList(e){
    console.log(e.target.value)
}

const cartBtn = {
    border:'none',
    background:'#A03037',
    color:'white',
    padding:'5px',
    height:'25px',   
}

let wishBtn = {...cartBtn}

wishBtn.color='black'
wishBtn.background='white'
wishBtn.border='.5px solid black'

const BtnStyle= {
    display:'flex',
    flexDirection:'row',
    flexWrap:'wrap',
    justifyContent:'space-around',
}