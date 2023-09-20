import React, { useRef, useEffect } from 'react';
import * as d3 from 'd3';

import './EfficientFrontier.css';

function EfficientFrontier({ data, optimal, minVariance }){

    const svgRef = useRef();

    useEffect(() => {

        const svg = d3.select(svgRef.current);
        svg.selectAll("*").remove();

        const width = 800;
        const extraWidth = 150;
        const height = 500;
        const margin = { top: 20, right: 150, bottom: 30, left: 70 };

        const x = d3.scaleLinear()
            .domain([d3.min(data, d => d.risk) - 0.0005, d3.max(data, d => d.risk) + 0.0005])
            .range([margin.left, width - margin.right])

        const y = d3.scaleLinear()
            .domain([d3.min(data, d => d.return) - 0.0005, d3.max(data, d => d.return) + 0.0005])
            .range([height - margin.bottom, margin.top]);

        const xAxis = g => g
            .attr("transform", `translate(0, ${height - margin.bottom})`)
            .call(d3.axisBottom(x).ticks(width / 80).tickFormat(d => `${(d * 100).toFixed(2)}%`));

        const yAxis = g => g
            .attr("transform", `translate(${margin.left}, 0)`)
            .call(d3.axisLeft(y).tickFormat(d => `${(d * 100).toFixed(2)}%`));

        const legendData = [
            {label: "Optimal Portfolio", color: "red"},
            {label: "Min. Variance Portfolio", color: "blue"}
        ];

        const legendWidth = 100;
        const legendMargin = 15;

        const legend = svg.append("g")
            .attr("class", "legend")
            .attr("transform", `translate(${width-legendMargin-30}, ${legendMargin})`);

        const interpolateGreenYellow = d3.interpolate('green', 'yellow');
        const interpolateYellowRed = d3.interpolate('yellow', 'red');

        const minSharpe = d3.min(data, d => d.sharpe_ratio) || 0;
        const maxSharpe = d3.max(data, d => d.sharpe_ratio) || 1;
        const colorScale = d3.scaleSequential(t => {
            return t < 0.5 ? interpolateGreenYellow(t * 2) : interpolateYellowRed((t - 0.5) * 2);
        }).domain([0, 1]);

        const colorScalePlots = d3.scaleSequential(d3.interpolateRdYlGn)
                     .domain([minSharpe, maxSharpe]);

        svg.append("g").call(xAxis);
        svg.append("g").call(yAxis);

        svg.append("text")
            .attr("class", "x label")
            .attr("text-anchor", "middle")
            .attr("x", width/2)
            .attr("y", height + 15)
            .text("Risk");

        svg.append("text")
            .attr("class", "y label")
            .attr("text-anchor", "middle")
            .attr("y", -1)
            .attr("x", -height/2)
            .attr("dy", ".75em")
            .attr("transform", "rotate(-90)")
            .text("Return");

        svg.append("g")
            .selectAll("circle")
            .data(data)
            .enter()
            .append("circle")
            .attr("cx", d => x(d.risk))
            .attr("cy", d => y(d.return))
            .attr("r", 3)
            .attr("fill", d => colorScalePlots(d.sharpe_ratio));

        svg.append("circle")
            .attr("cx", x(optimal.risk))
            .attr("cy", y(optimal.return))
            .attr("r", 5)
            .attr("fill", "red")
            .append("title").text(`Optimal Portfolio: ${optimal.return}, ${optimal.risk}`);

        svg.append("circle")
            .attr("cx", x(minVariance.risk))
            .attr("cy", y(minVariance.return))
            .attr("r", 5)
            .attr("fill", "blue")
            .append("title").text(`Minimum Variance Portfolio: ${minVariance.return}, ${minVariance.risk}`);

        legend.selectAll("rect")
            .data(legendData)
            .enter()
            .append("rect")
            .attr("x", 0)
            .attr("y", (d, i) => i * 20)
            .attr("width", 10)
            .attr("height", 10)
            .attr("fill", d => d.color);

        legend.selectAll("text")
            .data(legendData)
            .enter()
            .append("text")
            .attr("x", 20)
            .attr("y", (d, i) => i * 20 + 9)
            .text(d => d.label);

        const colorBarWidth = 20;
        const colorBarHeight = 150;
        const colorBarX = width + 30
        const colorBarY = margin.top + 60;

        const colorBarTitleX = colorBarX + (colorBarWidth / 2);
        const colorBarTitleY = colorBarY - 10;

        const numberOfStrips = 100;
        const stripHeight = colorBarHeight / numberOfStrips;

        for (let i = 0; i < numberOfStrips; i++){
            svg.append("rect")
                .attr("x", colorBarX)
                .attr("y", colorBarY + i * stripHeight + 15)
                .attr("width", colorBarWidth)
                .attr("height", stripHeight)
                .attr("fill", colorScale(i / numberOfStrips));
        }

        svg.append("text")
            .attr("x", colorBarX - 5)
            .attr("y", colorBarY+15)
            .attr("text-anchor", "end")
            .attr("alignment-baseline", "hanging")
            .text(`${maxSharpe.toFixed(3)}`);

        svg.append("text")
            .attr("x", colorBarX - 5)
            .attr("y", colorBarY + colorBarHeight+15)
            .attr("text-anchor", "end")
            .attr("alignment-baseline", "baseline")
            .text(`${minSharpe.toFixed(3)}`);

        svg.append("text")
            .attr("x", colorBarTitleX-40)
            .attr("y", colorBarTitleY+15)
            .attr("text-anchor", "middle")
            .attr("alignment-baseline", "baseline")
            .style("font-weight", "bold")
            .text("Sharpe Ratio");

    }, [data, optimal, minVariance]);

    return(
        <div class = "efficient-frontier-container">
            <h2>Efficient Frontier</h2>
            <svg ref={svgRef} width="950" height = "525"></svg>
        </div>
    );

}

export default EfficientFrontier;