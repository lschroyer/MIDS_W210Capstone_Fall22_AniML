import React from "react";

export default function ToDo({ todo, toggleToDo }) {
  function handleTodoClick(){
    toggleToDo(todo.id)
  }
  
  return (
    <div>
        <label>
        <input type="checkbox" checked={todo.complete} onChange={handleTodoClick} />
        {todo.name}
        </label>
     
    </div>
  )
}