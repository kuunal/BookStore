import React, { Component } from "react";

export class SearchBar extends Component {
  constructor(props) {
    super(props);

    this.state = {
      searchby: "",
    };
  }

  onSubmit = (e) => {
    e.preventDefault();
    // console.log(this.state.searchby);
    this.props.SearchBy(this.state.searchby)
    this.setState({
      searchby: "",
    });
  };

  searchProduct = (e) => {
    this.setState({
      [e.target.name]: e.target.value,
    });
  };

  render() {
    return (
      <form onSubmit={this.onSubmit} style={searchFormStyle}>
        <input
          type="text"
          name="searchby"
          onChange={this.searchProduct}
          value={this.state.searchby}
          style={inputStyle}
          placeholder="search..."
        />
      </form>
    );
  }
}

const inputStyle = {
  // // background:'black',
  // padding:'10px',
  // marginLeft:'10px',
  flex:'3',
  // justifyContent:'space-around',
//   padding: "10px",
border:'none',
borderRadius:'5px',
alignItems:'center',
height:'90%',
  width:'60%',
  marginLeft:'10px',
};

const searchFormStyle = {
    flex:'1'
}

export default SearchBar;
