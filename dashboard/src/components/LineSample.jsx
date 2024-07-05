import { useEffect, useRef, useState } from "react";
import * as d3 from "d3";

function LineChart (...args)  {
    const theData = args[0];
    const [totalUsage, setTotalUsage] = useState(theData.data.map((d)=>d.totalUsage));
    const [redelivery, setRedelivery] = useState(theData.data.map((d)=> d.redelivery));
    const [dates, setDates] = useState(theData.data.map((d)=>d.date));

    const svgRef = useRef();
    useEffect(() => {
        const w = 400;
        const h = 200;
        const svg = d3
            .select(svgRef.current)
            .attr("width", w)
            .attr("height", h)
            .style("overflow", "visible")
            .style("background", "#c5f6fa")

        const xScale = d3
            .scaleLinear()
            .domain([0, totalUsage.length - 1])
            .range([0, w]);

        // domain: the values shown on the scale
        // range: the part of the scale shown on the y-axis. [h,0] uses all of the axis, while [h/2,0] uses the top half of the axis
        const maxY = Math.max(...totalUsage, ...redelivery) + 10;
        console.log({maxY});
        const yScale = d3.scaleLinear()
            .domain([0, h])
            .range([h, 0]);

        const generateScaledLine = d3
            .line()
            .x((d, i) => xScale(i))
            .y(yScale)
            .curve(d3.curveCardinal);

        const xAxis = d3
            .axisBottom(xScale)
            .ticks(1 + Math.min(10,totalUsage.length))
            .tickFormat((i) => dates[i]);

        const yAxis = d3.axisLeft(yScale).ticks(7);
        svg.append("g").call(xAxis).attr("transform", `translate(0,${h})`)
            .selectAll("text").attr("transform", "rotate(-90)");

        svg.append("g").call(yAxis);

        svg
            .selectAll(".line")
            .data([totalUsage])
            .join("path")
            .attr("d", (d) => generateScaledLine(d))
            .attr("fill", "none")
            .attr("stroke", "red");
        svg
            .selectAll(".line")
            .data([redelivery])
            .join("path")
            .attr("d", (d) => generateScaledLine(d))
            .attr("fill", "none")
            .attr("stroke", "blue");
    }, [totalUsage]);

    return (
        <div>
            <h2>Line Charts</h2>
            <svg ref={svgRef} style={{ margin: "100px", display: "block" }}></svg>
        </div>
    );
};

export default LineChart;