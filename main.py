from pathlib import Path

from base_ontology.node import BaseNode
from base_ontology.relation import BaseRelation
from dynamic_kg_extractor.example_ontology.nodes import NODE_DICT
from dynamic_kg_extractor.example_ontology.relations import RELATION_DICT
from dynamic_kg_extractor.models.configurations import LLMOptions, NodeExtractorConfig, RelationExtractorConfig
from dynamic_kg_extractor.models.node_extractor import NodeExtractor
from dynamic_kg_extractor.models.relation_model import RelationExtractor
from dynamic_kg_extractor.visualization import KnowledgeGraphVisualizer
from janus_graph_connector.graph_utils import JanusGraphClient
from janus_graph_connector.utils import save_nodes, save_relations

# 0. Save pydantic object as JSON
node_dict: dict[str, tuple[type[BaseNode], bool, str]] = NODE_DICT
relation_dict: dict[str, type[BaseRelation]] = RELATION_DICT

ontology_name: str = ""
version: str = ""
node_path = Path("path/to/your/node_file.json")
relation_path = Path("path/to/your/relation_file.json")
save_nodes(node_dict, node_path)
save_relations(relation_dict, relation_path)

# 1. Write v0 version by reading JSON files (simulating JSON file reading)
test_client = JanusGraphClient()
test_client.cleanup_graph(ontology_name=ontology_name, version=version)
test_client.write_nodes(json_file_path=node_path, ontology_name=ontology_name, version=version)
test_client.write_relations(json_file_path=relation_path, ontology_name=ontology_name, version=version)
# 2. Finally read the graph
readed_node_dict = test_client.read_nodes(ontology_name=ontology_name, version=version)
readed_relation_dict = test_client.read_relations(ontology_name=ontology_name, version=version, node_dict=readed_node_dict)

# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------
#! 1. Extrac Nodes from pdf with the given READED_NODE_DICT
pdf_file_path = Path("path/to/your/pdf_file.pdf")

node_extractor = NodeExtractor(config=NodeExtractorConfig(file_path=pdf_file_path, node_dict=readed_node_dict, llm_model_name=LLMOptions.OPENAI_O3_MINI))
extracted_nodes = node_extractor.pipeline()

#! 2. Pass the extracted nodes to relation extractor
relation_extractor = RelationExtractor(config=RelationExtractorConfig(relation_dict=readed_relation_dict, llm_model_name=LLMOptions.OPENAI_O3_MINI))
extracted_relations = relation_extractor.pipeline(extracted_nodes=extracted_nodes)

#! 3. Visualize the extracted nodes and relations
vis = KnowledgeGraphVisualizer()
vis.create_visualization(nodes=extracted_nodes, relations=extracted_relations)
