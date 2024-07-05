import React, {useEffect, useState} from "react";
import LineChart from "./components/LineChart.jsx";
import LineSample from "./components/LineSample.jsx";


function App() {
    const [loading, setLoading] = useState(true);
    const [lineData, setLineData] = useState({
            data: [
                {date: "2024-01-01", totalUsage: 10, redelivery: 20},
                {date: "2024-01-02", totalUsage: 50, redelivery: 1},
                {date: "2024-01-03", totalUsage: 10, redelivery: 40},
                {date: "2024-01-04", totalUsage: 30, redelivery: 34},
                {date: "2024-01-05", totalUsage: 12, redelivery: 25},
                {date: "2024-01-06", totalUsage: 2, redelivery: 45},
                {date: "2024-01-07", totalUsage: 12, redelivery: 5},
                {date: "2024-01-08", totalUsage: 80, redelivery: 2},
                {date: "2024-01-09", totalUsage: 2, redelivery: 45},
                {date: "2024-01-10", totalUsage: 12, redelivery: 5},
                {date: "2024-01-11", totalUsage: 80, redelivery: 2},
                {date: "2024-02-01", totalUsage: 10, redelivery: 20},
                {date: "2024-02-02", totalUsage: 50, redelivery: 1},
                {date: "2024-02-03", totalUsage: 10, redelivery: 40},
                {date: "2024-02-04", totalUsage: 30, redelivery: 34},
                {date: "2024-02-05", totalUsage: 12, redelivery: 25},
                {date: "2024-02-06", totalUsage: 2, redelivery: 45},
                {date: "2024-02-07", totalUsage: 12, redelivery: 5},
                {date: "2024-02-08", totalUsage: 80, redelivery: 2},
                {date: "2024-02-09", totalUsage: 2, redelivery: 90},
                {date: "2024-02-10", totalUsage: 12, redelivery: 5},
                {date: "2024-02-11", totalUsage: 80, redelivery: 2},
            ]
        }
    );

    useEffect(() => {
        const getData = async () => {
            setLoading(true);
            // TODO: get data from url
            setLoading(false);
        };

        getData();
    }, []);

    if (loading) return <div>Loading...</div>;

    const theData = {
        data: [
            {date: "2024-01-01", totalUsage: 10, redelivery: 21},
            {date: "2024-01-02", totalUsage: 50, redelivery: 22},
            {date: "2024-01-03", totalUsage: 10, redelivery: 23},
            {date: "2024-01-04", totalUsage: 30, redelivery: 24},
            {date: "2024-01-05", totalUsage: 12, redelivery: 25},
        ]
    }

    return (
        <div className="dashboard">
            <div className="wrapper">
                <main className="main">
                    <div className="grid">
                        <div className="card bar-chart-container">
                            <h2>Test</h2>
                            <LineChart height={500} data={lineData.data}/>
                        </div>
                        <div className="card bar-chart-container">
                            <h2>Test2</h2>
                            <LineSample height={500} data={lineData.data}/>
                        </div>
                    </div>
                </main>
            </div>
        </div>
    );
}

export default App;
