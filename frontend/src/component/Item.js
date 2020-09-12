import React from "react";
import Buttons from './Buttons'

function Item(props) {
  const { id, author, title, image, quantity, price, description } = props.item;
  return (
    <li style={listStyle}>
      <div style={{ height:'150px' }}>
        <p style={{padding:'10px',background:'#f4f4f4'}}><img src={image.slice(0, -1)}  height='120'/></p>
      </div>
      <div style={{ height:'100px', fontSize:'90%'}}>
          <div style={{height:'70%'}}>
        <p style={{textAlign:'left'}}>{title}</p>
        <p style={{textAlign:'left', color:'gray', fontStyle:'bold', fontSize:"0.5em"}}>By {author}</p>
        <p style={{textAlign:'left'}}>Rs. {price}</p>
        </div>
        {
        (quantity !== 0) ?
        (<Buttons id={id}/>)
        : null
      }
      
      </div>
    </li>
  );
}




const listStyle = {
  borderRadius: "3px",
  margin: "0px",
  border: "1px  solid #F5F5F5",
  // flexBasis:'200px',
  // flexGrow:'3px',
  display:'flex',
  boxShadow:'0.5px 0.5px 4px black',
//   flexBasis:'50%',
  flexDirection:'column',
};

export default Item;
