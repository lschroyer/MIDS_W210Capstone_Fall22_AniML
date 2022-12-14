import React from "react";
import { BrowserRouter, Route, Link } from "react-router-dom";

function Navbar() {
  return (
    <nav>
      <ul>
        <li>
          <Link to="/">Home</Link>
        </li>
        <li>
          <Link to="/contact">Contact</Link>
        </li>
        <li>
          <Link to="/boundingbox">BoundingBox</Link>
        </li>
        <li>
          <Link to="/uploadimages">UploadImages</Link>
        </li>
      </ul>
    </nav>
  );
}

export default Navbar;