
/** @odoo-module **/
import { Component, onMounted, useState, useRef } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { loadJS } from "@web/core/assets"; // Load Chart.js dynamically
import { xml } from "@odoo/owl";

class GraphComponent extends Component {
    static template = xml`
        <div class="graph-container">
            <canvas t-ref="chartCanvas"></canvas>
        </div>
    `;

    setup() {
        this.state = useState({ data: [] });
        this.chartRef = useRef("chartCanvas");

        onMounted(async () => {
            await loadJS("https://cdn.jsdelivr.net/npm/chart.js"); // Load Chart.js dynamically
            const { active_id } = this.props.action.context;

            if (!active_id) {
                console.error("No active_id found!");
                return;
            }

            console.log("Fetching data for active_id:", active_id);

            // Fetch data from production.planning model with machine_id and related fields
            let records = await this.env.services.orm.searchRead("production.planning", [["planning_name_id", "=", active_id]],
                ["total_shifts", "available_shifts", "shortage_shifts", "machine_id"]);

            // Store fetched data in component state
            this.state.data = records;
            this.renderChart();
        });
    }

    renderChart() {
        const canvas = this.chartRef.el;
        if (!canvas) {
            console.error("Canvas element not found");
            return;
        }

        const ctx = canvas.getContext("2d");

        // Destroy any existing Chart instance before creating a new one
        if (this.chartInstance) {
            this.chartInstance.destroy();
        }
        // Create chart with Chart.js
        new Chart(ctx, {
            type: "bar",
            data: {
                labels: this.state.data.map(d => d.machine_id && d.machine_id[1] ? d.machine_id[1] : `Machine ${d.id}`), // Use machine_id.name for the label
                datasets: [
                    {
                        label: "Available Shifts",
                        data: this.state.data.map(d => d.available_shifts),
                        backgroundColor: "blue",
                        stack: "stack1",
                    },
                    {
                        label: "Loaded Shifts",
                        data: this.state.data.map(d => d.total_shifts),
                        backgroundColor: "green",
                        stack: "stack2",
                    },
                    {
                        label: "Excess/Shortage Shifts",
                        data: this.state.data.map(d => d.shortage_shifts),
                        backgroundColor: "red",
                        stack: "stack2",
                    }
                ]
            },
            options: {
                responsive: true,
                scales: {
                x: {
                    stacked: true,
                },
                y: {
                    stacked: true,
                    beginAtZero: true
                }
            }
            }
        });
    }
}

// Register the component as a client action
registry.category("actions").add("action_machine_analysis", GraphComponent);
