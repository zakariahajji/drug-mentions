import json
import streamlit.components.v1 as components

def d3_viewer(data: dict, height: int = 800):
    json_data = json.dumps(data, ensure_ascii=False)
    
    html_code = f"""
    <html>
      <head>
        <script src="https://d3js.org/d3.v7.min.js"></script>
        <style>
          html, body {{
            margin: 0; padding: 0;
            width: 100vw; height: 100vh;
            background-color: #ffffff;
            color: #000000;
            font-family: sans-serif;
            overflow: hidden;
          }}
          #graph {{
            width: 100vw;
            height: 100vh;
          }}
          #legend {{
            position: absolute;
            top: 10px;
            right: 10px;
            background: #fff;
            padding: 10px;
            border: 1px solid #ccc;
            font-size: 12px;
            z-index: 999;
          }}
          .legend-item {{
            display: flex;
            align-items: center;
            margin-bottom: 4px;
          }}
          .legend-color-box {{
            width: 12px;
            height: 12px;
            margin-right: 6px;
            display: inline-block;
          }}
        </style>
      </head>
      <body>
        <!-- Legend -->
        <div id="legend">
          <div class="legend-item">
            <div class="legend-color-box" style="background-color: #1f77b4;"></div>
            Drug
          </div>
          <div class="legend-item">
            <div class="legend-color-box" style="background-color: #ff7f0e;"></div>
            PubMed
          </div>
          <div class="legend-item">
            <div class="legend-color-box" style="background-color: #2ca02c;"></div>
            Clinical Trials
          </div>
          <div class="legend-item">
            <div class="legend-color-box" style="background-color: #d62728;"></div>
            Journal
          </div>
        </div>

        <div id="graph"></div>

        <script>
          // The pipeline data from Python:
          const data = {json_data};

          let nodes = [];
          let links = [];
          let added = new Set();

          function addNode(id, label, group) {{
            if (!added.has(id)) {{
              nodes.push({{ id, label, group }});
              added.add(id);
            }}
          }}

          // Build nodes/links from your JSON
          Object.keys(data).forEach(drug => {{
            addNode(drug, drug, "drug");
            const mentions = data[drug].mentions || {{}};
            // PubMed
            (mentions.pubmed || []).forEach(pub => {{
              let pubId = drug + "_pub_" + (pub.id || Math.random().toString(36).substring(2,7));
              addNode(pubId, pub.title, "pubmed");
              links.push({{ source: drug, target: pubId, label: "pubmed" }});
            }});
            // Clinical Trials
            (mentions.clinical_trials || []).forEach(ct => {{
              let ctId = drug + "_ct_" + (ct.id || Math.random().toString(36).substring(2,7));
              addNode(ctId, ct.title, "clinical");
              links.push({{ source: drug, target: ctId, label: "clinical_trial" }});
            }});
            // Journals
            (mentions.journals || []).forEach(j => {{
              let jid = drug + "_journal_" + j.name.replace(/\\s+/g, "_").toLowerCase();
              addNode(jid, j.name, "journal");
              links.push({{ source: drug, target: jid, label: "journal" }});
            }});
          }});

          // Dimensions
          const width = window.innerWidth;
          const height = window.innerHeight;

          const svg = d3.select("#graph").append("svg")
            .attr("width", width)
            .attr("height", height);

          const simulation = d3.forceSimulation(nodes)
            .force("link", d3.forceLink(links).id(d => d.id).distance(150))
            .force("charge", d3.forceManyBody().strength(-300))
            .force("center", d3.forceCenter(width / 2, height / 2))
            .on("tick", ticked);

          const link = svg.append("g")
            .attr("stroke", "#999")
            .attr("stroke-opacity", 0.6)
            .selectAll("line")
            .data(links)
            .enter().append("line")
            .attr("stroke-width", 1);

          const node = svg.append("g")
            .attr("stroke", "#fff")
            .attr("stroke-width", 1.5)
            .selectAll("circle")
            .data(nodes)
            .enter().append("circle")
            .attr("r", 8)
            .attr("fill", d => {{
              if(d.group === "drug") return "#1f77b4";
              if(d.group === "pubmed") return "#ff7f0e";
              if(d.group === "clinical") return "#2ca02c";
              if(d.group === "journal") return "#d62728";
              return "#ccc";
            }})
            .call(d3.drag()
              .on("start", dragstarted)
              .on("drag", dragged)
              .on("end", dragended));

          const labels = svg.append("g")
            .selectAll("text")
            .data(nodes)
            .enter().append("text")
            .text(d => d.label)
            .attr("font-size", 10)
            .attr("dx", 12)
            .attr("dy", ".35em");

          function ticked() {{
            link
              .attr("x1", d => d.source.x)
              .attr("y1", d => d.source.y)
              .attr("x2", d => d.target.x)
              .attr("y2", d => d.target.y);
            node
              .attr("cx", d => d.x)
              .attr("cy", d => d.y);
            labels
              .attr("x", d => d.x)
              .attr("y", d => d.y);
          }}

          function dragstarted(event, d) {{
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
          }}

          function dragged(event, d) {{
            d.fx = event.x;
            d.fy = event.y;
          }}

          function dragended(event, d) {{
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
          }}
        </script>
      </body>
    </html>
    """
    components.html(html_code, height=height, scrolling=True)
