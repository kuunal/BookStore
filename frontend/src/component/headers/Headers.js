import React from "react";
import SearchBar from "./SearchBar";
import Main from "./Main";
import Cart from "./Cart";

export default function Headers(props) {
  return (
    <div style={headerStyle}>
      <div style={headerContents}>
        <Main />
        {/* </div> */}
        {/* <div style={{background:'yellow', flex:'2'}}> */}
        <SearchBar SearchBy={props.SearchBy}/>
        <Cart/>
      </div>
    </div>
  );
}

const headerStyle = {
  background: "#A03037",
  padding: "10px",
  // display:'flex',
};

const headerContents = {
//   background: "black",
  margin: "0 auto",
  width: "70%",
  display:'flex'
};
