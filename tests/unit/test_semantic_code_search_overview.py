"""Regression tests for semantic search ranking in overview/config modes."""

from analyzers.semantic_code_search import SemanticCodeSearch, CodeChunk


class _DummyOrchestrator:
    def generate_completion(self, prompt, max_tokens=150):
        return ""


class _RerankOrchestrator:
    def generate_completion(self, prompt, max_tokens=320, temperature=0.0):
        if "User question" not in prompt:
            return ""
        # Prefer candidate 2 over candidate 1.
        return "\n".join([
            "2|95|Direct checkout implementation details",
            "1|25|Only UI wrapper text",
        ])


def _chunk(file_path: str, content: str) -> CodeChunk:
    return CodeChunk(
        file_path=file_path,
        content=content,
        start_line=1,
        end_line=max(1, len(content.splitlines())),
        language="javascript",
        chunk_type="block",
        name=file_path,
    )


def test_overview_query_prioritizes_feature_files_over_config_noise():
    engine = SemanticCodeSearch(_DummyOrchestrator())
    engine.code_chunks = [
        _chunk(
            "vite.config.js",
            "import { defineConfig } from 'vite'; export default defineConfig({ plugins: [] });",
        ),
        _chunk(
            "src/router.jsx",
            "import { createBrowserRouter } from 'react-router-dom'; const router = createBrowserRouter([{ path: '/' }]);",
        ),
        _chunk(
            "src/components/Shimmer.jsx",
            "export const Shimmer = () => <div className='skeleton shimmer'>Loading...</div>;",
        ),
        _chunk(
            "src/pages/Home.jsx",
            "export default function Home() { return <main>Home</main>; }",
        ),
    ]

    results = engine.search_by_intent("what are the key features in this codebase?", top_k=3)
    files = [item.file_path.lower() for item in results]

    assert files
    assert "src/router.jsx" in files
    assert "src/components/shimmer.jsx" in files
    assert "vite.config.js" not in files


def test_config_query_can_return_config_files():
    engine = SemanticCodeSearch(_DummyOrchestrator())
    engine.code_chunks = [
        _chunk(
            "vite.config.js",
            "import { defineConfig } from 'vite'; export default defineConfig({ plugins: [] });",
        ),
        _chunk(
            "src/router.jsx",
            "import { createBrowserRouter } from 'react-router-dom'; const router = createBrowserRouter([{ path: '/' }]);",
        ),
    ]

    results = engine.search_by_intent("explain the vite config and build setup", top_k=2)
    files = [item.file_path.lower() for item in results]

    assert files
    assert files[0] == "vite.config.js"


def test_location_query_prefers_files_that_define_target_behavior():
    engine = SemanticCodeSearch(_DummyOrchestrator())
    engine.code_chunks = [
        _chunk(
            "src/components/Header.jsx",
            "export default function Header() { return <header>Hi</header>; }",
        ),
        _chunk(
            "src/router.jsx",
            "import { createBrowserRouter } from 'react-router-dom'; const router = createBrowserRouter([{ path: '/' }]);",
        ),
    ]

    results = engine.search_by_intent("which file routing is implemented in?", top_k=1)
    assert results
    assert results[0].file_path.lower() == "src/router.jsx"


def test_debug_query_prefers_error_handling_chunks():
    engine = SemanticCodeSearch(_DummyOrchestrator())
    engine.code_chunks = [
        _chunk(
            "src/components/Cart.jsx",
            "export default function Cart() { return <div>Cart</div>; }",
        ),
        _chunk(
            "src/utils/errorHandler.js",
            "export function handleError(err) { try { throw err; } catch (e) { return e.message; } }",
        ),
    ]

    results = engine.search_by_intent("app is not working, debug this exception and bug", top_k=1)
    assert results
    assert results[0].file_path.lower() == "src/utils/errorhandler.js"


def test_specific_query_requires_anchor_match_and_avoids_noise_fallback():
    engine = SemanticCodeSearch(_DummyOrchestrator())
    engine.code_chunks = [
        _chunk(
            "src/router.jsx",
            "import { createBrowserRouter } from 'react-router-dom'; const router = createBrowserRouter([{ path: '/' }]);",
        ),
        _chunk(
            "src/components/Header.jsx",
            "export default function Header() { return <header>Hi</header>; }",
        ),
    ]

    results = engine.search_by_intent("where is payment gateway implemented?", top_k=3)
    assert results == []


def test_specific_entity_query_prioritizes_entity_matching_chunks():
    engine = SemanticCodeSearch(_DummyOrchestrator())
    engine.code_chunks = [
        _chunk(
            "src/components/Shimmer.jsx",
            "export default function Shimmer() { return <div className='shimmer'>Loading</div>; }",
        ),
        _chunk(
            "src/router.jsx",
            "import { createBrowserRouter } from 'react-router-dom'; const router = createBrowserRouter([{ path: '/' }]);",
        ),
        _chunk(
            "src/pages/Home.jsx",
            "export default function Home() { return <main>Home</main>; }",
        ),
    ]

    results = engine.search_by_intent("what is shimmer in this repo and why we use that", top_k=2)
    files = [item.file_path.lower() for item in results]

    assert files
    assert files[0] == "src/components/shimmer.jsx"
    assert "src/router.jsx" not in files


def test_llm_reranker_can_reorder_close_candidates_for_direct_answer():
    engine = SemanticCodeSearch(_RerankOrchestrator())
    engine.code_chunks = [
        _chunk(
            "src/components/CheckoutBanner.jsx",
            "export default function CheckoutBanner() { return <div>Checkout now</div>; }",
        ),
        _chunk(
            "src/pages/Checkout.jsx",
            "export default function Checkout() { const checkout = true; return <main>Checkout flow</main>; }",
        ),
    ]

    results = engine.search_by_intent("where is checkout implemented?", top_k=2)
    files = [item.file_path.lower() for item in results]

    assert files
    assert files[0] == "src/pages/checkout.jsx"
