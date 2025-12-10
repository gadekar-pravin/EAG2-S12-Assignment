from dataclasses import dataclass, field
from typing import Any

from pydantic import BaseModel

from browserMCP.dom.history_tree_processor.service import DOMHistoryElement
from browserMCP.dom.views import DOMState


# Pydantic
class TabInfo(BaseModel):
	"""Represents information about a browser tab.

	Attributes:
		page_id (int): Unique identifier for the page.
		url (str): The current URL of the tab.
		title (str): The title of the tab.
		parent_page_id (int | None): ID of the parent page if this is a popup or iframe.
	"""

	page_id: int
	url: str
	title: str
	parent_page_id: int | None = None  # parent page that contains this popup or cross-origin iframe


@dataclass
class BrowserStateSummary(DOMState):
	"""The summary of the browser's current state designed for an LLM to process.

	Inherits from DOMState (which provides element_tree and selector_map).

	Attributes:
		url (str): The current URL.
		title (str): The page title.
		tabs (list[TabInfo]): Information about all open tabs.
		screenshot (str | None): Base64 encoded screenshot.
		pixels_above (int): Number of pixels scrolled above the current viewport.
		pixels_below (int): Number of pixels of content below the current viewport.
		browser_errors (list[str]): List of errors encountered.
	"""

	# provided by DOMState:
	# element_tree: DOMElementNode
	# selector_map: SelectorMap

	url: str
	title: str
	tabs: list[TabInfo]
	screenshot: str | None = None
	pixels_above: int = 0
	pixels_below: int = 0
	browser_errors: list[str] = field(default_factory=list)


@dataclass
class BrowserStateHistory:
	"""The summary of the browser's state at a past point in time to use in LLM message history.

	Attributes:
		url (str): The URL at that time.
		title (str): The title at that time.
		tabs (list[TabInfo]): The tabs open at that time.
		interacted_element (list[DOMHistoryElement | None]): Elements interacted with.
		screenshot (str | None): Screenshot at that time.
	"""

	url: str
	title: str
	tabs: list[TabInfo]
	interacted_element: list[DOMHistoryElement | None] | list[None]
	screenshot: str | None = None

	def to_dict(self) -> dict[str, Any]:
		"""Converts the history state to a dictionary.

		Returns:
			dict[str, Any]: Dictionary representation of the state history.
		"""
		data = {}
		data['tabs'] = [tab.model_dump() for tab in self.tabs]
		data['screenshot'] = self.screenshot
		data['interacted_element'] = [el.to_dict() if el else None for el in self.interacted_element]
		data['url'] = self.url
		data['title'] = self.title
		return data


class BrowserError(Exception):
	"""Base class for all browser errors."""


class URLNotAllowedError(BrowserError):
	"""Error raised when a URL is not allowed."""
