
// https://www.youtube.com/watch?v=hQAHSlTtcmY&ab_channel=WebDevSimplified
import React, { useState, useRef, useEffect } from "react";
import ToDoList from "./ToDoList";
// import uuidv4 from 'uuid/v4'
import { v4 as uuidv4 } from 'uuid';

const LOCAL_STORAGE_KEY = 'todoApp.todos'

function ToDoApp() {
  const [todos, setTodos] = useState([])
  const todoNameRef = useRef()
  
  useEffect(() => {
    const storedTodos = JSON.parse(localStorage.getItem(LOCAL_STORAGE_KEY))
    if (storedTodos) setTodos(storedTodos)
  }, [])

  useEffect(() => {
    localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(todos))
  }, [todos])

  function toggleToDo(id){
    const newTodos = [...todos]
    const todo = newTodos.find(todo => todo.id === id)
    todo.complete = !todo.complete
    setTodos(newTodos)
  }
  
  function handleAddTodo(e) {
    const name = todoNameRef.current.value
    if (name === '') return
    setTodos(prevToDos => {
      return[...prevToDos, { id:uuidv4(), name:name, complete:false }]
    })
    todoNameRef.current.value = null
  }

  function hanldleClearToDos(){
    const newTodos = todos.filter(todo => !todo.complete)
    setTodos(newTodos)
  }


  return (
    <>
      <ToDoList todos ={todos} toggleToDo={toggleToDo}/>
      <input ref={todoNameRef} type = "text"/>
      <button onClick={handleAddTodo}>Add ToDo</button>
      <button onClick={hanldleClearToDos}>Clear Completed</button>
      <div>{todos.filter(todo => !todo.complete).length} left ToDo</div>
    </>
  )
}

export default ToDoApp;



// import Boundingbox from "react-bounding-box";

// function App() {
//   const params = {
//     image:
//       "https://images.unsplash.com/photo-1612831660296-0cd5841b89fb?ixid=MXwxMjA3fDF8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=700&q=80",
//     boxes: [[400, 100, 250, 250]]
//   };

//   return <Boundingbox image={params.image} boxes={params.boxes} />;
// }