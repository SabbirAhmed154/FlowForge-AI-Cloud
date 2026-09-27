import {
    useEffect,
    useState
} from "react";

import {
    useNavigate,
    useParams
} from "react-router-dom";

import api from "../api/api";


function RunHistory() {

    const navigate = useNavigate();

    const { workflowId } = useParams();

    const [runs, setRuns] =
        useState([]);

    const [message, setMessage] =
        useState("");


    useEffect(() => {

        loadRuns();

    }, [workflowId]);


    const loadRuns = async () => {

        try {

            const response =
                await api.get(
                    `/workflows/${workflowId}/runs`
                );

            setRuns(
                response.data
            );

        } catch (error) {

            setMessage(
                "Could not load run history"
            );
        }
    };


    return (

        <div className="content">

            <button
                onClick={
                    () =>
                        navigate(
                            `/workflows/${workflowId}`
                        )
                }
            >
                Back to Workflow
            </button>


            <h1>
                Run History
            </h1>


            {message && (

                <p className="error">
                    {message}
                </p>

            )}


            {
                runs.length === 0
                ?

                <p>
                    No workflow runs yet.
                </p>

                :

                runs.map(
                    (run) => (

                        <div
                            className="workflow-card"
                            key={run.id}
                        >

                            <div>

                                <h3>
                                    Run #{run.id}
                                </h3>

                                <p>
                                    Status: {
                                        run.status
                                    }
                                </p>

                                <p>
                                    Input:
                                    {" "}
                                    {run.input_text}
                                </p>

                                {
                                    run.final_output
                                    &&
                                    (
                                        <p>
                                            Final Result:
                                            {" "}
                                            {
                                                run.final_output
                                            }
                                        </p>
                                    )
                                }

                                {
                                    run.error_message
                                    &&
                                    (
                                        <p className="error">
                                            Error:
                                            {" "}
                                            {
                                                run.error_message
                                            }
                                        </p>
                                    )
                                }

                            </div>


                            <button
                                onClick={
                                    () =>
                                        navigate(
                                            `/runs/${run.id}/steps`
                                        )
                                }
                            >
                                View Steps
                            </button>

                        </div>

                    )
                )
            }

        </div>
    );
}


export default RunHistory;