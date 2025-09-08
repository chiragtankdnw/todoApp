import React, { Component } from "react";
import {
	Button,
	Modal,
	ModalHeader,
	ModalBody,
	ModalFooter,
	Form,
	FormGroup,
	Input,
	Label,
	FormFeedback
} from "reactstrap";

export default class CustomModal extends Component {
	constructor(props) {
		super(props);
		this.state = {
			activeItem: this.props.activeItem,
			dateError: ""
		};
	}
	
	handleChange = e => {
		let { name, value } = e.target;
		if (e.target.type === "checkbox") {
			value = e.target.checked;
		}
		const activeItem = { ...this.state.activeItem, [name]: value };
		this.setState({ 
			activeItem,
			dateError: "" // Clear any previous date error when user makes changes
		});
	};
	
	validateDates = () => {
		const { start_date, end_date } = this.state.activeItem;
		if (start_date && end_date && new Date(end_date) < new Date(start_date)) {
			this.setState({ dateError: "End date cannot be before start date." });
			return false;
		}
		return true;
	};
	
	handleSave = () => {
		if (this.validateDates()) {
			this.props.onSave(this.state.activeItem);
		}
	};
	
	render() {
		const { toggle } = this.props;
		const { dateError } = this.state;
		
		return (
			<Modal isOpen={true} toggle={toggle}>
				<ModalHeader toggle={toggle}> Todo Item </ModalHeader>
				<ModalBody>
					<Form>
						<FormGroup>
							<Label for="title">Title</Label>
							<Input
								type="text"
								name="title"
								value={this.state.activeItem.title}
								onChange={this.handleChange}
								placeholder="Enter Todo Title"
							/>
						</FormGroup>
						<FormGroup>
							<Label for="description">Description</Label>
							<Input
								type="text"
								name="description"
								value={this.state.activeItem.description}
								onChange={this.handleChange}
								placeholder="Enter Todo description"
							/>
						</FormGroup>
						<FormGroup>
							<Label for="start_date">Start Date</Label>
							<Input
								type="date"
								name="start_date"
								value={this.state.activeItem.start_date || ""}
								onChange={this.handleChange}
							/>
						</FormGroup>
						<FormGroup>
							<Label for="end_date">End Date</Label>
							<Input
								type="date"
								name="end_date"
								value={this.state.activeItem.end_date || ""}
								onChange={this.handleChange}
								invalid={!!dateError}
							/>
							{dateError && <FormFeedback>{dateError}</FormFeedback>}
						</FormGroup>
						<FormGroup check>
							<Label for="completed">
								<Input
									type="checkbox"
									name="completed"
									checked={this.state.activeItem.completed}
									onChange={this.handleChange}
								/>
								Completed
							</Label>
						</FormGroup>
					</Form>
				</ModalBody>
				<ModalFooter>
					<Button color="success" onClick={this.handleSave}>
						Save
              		</Button>
				</ModalFooter>
			</Modal>
		);
	}
}