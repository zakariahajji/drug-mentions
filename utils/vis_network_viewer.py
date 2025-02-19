import json
import streamlit.components.v1 as components

def vis_network_viewer(data: dict, height: int = 800):
    """
    Renders an interactive network graph using vis-network.
    The JSON structure is converted into nodes and edges.
    """
    # Convert the Python dict to a JSON string.
    json_data = json.dumps(data, ensure_ascii=False)
    
    # Build HTML code that loads vis-network from CDN and renders the graph.
    html_code = f"""
    <html>
      <head>
        <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
        <style>
          html, body {{
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
          }}
          #mynetwork {{
            width: 100%;
            height: 100%;
            border: 1px solid lightgray;
          }}
        </style>
      </head>
      <body>
        <div id="mynetwork"></div>
        <script type="text/javascript">
          // Data passed from Python
          const dataFromPython = {json_data};
          let nodes = [];
          let edges = [];
          let nodeSet = new Set();

          // Iterate over drugs in the data
          Object.keys(dataFromPython).forEach(drug => {{
              // Add drug node
              nodes.push({{ id: drug, label: drug, shape: 'box', color: '#66b3ff' }});
              
              // Process PubMed mentions
              (dataFromPython[drug].mentions.pubmed || []).forEach(pub => {{
                  let pubNodeId = drug + "_pub_" + pub.id;
                  if (!nodeSet.has(pubNodeId)) {{
                      nodes.push({{ id: pubNodeId, label: pub.title, shape: 'ellipse', color: '#ccffcc' }});
                      nodeSet.add(pubNodeId);
                  }}
                  edges.push({{ from: drug, to: pubNodeId, label: pub.source || "pubmed" }});
              }});

              // Process Clinical Trials mentions
              (dataFromPython[drug].mentions.clinical_trials || []).forEach(pub => {{
                  let pubNodeId = drug + "_ct_" + pub.id;
                  if (!nodeSet.has(pubNodeId)) {{
                      nodes.push({{ id: pubNodeId, label: pub.title, shape: 'ellipse', color: '#ffcccc' }});
                      nodeSet.add(pubNodeId);
                  }}
                  edges.push({{ from: drug, to: pubNodeId, label: pub.source || "clinical_trial" }});
              }});

              // Process Journals
              (dataFromPython[drug].mentions.journals || []).forEach(journal => {{
                  let journalId = drug + "_journal_" + journal.name.replace(/\\s+/g, "_").toLowerCase();
                  if (!nodeSet.has(journalId)) {{
                      nodes.push({{ id: journalId, label: journal.name, shape: 'diamond', color: '#ffff99' }});
                      nodeSet.add(journalId);
                  }}
                  edges.push({{ from: drug, to: journalId, label: "journal" }});
              }});
          }});

          // Initialize the network
          const container = document.getElementById("mynetwork");
          const visData = {{
              nodes: new vis.DataSet(nodes),
              edges: new vis.DataSet(edges)
          }};
          const options = {{
              layout: {{
                  improvedLayout: true
              }},
              edges: {{
                  arrows: {{
                      to: {{ enabled: true, scaleFactor: 0.5 }}
                  }},
                  font: {{
                      align: "middle"
                  }}
              }},
              physics: {{
                  stabilization: false
              }}
          }};
          new vis.Network(container, visData, options);
        </script>
      </body>
    </html>
    """
    
    components.html(html_code, height=height, scrolling=True)
