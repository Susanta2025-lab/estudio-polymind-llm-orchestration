"""Historical local composition; explicit request graphs use graph.composition."""
from graph.composition import create_app_graph
from llm.provider_factory import create_inference_provider
from memory.provider_factory import get_memory_store


inference_provider = create_inference_provider()
memory_store = get_memory_store()
app_graph = create_app_graph(inference_provider, memory_store)
