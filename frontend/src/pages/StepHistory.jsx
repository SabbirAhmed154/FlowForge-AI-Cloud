import {
    useEffect,
    useState
} from "react";

import {
    useNavigate,
    useParams
} from "react-router-dom";

import api from "../api/api";


function StepHistory() {

    const navigate = useNavigate();

    const { runId } = useParams();

    const [steps, setSteps] =
        useState([]);

    const [message, setMessage] =
        useState("");


    useEffect(() => {

        loadSteps();

    }, [runId]);


    const loadSteps = async () => {

        try {

            const response =
                await api.get(
                    `/workflows/runs/${runId}/steps`
                );

            setSteps(
                response.data
            );

        } catch (error) {

            setMessage(
                "Could not load step history"
            );
        }
    };


    return (

        <div className="content">

            <button
                onClick={
                    () =>
                        navigate(-1)
                }
            >
                Back
            </button>


            <h1>
                Step History
            </h1>


            {message && (

                <p className="error">
                    {message}
                </p>

            )}


            {
                steps.length === 0
                ?

                <p>
                    No step history found.
                </p>

                :

                steps.map(
                    (step) => (

                        <div
                            className="result-card"
                            key={step.id}
                        >

                            <h2>
                                Step {
                                    step.step_order
                                }: {
                                    step.step_title
                                }
                            </h2>


                            <p>
                                <strong>
                                    Status:
                                </strong>

                                {" "}

                                {step.status}
                            </p>


                            <h3>
                                Input
                            </h3>

                            <p>
                                {
                                    step.input_text
                                    || "No input"
                                }
                            </p>


                            <h3>
                                Output
                            </h3>

                            <p>
                                {
                                    step.output_text
                                    || "No output"
                                }
                            </p>

                        </div>

                    )
                )
            }

        </div>
    );
}


export default StepHistory;