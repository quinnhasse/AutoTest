// Importing required modules
const express = require('express');
const fs = require('fs');

// Create a new Express application
const app = express();
app.use(express.json());

// JSON file to store the TODO items
const todoDataPath = 'todoData.json';

// Load the existing TODO items from the JSON file
let todoData = [];
if (fs.existsSync(todoDataPath)) {
    const data = fs.readFileSync(todoDataPath);
    todoData = JSON.parse(data);
}

// Route to get all TODO items
app.get('/todos', (req, res) => {
    res.json(todoData);
});

// Route to add a new TODO item
app.post('/todos', (req, res) => {
    const newTodo = req.body;
    todoData.push(newTodo);
    fs.writeFileSync(todoDataPath, JSON.stringify(todoData));
    res.json({ message: 'TODO item added successfully', todo: newTodo });
});

// Route to update a TODO item
app.put('/todos/:id', (req, res) => {
    const todoId = req.params.id;
    const updatedTodo = req.body;

    const index = todoData.findIndex(todo => todo.id === parseInt(todoId));
    if (index !== -1) {
        todoData[index] = updatedTodo;
        fs.writeFileSync(todoDataPath, JSON.stringify(todoData));
        res.json({ message: 'TODO item updated successfully', todo: updatedTodo });
    } else {
        res.status(404).json({ message: 'TODO item not found' });
    }
});

// Route to delete a TODO item
app.delete('/todos/:id', (req, res) => {
    const todoId = req.params.id;

    const index = todoData.findIndex(todo => todo.id === parseInt(todoId));
    if (index !== -1) {
        todoData.splice(index, 1);
        fs.writeFileSync(todoDataPath, JSON.stringify(todoData));
        res.json({ message: 'TODO item deleted successfully' });
    } else {
        res.status(404).json({ message: 'TODO item not found' });
    }
});

// Start the server on port 3000
const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});