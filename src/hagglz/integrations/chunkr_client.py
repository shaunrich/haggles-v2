"""
Chunkr Integration Client

Provides a thin wrapper around chunkr_ai SDK to upload documents (images/PDFs)
and extract OCR text suitable for downstream Hagglz agents.
"""

from __future__ import annotations

import os
import tempfile
from typing import Optional, Iterable

try:
    from chunkr_ai import Chunkr  # type: ignore
except Exception:  # pragma: no cover
    Chunkr = None  # Lazy import guard


class ChunkrClient:
    """Wrapper for Chunkr SDK.

    This client abstracts away temporary file handling and text aggregation from
    returned segments.
    """

    def __init__(self, api_key: Optional[str] = None) -> None:
        self._api_key = api_key or os.getenv("CHUNKR_API_KEY")
        self._client: Optional[Chunkr] = None
        if self._api_key and Chunkr is not None:
            self._client = Chunkr(api_key=self._api_key)

    @property
    def enabled(self) -> bool:
        return self._client is not None

    def close(self) -> None:
        if self._client is not None:
            try:
                self._client.close()
            finally:
                self._client = None

    def extract_text_from_bytes(self, content: bytes, suffix: str = ".pdf") -> str:
        """Upload raw bytes to Chunkr and return concatenated OCR text.

        When given image/PDF bytes, writes to a temporary file to satisfy the
        SDK's file-path based upload and aggregates `segment.text` fields.
        """
        if not self.enabled:
            raise RuntimeError("Chunkr client not initialised. Set CHUNKR_API_KEY and restart.")
        assert self._client is not None

        with tempfile.NamedTemporaryFile(suffix=suffix, delete=True) as tmp:
            tmp.write(content)
            tmp.flush()
            task = self._client.upload(tmp.name)
            return _aggregate_text(getattr(task, "segments", []))

    def extract_text_from_path(self, path: str) -> str:
        if not self.enabled:
            raise RuntimeError("Chunkr client not initialised. Set CHUNKR_API_KEY and restart.")
        assert self._client is not None

        task = self._client.upload(path)
        return _aggregate_text(getattr(task, "segments", []))


def _aggregate_text(segments: Iterable) -> str:
    parts = []
    for s in segments or []:
        # Per latest docs, OCR text is in `segment.text`
        text = getattr(s, "text", None)
        if text:
            parts.append(str(text))
    return "\n\n".join(parts)
