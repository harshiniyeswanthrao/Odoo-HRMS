/** @odoo-module **/

import { Component, mount, useState } from "@odoo/owl";

class TaskList extends Component {
    static template = `
        <div>
            <h1>To-Do List</h1>
            <form t-on-submit.prevent="addTask">
                <input t-model="newTask" placeholder="New task..."/>
                <button type="submit">Add</button>
            </form>
            <ul>
                <t t-foreach="tasks" t-as="task" t-key="task.name">
                    <li>
                        <input type="checkbox" t-model="task.is_done"/>
                        <span t-att-class="task.is_done ? 'done' : ''" t-esc="task.name"></span>
                        <button t-on-click="deleteTask(task)">Delete</button>
                    </li>
                </t>
            </ul>
        </div>
    `;

    setup() {
        this.tasks = useState([]);
        this.newTask = "";
    }

    addTask() {
        if (this.newTask) {
            this.tasks.push({ name: this.newTask, is_done: false });
            this.newTask = "";
        }
    }

    deleteTask(task) {
        const index = this.tasks.indexOf(task);
        if (index > -1) {
            this.tasks.splice(index, 1);
        }
    }
}

mount(TaskList, { target: document.body });
