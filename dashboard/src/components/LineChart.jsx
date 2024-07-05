import { useEffect, useRef, useState } from "react";
import * as d3 from "d3";

/*
 * inspired by https://blog.stackademic.com/creating-line-charts-using-d3-js-module-and-react-953b40a82232
 */

function LineChart (...args)  {
    const theData = args[0];
    const [data, setData] = useState(theData.data.map((d)=>d.totalUsage));

    const svgRef= useRef();
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
            .domain([0, data.length - 1])
            .range([0, w]);

        const yScale = d3.scaleLinear().domain([0, h]).range([h, 0]);

        const generateScaledLine = d3
            .line()
            .x((d, i) => xScale(i))
            .y(yScale)
            .curve(d3.curveCardinal);

        const xAxis = d3
            .axisBottom(xScale)
            .ticks(1 + data.length)
            .tickFormat((i) => i + 1);
        const yAxis = d3.axisLeft(yScale).ticks(7);
        svg.append("g").call(xAxis).attr("transform", `translate(0,${h})`);
        svg.append("g").call(yAxis);

        svg
            .selectAll(".line")
            .data([data])
            .join("path")
            .attr("d", (d) => generateScaledLine(d))
            .attr("fill", "none")
            .attr("stroke", "black");
    }, [data]);
    return (
        <div>
            <h2>Line Charts</h2>
            <svg ref={svgRef} style={{ margin: "100px", display: "block" }}></svg>
        </div>
    );
};

export default LineChart;