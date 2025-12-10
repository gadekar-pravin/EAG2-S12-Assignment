import hashlib

from browserMCP.dom.views import DOMElementNode


class ClickableElementProcessor:
	"""Processes clickable elements in a DOM tree, providing hashing and extraction utilities."""

	@staticmethod
	def get_clickable_elements_hashes(dom_element: DOMElementNode) -> set[str]:
		"""Calculates and returns a set of hashes for all clickable elements in the DOM tree.

		Args:
			dom_element (DOMElementNode): The root DOM element to start traversing from.

		Returns:
			set[str]: A set of unique hash strings for clickable elements.
		"""
		clickable_elements = ClickableElementProcessor.get_clickable_elements(dom_element)
		return {ClickableElementProcessor.hash_dom_element(element) for element in clickable_elements}

	@staticmethod
	def get_clickable_elements(dom_element: DOMElementNode) -> list[DOMElementNode]:
		"""Recursively retrieves all clickable elements from the DOM tree.

		Args:
			dom_element (DOMElementNode): The root DOM element to traverse.

		Returns:
			list[DOMElementNode]: A list of DOMElementNodes that are clickable (have a highlight_index).
		"""
		clickable_elements = list()
		for child in dom_element.children:
			if isinstance(child, DOMElementNode):
				if child.highlight_index:
					clickable_elements.append(child)

				clickable_elements.extend(ClickableElementProcessor.get_clickable_elements(child))

		return list(clickable_elements)

	@staticmethod
	def hash_dom_element(dom_element: DOMElementNode) -> str:
		"""Generates a unique hash for a DOM element based on its properties and position.

		Args:
			dom_element (DOMElementNode): The DOM element to hash.

		Returns:
			str: The generated hash string.
		"""
		parent_branch_path = ClickableElementProcessor._get_parent_branch_path(dom_element)
		branch_path_hash = ClickableElementProcessor._parent_branch_path_hash(parent_branch_path)
		attributes_hash = ClickableElementProcessor._attributes_hash(dom_element.attributes)
		xpath_hash = ClickableElementProcessor._xpath_hash(dom_element.xpath)
		# text_hash = DomTreeProcessor._text_hash(dom_element)

		return ClickableElementProcessor._hash_string(f'{branch_path_hash}-{attributes_hash}-{xpath_hash}')

	@staticmethod
	def _get_parent_branch_path(dom_element: DOMElementNode) -> list[str]:
		"""Constructs the path of tag names from the root to the given element.

		Args:
			dom_element (DOMElementNode): The element to trace back.

		Returns:
			list[str]: A list of tag names representing the path.
		"""
		parents: list[DOMElementNode] = []
		current_element: DOMElementNode = dom_element
		while current_element.parent is not None:
			parents.append(current_element)
			current_element = current_element.parent

		parents.reverse()

		return [parent.tag_name for parent in parents]

	@staticmethod
	def _parent_branch_path_hash(parent_branch_path: list[str]) -> str:
		"""Hashes the parent branch path string.

		Args:
			parent_branch_path (list[str]): The list of tag names in the path.

		Returns:
			str: The hash of the path.
		"""
		parent_branch_path_string = '/'.join(parent_branch_path)
		return hashlib.sha256(parent_branch_path_string.encode()).hexdigest()

	@staticmethod
	def _attributes_hash(attributes: dict[str, str]) -> str:
		"""Hashes the element attributes.

		Args:
			attributes (dict[str, str]): Dictionary of attributes.

		Returns:
			str: The hash of the attributes string.
		"""
		attributes_string = ''.join(f'{key}={value}' for key, value in attributes.items())
		return ClickableElementProcessor._hash_string(attributes_string)

	@staticmethod
	def _xpath_hash(xpath: str) -> str:
		"""Hashes the XPath string.

		Args:
			xpath (str): The XPath string.

		Returns:
			str: The hash of the XPath.
		"""
		return ClickableElementProcessor._hash_string(xpath)

	@staticmethod
	def _text_hash(dom_element: DOMElementNode) -> str:
		"""Hashes the text content of the element (currently unused).

		Args:
			dom_element (DOMElementNode): The DOM element.

		Returns:
			str: The hash of the text content.
		"""
		text_string = dom_element.get_all_text_till_next_clickable_element()
		return ClickableElementProcessor._hash_string(text_string)

	@staticmethod
	def _hash_string(string: str) -> str:
		"""Computes the SHA256 hash of a string.

		Args:
			string (str): The input string.

		Returns:
			str: The hexadecimal representation of the hash.
		"""
		return hashlib.sha256(string.encode()).hexdigest()
