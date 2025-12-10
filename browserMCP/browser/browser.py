from browserMCP.browser.profile import BrowserProfile
from browserMCP.browser.session import BrowserSession

# Alias for backwards compatibility and clarity
BrowserConfig = BrowserProfile
BrowserContextConfig = BrowserProfile
Browser = BrowserSession

__all__ = ['BrowserConfig', 'BrowserContextConfig', 'Browser']
