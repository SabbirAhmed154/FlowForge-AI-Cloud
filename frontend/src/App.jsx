import {
    BrowserRouter,
    Routes,
    Route,
    Navigate
} from "react-router-dom";

import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import Workflows from "./pages/Workflows";
import WorkflowDetail from "./pages/WorkflowDetail";
import RunHistory from "./pages/RunHistory";
import StepHistory from "./pages/StepHistory";

import ProtectedRoute from "./components/ProtectedRoute";


function App() {

    return (

        <BrowserRouter>

            <Routes>

                <Route
                    path="/"
                    element={
                        <Navigate
                            to="/login"
                            replace
                        />
                    }
                />

                <Route
                    path="/login"
                    element={<Login />}
                />

                <Route
                    path="/register"
                    element={<Register />}
                />

                <Route
                    path="/dashboard"
                    element={
                        <ProtectedRoute>
                            <Dashboard />
                        </ProtectedRoute>
                    }
                />

                <Route
                    path="/workflows"
                    element={
                        <ProtectedRoute>
                            <Workflows />
                        </ProtectedRoute>
                    }
                />

                <Route
                    path="/workflows/:workflowId"
                    element={
                        <ProtectedRoute>
                            <WorkflowDetail />
                        </ProtectedRoute>
                    }
                />

                <Route
                    path="/workflows/:workflowId/runs"
                    element={
                        <ProtectedRoute>
                            <RunHistory />
                        </ProtectedRoute>
                    }
                />

                <Route
                    path="/runs/:runId/steps"
                    element={
                        <ProtectedRoute>
                            <StepHistory />
                        </ProtectedRoute>
                    }
                />

            </Routes>

        </BrowserRouter>
    );
}


export default App;