import {
    useEffect,
    useState
} from "react";

import {
    useNavigate
} from "react-router-dom";

import api from "../api/api";


function Workflows() {

    const navigate = useNavigate();

    const [workflows, setWorkflows] =
        useState([]);

    const [name, setName] =
        useState("");

    const [description, setDescription] =
        useState("");

    const [message, setMessage] =
        useState("");


    useEffect(() => {

        loadWorkflows();

    }, []);


    const loadWorkflows = async () => {

        try {

            const response =
                await api.get(
                    "/workflows/"
                );

            setWorkflows(
                response.data
            );

        } catch (error) {

            setMessage(
                "Could not load workflows"
            );
        }
    };


    const createWorkflow = async (e) => {

        e.preventDefault();

        setMessage("");


        try {

            await api.post(
                "/workflows/",
                {
                    name: name,
                    description: description
                }
            );


            setName("");

            setDescription("");


            await loadWorkflows();


        } catch (error) {

            setMessage(
                error.response?.data?.detail
                || "Workflow creation failed"
            );
        }
    };


    const deleteWorkflow = async (
        workflowId
    ) => {

        try {

            await api.delete(
                `/workflows/${workflowId}`
            );


            await loadWorkflows();


        } catch (error) {

            setMessage(
                "Could not delete workflow"
            );
        }
    };


    return (

        <div className="content">

            <button
                onClick={
                    () =>
                        navigate(
                            "/dashboard"
                        )
                }
            >
                Dashboard
            </button>


            <h1>
                My Workflows
            </h1>


            <form
                className="workflow-form"
                onSubmit={createWorkflow}
            >

                <h2>
                    Create Workflow
                </h2>


                <input
                    type="text"
                    placeholder="Workflow Name"
                    value={name}
                    onChange={
                        (e) =>
                            setName(
                                e.target.value
                            )
                    }
                    required
                />


                <textarea
                    placeholder="Description"
                    value={description}
                    onChange={
                        (e) =>
                            setDescription(
                                e.target.value
                            )
                    }
                />


                <button type="submit">
                    Create Workflow
                </button>

            </form>


            {message && (

                <p className="error">
                    {message}
                </p>

            )}


            <h2>
                Workflow List
            </h2>


            {
                workflows.length === 0
                ?

                <p>
                    No workflows created yet.
                </p>

                :

                workflows.map(
                    (workflow) => (

                        <div
                            className="workflow-card"
                            key={workflow.id}
                        >

                            <div>

                                <h3>
                                    {workflow.name}
                                </h3>

                                <p>
                                    {
                                        workflow.description
                                        || "No description"
                                    }
                                </p>

                                <span>
                                    Status: {
                                        workflow.status
                                    }
                                </span>

                            </div>


                            <div>

                                <button
                                    onClick={
                                        () =>
                                            navigate(
                                                `/workflows/${workflow.id}`
                                            )
                                    }
                                >
                                    Open
                                </button>


                                <button
                                    onClick={
                                        () =>
                                            deleteWorkflow(
                                                workflow.id
                                            )
                                    }
                                >
                                    Delete
                                </button>

                            </div>

                        </div>

                    )
                )
            }

        </div>
    );
}


export default Workflows;