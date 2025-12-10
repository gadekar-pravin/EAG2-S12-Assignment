from pydantic import BaseModel, ConfigDict, Field, model_validator

# Action Input Models
class SearchGoogleAction(BaseModel):
	"""Input model for searching Google."""
	query: str

class GoToUrlAction(BaseModel):
	"""Input model for navigating to a URL."""
	url: str

class ClickElementAction(BaseModel):
	"""Input model for clicking an element by index."""
	index: int
	xpath: str | None = None

class InputTextAction(BaseModel):
	"""Input model for entering text into an element."""
	index: int
	text: str
	xpath: str | None = None

class DoneAction(BaseModel):
	"""Input model for completing a task."""
	text: str
	success: bool

class SwitchTabAction(BaseModel):
	"""Input model for switching tabs."""
	page_id: int

class OpenTabAction(BaseModel):
	"""Input model for opening a new tab."""
	url: str

class CloseTabAction(BaseModel):
	"""Input model for closing a tab."""
	page_id: int

class ScrollAction(BaseModel):
	"""Input model for scrolling the page."""
	amount: int | None = None  # The number of pixels to scroll. If None, scroll down/up one page

class SendKeysAction(BaseModel):
	"""Input model for sending keyboard keys."""
	keys: str

class ExtractPageContentAction(BaseModel):
	"""Input model for extracting page content."""
	value: str

class NoParamsAction(BaseModel):
	"""
	Accepts absolutely anything in the incoming data
	and discards it, so the final parsed model is empty.
	"""

	model_config = ConfigDict(extra='allow')

	@model_validator(mode='before')
	def ignore_all_inputs(cls, values):
		# No matter what the user sends, discard it and return empty.
		return {}

class Position(BaseModel):
	"""Model representing an (x, y) coordinate position."""
	x: int
	y: int

class DragDropAction(BaseModel):
	"""Input model for drag and drop operations."""
	# Element-based approach
	element_source: str | None = Field(None, description='CSS selector or XPath of the element to drag from')
	element_target: str | None = Field(None, description='CSS selector or XPath of the element to drop onto')
	element_source_offset: Position | None = Field(
		None, description='Precise position within the source element to start drag (in pixels from top-left corner)'
	)
	element_target_offset: Position | None = Field(
		None, description='Precise position within the target element to drop (in pixels from top-left corner)'
	)

	# Coordinate-based approach (used if selectors not provided)
	coord_source_x: int | None = Field(None, description='Absolute X coordinate on page to start drag from (in pixels)')
	coord_source_y: int | None = Field(None, description='Absolute Y coordinate on page to start drag from (in pixels)')
	coord_target_x: int | None = Field(None, description='Absolute X coordinate on page to drop at (in pixels)')
	coord_target_y: int | None = Field(None, description='Absolute Y coordinate on page to drop at (in pixels)')

	# Common options
	steps: int | None = Field(10, description='Number of intermediate points for smoother movement (5-20 recommended)')
	delay_ms: int | None = Field(5, description='Delay in milliseconds between steps (0 for fastest, 10-20 for more natural)')

# Additional action models for MCP server
class WaitAction(BaseModel):
	"""Input model for waiting a specified duration."""
	seconds: int = 3

class ExtractContentAction(BaseModel):
	"""Input model for extracting specific content from a page."""
	goal: str
	should_strip_link_urls: bool = True

class GetAxTreeAction(BaseModel):
	"""Input model for retrieving the accessibility tree."""
	number_of_elements: int = 50

class ScrollToTextAction(BaseModel):
	"""Input model for scrolling to specific text."""
	text: str

class GetDropdownOptionsAction(BaseModel):
	"""Input model for getting dropdown options."""
	index: int

class SelectDropdownOptionAction(BaseModel):
	"""Input model for selecting a dropdown option."""
	index: int
	text: str

class GoogleSheetsRangeAction(BaseModel):
	"""Input model for Google Sheets range operations."""
	cell_or_range: str

class GoogleSheetsTextAction(BaseModel):
	"""Input model for Google Sheets text input."""
	text: str

class GoogleSheetsUpdateAction(BaseModel):
	"""Input model for updating Google Sheets content."""
	range: str
	new_contents_tsv: str
