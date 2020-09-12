import React from "react";
import "./App.css";
import BookStore from "./component/bookstore";
import Headers from "./component/headers/Headers";
import { Component } from "react";

export class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      shared_var: "",
    };
  }
  SearchBy = (searchBy) =>
    this.setState({
      shared_var: searchBy,
    });

  render() {
    return (
      <div className="App">
        <Headers SearchBy={this.SearchBy} />
        <BookStore shared_var={this.state.shared_var} />
      </div>
    );
  }
}

export default App;
