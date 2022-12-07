import React from "react";
import ToDo from "./ToDo";

export default function ToDoList({ todos, toggleToDo }) {
  return (
    todos.map(todo => {
        return <ToDo key={todo.id} toggleToDo={toggleToDo} todo={todo} />
    })
  )
}