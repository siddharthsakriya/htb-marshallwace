import React, { useState } from 'react';
import { useTheme } from '@mui/material/styles';
import { tokens } from '../../theme';
import './styles.css'; // Update this path

const KanbanBoard = () => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    const [newTaskText, setNewTaskText] = useState('');
    const [newTaskName, setNewTaskName] = useState('');

    const listTasksByLane = (tasks) => {
        const lanes = Object.keys(tasks); // Get all lanes

        lanes.forEach(lane => {
            console.log(`Tasks in ${lane}:`);
            tasks[lane].forEach((task, index) => {
                console.log(`${index + 1}. ${task.name} (ID: ${task.id}) - ${task.text}`);
            });
        });
    };
    

    const [tasks, setTasks] = useState({
        Client: [{ id: 1, name: 'hello', text: 'Get groceries' }, { id: 2, name: 'hello', text: 'Feed the dogs' }, { id: 3, name: 'hello', text: 'Mow the lawn' }],
        Trader: [{ id: 5, name: 'hello', text: 'Watch video of a man raising a grocery store lobster as a pet' }],
    });
    const [draggedItem, setDraggedItem] = useState(null);

    const onDragStart = (e, item) => {
        e.dataTransfer.effectAllowed = "move";
        setDraggedItem(item);
    };

    const handleAddTask = (e) => {
        e.preventDefault(); // Prevent form from causing page reload
        if (!newTaskName.trim() || !newTaskText.trim()) return; // Ensure both name and text are not empty
    
        // Generate a unique ID considering all tasks in all lanes
        const allTasks = Object.values(tasks).flat(); // Flatten all tasks into a single array
        const newId = allTasks.reduce((maxId, task) => Math.max(maxId, task.id), 0) + 1;
    
        const newTask = {
            id: newId,
            name: newTaskName, // Include the task name
            text: newTaskText, // Include the task description
        };
    
        // Assume we're adding to the 'Client' lane, adjust as needed
        setTasks(prevTasks => ({
            ...prevTasks,
            Client: [...prevTasks.Client, newTask],
        }));
    
        setNewTaskName(''); // Clear task name input after adding
        setNewTaskText(''); // Clear task description input after adding
    };
    
    
    

    const onDragOver = (e) => {
        e.preventDefault(); // Necessary to allow dropping
    };

    const deleteTask = (lane, taskId) => {
        setTasks(prevTasks => ({
            ...prevTasks,
            [lane]: prevTasks[lane].filter(task => task.id !== taskId),
        }));
    };

    

    const onDrop = (e, lane) => {
        e.preventDefault();
        // Update tasks to move the dragged item to the new lane
        const updatedTasks = { ...tasks };
        // Remove from current lane
        updatedTasks[draggedItem.lane] = updatedTasks[draggedItem.lane].filter(task => task.id !== draggedItem.task.id);
        // Add to new lane
        updatedTasks[lane].push(draggedItem.task);

        setTasks(updatedTasks);
        setDraggedItem(null); // Clear the dragged item
    };

    return (
        <div className="board">
           
            <form onSubmit={handleAddTask} style={{ backgroundColor: colors.primary[400], color: colors.grey[100]}}>
                <input
                    type="text"
                    placeholder="Task name..."
                    value={newTaskName}
                    onChange={(e) => setNewTaskName(e.target.value)}
                    style={{marginLeft: '30px', marginTop: '20px', padding: '10px 22px'}}
                />
                <textarea
                    placeholder="Add new task description..."
                    value={newTaskText}
                    onChange={(e) => setNewTaskText(e.target.value)}
                    style={{
                        marginLeft: '30px',
                        marginTop: '22px',
                        padding: '10px 25px',
                        width: 'calc(100% - 60px)', // Adjusts width considering marginLeft and marginRight
                        height: '150px', // Sets an initial height to accommodate multi-line text
                        resize: 'both', // Allows the user to resize both vertically and horizontally
                        display: 'block', // Ensures the textarea is properly block-level for layout
                        fontFamily: 'sans-serif', // Matches the font of the rest of the form
                        fontSize: '16px', // Adjust as needed for readability
                        backgroundColor: '#fff', // Background color of the textarea
                        color: '#000', // Text color
                        border: '1px solid #ddd', // Border color
                        borderRadius: '5px', // Rounded corners
                    }}
                />
                <button
                    type="submit"
                    style={{
                        marginTop: '15px',
                        marginLeft: '55px',
                        padding: '10px 35px',
                        fontFamily: 'sans-serif',
                        fontSize: '18px',
                        backgroundColor: colors.greenAccent[400],
                        color: colors.grey[100],
                        border: 'none',
                        borderRadius: '5px',
                        cursor: 'pointer',
                        boxShadow: '0 4px 8px rgba(0, 0, 0, 0.2)',
                        transition: 'background-color 0.3s, transform 0.2s',
                    }}
                >
                    Add Task
                </button>
            </form>

            {/* Existing Kanban board layout */}
            {Object.keys(tasks).map((lane) => (
                <div key={lane} className="lane"
                    onDragOver={onDragOver}
                    onDrop={(e) => onDrop(e, lane)}
                    style={{ backgroundColor: colors.primary[400], color: colors.greenAccent[400] }}>
                    <h3>{lane.toUpperCase()}</h3>
                    {tasks[lane].map((task, index) => (
                        <div key={task.id} draggable
                            onDragStart={(e) => onDragStart(e, { lane, task })}
                            className="task"
                            style={{ /* inline styles if necessary, but prefer class-based styling */ }}>
                            <div className="task-name">{task.name}</div>
                            <div className="task-text" style={{ /* additional inline styles if necessary */ }}>
                                {task.text}
                            </div>
                            <button
                                onClick={(e) => {
                                    e.stopPropagation(); // Prevent drag initiation when clicking the button
                                    deleteTask(lane, task.id);
                                }}
                                style={{
                                    position: 'absolute',
                                    top: '5px',
                                    right: '5px',
                                    /* styling for your delete button */
                                }}
                            >
                                &#x2715; {/* 'X' icon or similar for delete */}
                            </button>
                        </div>
                    ))}
                </div>
            ))}
        </div>
    );


    
    
};

export default KanbanBoard;
