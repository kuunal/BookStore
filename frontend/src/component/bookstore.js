import React, { Component } from "react";
import axios from "axios";
import Panel from './secondaryHeader/Panel';
import Item from "./Item";
import Pageno from "./Paginator/Pageno";
import Headers from './headers/Headers'

class BookStore extends Component {
  constructor(props) {
    super(props);

    // this.
    // };
  }
  state = {
    products:[],
    searchby:''
  }

  componentDidMount() {
    axios.get("http://localhost:8000/products/"+this.state.searchby).then((res) => {
      this.setState({
        products: res.data,
      });
    });
  }

  componentDidUpdate(prevProps, prevState, snapShot){  
    axios.get("http://localhost:8000/products/"+this.state.searchby).then((res) => {
      this.setState({
        products: res.data,
      });
    });
  }

  static getDerivedStateFromProps(nextProp, prevState){
    // console.log(nextProp)
    // if (this.props.shared_var !== nextProp){
      return {searchby:nextProp.shared_var}
    // }
  }

  // SearchBy = searchby=>{
  //   console.log(searchby)
  // }

  render() {
    console.log(this.state.searchby)
    return (
      <div className='v' style={{margin:'auto', width:'70%'}}>

      <Panel/>

        <ul style={ulStyle}>
          {this.state.products.map((item, index) => (
            // <li>
              <Item key={index} item={item} />
            // </li>
          ))}
        </ul>
        <Pageno/>
      </div>
    );
  }
}

const ulStyle = {
  // background:'black',
  textAlign: "center",
  display: "grid",
  gridTemplateColumns: '23% 23% 23% 23%',
  gridGap:'2em',
  gridAutoRow: 'minmax(10000px, auto)',
  padding:'10px',
  // marginLeft:'100px',

  // alignItems: "center",
  // justifyContent: "space-around",
  flexWrap: "wrap",
  // flexBasis:'25%'
};
export default BookStore;
