import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import api from "../api/api";


function Dashboard() {

    const navigate = useNavigate();

    const [dashboard, setDashboard] = useState(null);

    const [user, setUser] = useState(null);


    useEffect(() => {

        loadData();

    }, []);


    const loadData = async () => {

        try {

            const userResponse =
                await api.get("/auth/me");

            const dashboardResponse =
                await api.get("/dashboard/");


            setUser(
                userResponse.data
            );

            setDashboard(
                dashboardResponse.data
            );

        } catch (error) {

            localStorage.removeItem(
                "access_token"
            );

            navigate("/login");
        }
    };


    const logout = () => {

        localStorage.removeItem(
            "access_token"
        );

        navigate("/login");
    };


    if (!dashboard || !user) {

        return (
            <div className="loading">
                Loading...
            </div>
        );
    }


    return (

        <div className="dashboard">

            <div className="navbar">

                <h2>
                    FlowForge AI
                </h2>


                <div>

                    <span>
                        {user.username}
                    </span>


                    <button
                        onClick={logout}
                    >
                        Logout
                    </button>

                </div>

            </div>


            <div className="content">

                <h1>
                    Dashboard
                </h1>

<button
    onClick={
        () =>
            navigate("/workflows")
    }
>
    My Workflows
</button>
                <div className="stats">

                    <div className="stat-card">

                        <h3>
                            Total Workflows
                        </h3>

                        <strong>
                            {
                                dashboard.total_workflows
                            }
                        </strong>

                    </div>


                    <div className="stat-card">

                        <h3>
                            Total Runs
                        </h3>

                        <strong>
                            {
                                dashboard.total_runs
                            }
                        </strong>

                    </div>


                    <div className="stat-card">

                        <h3>
                            Completed
                        </h3>

                        <strong>
                            {
                                dashboard.completed_runs
                            }
                        </strong>

                    </div>


                    <div className="stat-card">

                        <h3>
                            Failed
                        </h3>

                        <strong>
                            {
                                dashboard.failed_runs
                            }
                        </strong>

                    </div>


                    <div className="stat-card">

                        <h3>
                            Running
                        </h3>

                        <strong>
                            {
                                dashboard.running_runs
                            }
                        </strong>

                    </div>

                </div>


                <h2>
                    Recent Workflows
                </h2>


                {
                    dashboard.recent_workflows.length === 0
                    ?

                    <p>
                        No workflows yet.
                    </p>

                    :

                    dashboard.recent_workflows.map(
                        (workflow) => (

                            <div
                                className="list-card"
                                key={workflow.id}
                            >

                                <strong>
                                    {workflow.name}
                                </strong>

                                <span>
                                    {workflow.status}
                                </span>

                            </div>

                        )
                    )
                }


                <h2>
                    Recent Runs
                </h2>


                {
                    dashboard.recent_runs.length === 0
                    ?

                    <p>
                        No workflow runs yet.
                    </p>

                    :

                    dashboard.recent_runs.map(
                        (run) => (

                            <div
                                className="list-card"
                                key={run.id}
                            >

                                <strong>
                                    {run.workflow_name}
                                </strong>

                                <span>
                                    {run.status}
                                </span>

                            </div>

                        )
                    )
                }

            </div>

        </div>
    );
}


export default Dashboard;