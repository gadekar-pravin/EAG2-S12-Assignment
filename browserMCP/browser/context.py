from browserMCP.browser.profile import BrowserProfile
from browserMCP.browser.session import BrowserSession

# Aliases for browser components to maintain consistent naming conventions
Browser = BrowserSession
BrowserConfig = BrowserProfile
BrowserContext = BrowserSession
BrowserContextConfig = BrowserProfile

__all__ = ['Browser', 'BrowserConfig', 'BrowserContext', 'BrowserContextConfig']
