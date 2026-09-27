import {
    useEffect,
    useState
} from "react";

import {
    useNavigate,
    useParams
} from "react-router-dom";

import api from "../api/api";


function WorkflowDetail() {

    const navigate = useNavigate();

    const { workflowId } = useParams();


    const [workflow, setWorkflow] =
        useState(null);

    const [stepOrder, setStepOrder] =
        useState("");

    const [title, setTitle] =
        useState("");

    const [prompt, setPrompt] =
        useState("");

    const [message, setMessage] =
        useState("");


    // AI Run
    const [inputText, setInputText] =
        useState("");

    const [finalResult, setFinalResult] =
        useState("");

    const [running, setRunning] =
        useState(false);


    useEffect(() => {

        loadWorkflow();

    }, [workflowId]);


    const loadWorkflow = async () => {

        try {

            const response =
                await api.get(
                    `/workflows/${workflowId}`
                );

            setWorkflow(
                response.data
            );

        } catch (error) {

            setMessage(
                "Could not load workflow"
            );
        }
    };


    const addStep = async (e) => {

        e.preventDefault();

        setMessage("");


        try {

            await api.post(
                `/workflows/${workflowId}/steps`,
                {
                    step_order:
                        Number(stepOrder),

                    title: title,

                    prompt: prompt
                }
            );


            setStepOrder("");

            setTitle("");

            setPrompt("");


            await loadWorkflow();


        } catch (error) {

            setMessage(
                error.response?.data?.detail
                || "Could not add step"
            );
        }
    };


    const deleteStep = async (
        stepId
    ) => {

        try {

            await api.delete(
                `/workflows/${workflowId}/steps/${stepId}`
            );


            await loadWorkflow();


        } catch (error) {

            setMessage(
                "Could not delete step"
            );
        }
    };


    const runWorkflow = async (e) => {

        e.preventDefault();

        setMessage("");

        setFinalResult("");

        setRunning(true);


        try {

            const response =
                await api.post(
                    `/workflows/${workflowId}/run`,
                    {
                        input_text: inputText
                    }
                );


            setFinalResult(
                response.data.final_output
            );


            await loadWorkflow();


        } catch (error) {

            setMessage(
                error.response?.data?.detail
                || "Workflow execution failed"
            );

        } finally {

            setRunning(false);
        }
    };


    if (!workflow) {

        return (
            <div className="loading">
                Loading...
            </div>
        );
    }


    return (

        <div className="content">


            <button
                onClick={
                    () =>
                        navigate("/workflows")
                }
            >
                Back to Workflows
                <button
    onClick={
        () =>
            navigate(
                `/workflows/${workflowId}/runs`
            )
    }
>
    View Run History
</button>
            </button>


            <h1>
                {workflow.name}
            </h1>


            <p>
                {
                    workflow.description
                    || "No description"
                }
            </p>


            <p>
                Status: {workflow.status}
            </p>


            <hr />


            <h2>
                Add Workflow Step
            </h2>


            <form
                className="workflow-form"
                onSubmit={addStep}
            >

                <input
                    type="number"
                    min="1"
                    placeholder="Step Order"
                    value={stepOrder}
                    onChange={
                        (e) =>
                            setStepOrder(
                                e.target.value
                            )
                    }
                    required
                />


                <input
                    type="text"
                    placeholder="Step Title"
                    value={title}
                    onChange={
                        (e) =>
                            setTitle(
                                e.target.value
                            )
                    }
                    required
                />


                <textarea
                    placeholder="AI Prompt"
                    value={prompt}
                    onChange={
                        (e) =>
                            setPrompt(
                                e.target.value
                            )
                    }
                    required
                />


                <button type="submit">
                    Add Step
                </button>

            </form>


            <h2>
                Workflow Steps
            </h2>


            {
                workflow.steps.length === 0
                ?

                <p>
                    No steps added yet.
                </p>

                :

                workflow.steps.map(
                    (step) => (

                        <div
                            className="workflow-card"
                            key={step.id}
                        >

                            <div>

                                <h3>
                                    Step {
                                        step.step_order
                                    }: {
                                        step.title
                                    }
                                </h3>

                                <p>
                                    {step.prompt}
                                </p>

                            </div>


                            <button
                                onClick={
                                    () =>
                                        deleteStep(
                                            step.id
                                        )
                                }
                            >
                                Delete Step
                            </button>

                        </div>

                    )
                )
            }


            <hr />


            <h2>
                Run AI Workflow
            </h2>


            <form
                className="workflow-form"
                onSubmit={runWorkflow}
            >

                <textarea
                    placeholder="Enter your starting input..."
                    value={inputText}
                    onChange={
                        (e) =>
                            setInputText(
                                e.target.value
                            )
                    }
                    required
                />


                <button
                    type="submit"
                    disabled={running}
                >

                    {
                        running
                        ? "AI is Running..."
                        : "Run Workflow"
                    }

                </button>

            </form>


            {message && (

                <p className="error">
                    {message}
                </p>

            )}


            {finalResult && (

                <div className="result-card">

                    <h2>
                        Final AI Result
                    </h2>

                    <p>
                        {finalResult}
                    </p>

                </div>

            )}


        </div>
    );
}


export default WorkflowDetail;