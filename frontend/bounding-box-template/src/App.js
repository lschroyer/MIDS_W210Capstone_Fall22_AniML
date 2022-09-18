import React from "react";
import Boundingbox from "react-bounding-box";

export default function App() {
  const params = {
    image:
      "https://images.unsplash.com/photo-1612831660296-0cd5841b89fb?ixid=MXwxMjA3fDF8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=700&q=80",
    boxes: [[400, 100, 250, 250]]
  };

  return <Boundingbox image={params.image} boxes={params.boxes} />;
}
