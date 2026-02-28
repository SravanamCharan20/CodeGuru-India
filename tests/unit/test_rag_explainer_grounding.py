"""Regression tests for grounded RAG explanations."""

import re
from types import SimpleNamespace

from analyzers.rag_explainer import RAGExplainer
from analyzers.semantic_code_search import CodeChunk


class _DummyOrchestrator:
    def generate_completion(self, prompt, max_tokens=300):
        # Intentionally hallucinates BrowserRouter style code.
        return (
            "This repo uses BrowserRouter.\n\n"
            "```javascript\n"
            "import { BrowserRouter } from 'react-router-dom';\n"
            "function App() { return <BrowserRouter /> }\n"
            "```\n"
            "Routing is configured in router file."
        )


class _CountingOrchestrator:
    def __init__(self):
        self.calls = 0

    def generate_completion(self, prompt, max_tokens=300):
        self.calls += 1
        return "This should not be used for deterministic feature overview."


def test_rag_explainer_strips_synthetic_code_and_keeps_grounded_evidence():
    explainer = RAGExplainer(_DummyOrchestrator(), web_search_available=False)
    repo_context = SimpleNamespace(
        repo_url="local-repo",
        languages={"javascript": 10},
    )
    chunks = [
        CodeChunk(
            file_path="frontend/src/router.js",
            start_line=1,
            end_line=24,
            language="javascript",
            chunk_type="block",
            name="router",
            content=(
                "import { createBrowserRouter } from 'react-router-dom';\n"
                "const router = createBrowserRouter([\n"
                "  { path: '/', element: <Home/> },\n"
                "  { path: '/restaurant/:resId', element: <RestaurantMenu/> }\n"
                "]);\n"
                "export default router;\n"
            ),
        )
    ]

    result = explainer.generate_detailed_explanation(
        intent="which routing system used for the routing in this codebase and explain about that",
        relevant_chunks=chunks,
        repo_context=repo_context,
        use_web_search=False,
        output_language="english",
    )

    text = result["explanation"]
    assert re.search(r"\bBrowserRouter\b", text) is None
    assert "createBrowserRouter" in text
    assert "Evidence From Repository" in text
    assert "frontend/src/router.js" in text


def test_feature_overview_query_is_deterministic_and_filters_config_noise():
    orchestrator = _CountingOrchestrator()
    explainer = RAGExplainer(orchestrator, web_search_available=False)
    repo_context = SimpleNamespace(
        repo_url="local-repo",
        languages={"javascript": 10},
    )
    chunks = [
        CodeChunk(
            file_path="frontend/src/router.js",
            start_line=1,
            end_line=35,
            language="javascript",
            chunk_type="block",
            name="router",
            content=(
                "import { createBrowserRouter } from 'react-router-dom';\n"
                "const router = createBrowserRouter([{ path: '/', element: <Home/> }]);\n"
                "export default router;\n"
            ),
        ),
        CodeChunk(
            file_path="frontend/src/components/Shimmer.jsx",
            start_line=1,
            end_line=24,
            language="javascript",
            chunk_type="block",
            name="shimmer",
            content=(
                "export default function Shimmer() {\n"
                "  return <div className='skeleton shimmer'>Loading...</div>;\n"
                "}\n"
            ),
        ),
        CodeChunk(
            file_path="vite.config.js",
            start_line=1,
            end_line=20,
            language="javascript",
            chunk_type="block",
            name="vite",
            content=(
                "import { defineConfig } from 'vite';\n"
                "export default defineConfig({ plugins: [] });\n"
            ),
        ),
    ]

    result = explainer.generate_detailed_explanation(
        intent="what are the key features in this codebase?",
        relevant_chunks=chunks,
        repo_context=repo_context,
        use_web_search=False,
        output_language="english",
    )

    text = result["explanation"].lower()
    refs = [item["file"].lower() for item in result["code_references"]]

    assert "key features in this codebase" in text
    assert "routing and navigation" in text
    assert "loading experience" in text or "shimmer" in text
    assert "vite.config.js" not in text
    assert all("vite.config.js" not in ref for ref in refs)
    assert orchestrator.calls == 0


def test_generic_unsupported_code_entities_are_filtered_from_answer():
    class _HallucinatingOrchestrator:
        def generate_completion(self, prompt, max_tokens=300):
            return (
                "The code uses `createBrowserRouter` from `frontend/src/router.js`.\n"
                "It also has `MagicRouterEngine` in `src/magic_router.ts`."
            )

    explainer = RAGExplainer(_HallucinatingOrchestrator(), web_search_available=False)
    repo_context = SimpleNamespace(
        repo_url="local-repo",
        languages={"javascript": 10},
    )
    chunks = [
        CodeChunk(
            file_path="frontend/src/router.js",
            start_line=1,
            end_line=20,
            language="javascript",
            chunk_type="block",
            name="router",
            content=(
                "import { createBrowserRouter } from 'react-router-dom';\n"
                "const router = createBrowserRouter([{ path: '/', element: <Home/> }]);\n"
                "export default router;\n"
            ),
        )
    ]

    result = explainer.generate_detailed_explanation(
        intent="which routing system is used",
        relevant_chunks=chunks,
        repo_context=repo_context,
        use_web_search=False,
        output_language="english",
    )

    text = result["explanation"]
    assert "createBrowserRouter" in text
    assert "frontend/src/router.js" in text
    assert "MagicRouterEngine" not in text
    assert "src/magic_router.ts" not in text
