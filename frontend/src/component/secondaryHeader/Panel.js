import React, { Component } from 'react'
import DropDown from './DropDown'

export class Panel extends Component {
    render() {
        return (
            <div style={secondaryHeaderStyle}>
                <h2 style={{flex:'1'}}>Books</h2>
                <DropDown/>
            </div>
        )
    }
}

const secondaryHeaderStyle = {
    display:'flex',
    flexWrap:'wrap',
    padding:'10px'

}


export default Panel
