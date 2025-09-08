import React, { Component } from "react";
import Modal from "./components/Modal";
import axios from "axios";

axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'
class App extends Component {

	constructor(props) {
		super(props);
		this.state = {
			viewCompleted: false,
			activeItem: {
				title: "",
				description: "",
				completed: false,
				start_date: "",
				end_date: ""
			},
								todoList: [],
				isDarkMode: false
		};
	}

	componentDidMount() {
			this.refreshList();
			// Initialize theme from localStorage or system preference
			const storedTheme = localStorage.getItem('theme');
			let isDark = false;
			if (storedTheme === 'dark') {
				isDark = true;
			} else if (storedTheme === 'light') {
				isDark = false;
			} else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
				isDark = true;
			}
			this.setState({ isDarkMode: isDark }, this.applyTheme);
	}

		applyTheme = () => {
			const { isDarkMode } = this.state;
			document.body.classList.toggle('theme-dark', isDarkMode);
			document.body.classList.toggle('theme-light', !isDarkMode);
			localStorage.setItem('theme', isDarkMode ? 'dark' : 'light');
		};

		toggleTheme = () => {
			this.setState(prev => ({ isDarkMode: !prev.isDarkMode }), this.applyTheme);
		};

	refreshList = () => {
		axios
			// .get("http://localhost:8000/api/todos/")
			// Because of proxy in package.json, command be shorten as follows:
			.get("/api/todos/")
			.then(res => this.setState({ todoList: res.data }))
			.catch(err => console.log(err));
	};

	displayCompleted = status => {
		if (status) {
			return this.setState({ viewCompleted: true });
		}
		return this.setState({ viewCompleted: false });
	};

	renderTabList = () => {
		return (
			<div className="my-5 tab-list">
				<span
					onClick={() => this.displayCompleted(true)}
					className={this.state.viewCompleted ? "active" : ""}
				>
					Complete
            </span>
				<span
					onClick={() => this.displayCompleted(false)}
					className={this.state.viewCompleted ? "" : "active"}
				>
					Incomplete
            </span>
			</div>
		);
	};
	
	formatDate = (dateString) => {
		if (!dateString) return null;
		const date = new Date(dateString);
		return date.toLocaleDateString('en-US', { 
			year: 'numeric', 
			month: 'short', 
			day: 'numeric' 
		});
	};
	
	renderItems = () => {
		const { viewCompleted } = this.state;
		const newItems = this.state.todoList.filter(
			item => item.completed === viewCompleted
		);
		return newItems.map(item => (
			<li
				key={item.id}
				className="list-group-item d-flex justify-content-between align-items-center"
			>
				<div className="todo-content">
					<span
						className={`todo-title mr-2 ${this.state.viewCompleted ? "completed-todo" : ""
							}`}
						title={item.description}
					>
						{item.title}
					</span>
					{(item.start_date || item.end_date) && (
						<div className="todo-dates text-muted small">
							{item.start_date && (
								<span className="start-date">
									Start: {this.formatDate(item.start_date)}
								</span>
							)}
							{item.start_date && item.end_date && " | "}
							{item.end_date && (
								<span className="end-date">
									End: {this.formatDate(item.end_date)}
								</span>
							)}
						</div>
					)}
				</div>
				<span>
					<button
						onClick={() => this.editItem(item)}
						className="btn btn-secondary mr-2"
					>
						Edit
					</button>
					<button
						onClick={() => this.handleDelete(item)}
						className="btn btn-danger"
					>
						Delete
					</button>
				</span>
			</li>
		));
	};

	toggle = () => {
		this.setState({ modal: !this.state.modal });
	};

	handleSubmit = item => {
		this.toggle();
		
		// Convert empty strings to null for date fields to match API expectations
		const processedItem = {
			...item,
			start_date: item.start_date || null,
			end_date: item.end_date || null
		};
		
		if (item.id) {
			axios
				// Because of proxy in package.json, command be shorten as follows:
				// .put(`http://localhost:8000/api/todos/${item.id}/`, item)
				.put(`/api/todos/${item.id}/`, processedItem)
				.then(res => this.refreshList());
			return;
		}
		axios
			// Because of proxy in package.json, command be shorten as follows:
			// .post("http://localhost:8000/api/todos/", item)
			.post("/api/todos/", processedItem)
			.then(res => this.refreshList());
	};

	handleDelete = item => {
		axios
			// Because of proxy in package.json, command be shorten as follows:
			// .delete(`http://localhost:8000/api/todos/${item.id}`)
			.delete(`/api/todos/${item.id}/`)
			.then(res => this.refreshList());
	};

	createItem = () => {
		const item = { title: "", description: "", completed: false, start_date: "", end_date: "" };
		this.setState({ activeItem: item, modal: !this.state.modal });
	};

	editItem = item => {
		// Convert null date values to empty strings for form display
		const editableItem = {
			...item,
			start_date: item.start_date || "",
			end_date: item.end_date || ""
		};
		this.setState({ activeItem: editableItem, modal: !this.state.modal });
	};

	render() {
		return (
			<main className="content">
				<h1 className="text-white text-center my-4">copilot's Todo App</h1>
				<div className="row ">
					<div className="col-md-6 col-sm-10 mx-auto p-0">
						<div className="card p-3">
							<div className="d-flex align-items-center mb-2">
								<button onClick={this.createItem} className="btn btn-primary mr-2">
									Add task
								</button>
								<button
									onClick={this.toggleTheme}
									className="btn btn-outline-secondary"
									aria-label="Toggle dark mode"
								>
									{this.state.isDarkMode ? 'Light Mode' : 'Dark Mode'}
								</button>
							</div>
							{this.renderTabList()}
							<ul className="list-group list-group-flush">
								{this.renderItems()}
							</ul>
						</div>
					</div>
				</div>
				{this.state.modal ? (
					<Modal
						activeItem={this.state.activeItem}
						toggle={this.toggle}
						onSave={this.handleSubmit}
					/>
				) : null}
			</main>
		);
	}
}
export default App;