import React, { Component } from 'react'

export class DropDown extends Component {
    constructor(props) {
        super(props)
    
        this.state = {
            list:'SortBy'
        }
    }

    handler = (e)=> this.setState({list : e.target.value })
    
    
    render() {
        return (
            <div>
                <select value={this.state.list} onChange={this.handler} style={dropDownStyle}>
                <option value='id'>Relevance</option>
                <option value='price'>Price</option>
                <option value='author'>Author</option>
                <option value='title'>Title</option>
                </select>
            </div>
        )
    }
}

const dropDownStyle = {
    // border: '1px sol'
    padding:'4px'
}

export default DropDown
