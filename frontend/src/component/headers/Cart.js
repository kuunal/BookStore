import React, { Component } from 'react'
import axios from 'axios'

export class Cart extends Component {
    constructor(props) {
        super(props)
    
        this.state = {
            cartItems: ''
        }
    }

    // componentDidMount(){
    //     axios.get('http://localhost:8000/ ')
    // }
    
    render() {
        return (
            <div style={cartHeaderStyle}>
                Cart
                <img src="https://public-v2links.adobecc.com/f01e3875-2a95-4975-7ad1-9a60aa079aec/component?params=component_id%3A6861d6b7-251c-4183-b182-3281feb8b845&params=version%3A0&token=1599288995_da39a3ee_de376559630c81d97346ca6266b6b24e858dbe3c&api_key=CometServer1" height='30'/>    
            </div>
        )
    }
}

const cartHeaderStyle = {
    color:'white',
    // alignItem:'end',
    justifyContent:'flex-start',
    cursor:'pointer'
}

export default Cart
