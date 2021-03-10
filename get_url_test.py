import uiautomation as auto
import time

class BrowserWindow:
    def __init__(self, browser_name, window_index=1):
        """
        A Browser Window support UIAutomation.

        :param browser_name: Browser name, support 'Google Chrome', 'Firefox', 'Edge', 'Opera', etc.
        :param window_index: Count from back to front, default value 1 represents the most recently created window.
        """
        if browser_name == 'Firefox':
            addr_bar = auto.Control(Depth=1, ClassName='MozillaWindowClass', foundIndex=window_index) \
                .ToolBarControl(AutomationId='nav-bar').ComboBoxControl(Depth=1, foundIndex=1) \
                .EditControl(Depth=1, foundIndex=1)
        else:
            win = auto.Control(Depth=1, ClassName='Chrome_WidgetWin_1', SubName=browser_name, foundIndex=window_index)
            win_pane = win.PaneControl(Depth=1, Compare=lambda control, _depth: control.Name != '')
            if browser_name == 'Edge':
                addr_pane = win_pane.PaneControl(Depth=1, foundIndex=1).PaneControl(Depth=1, foundIndex=2) \
                    .PaneControl(Depth=1, foundIndex=1).ToolBarControl(Depth=1, foundIndex=1)
            elif browser_name == 'Opera':
                addr_pane = win_pane.GroupControl(Depth=1, foundIndex=1).PaneControl(Depth=1, foundIndex=1) \
                    .PaneControl(Depth=1, foundIndex=2).GroupControl(Depth=1, foundIndex=1) \
                    .GroupControl(Depth=1, foundIndex=1).ToolBarControl(Depth=1, foundIndex=1) \
                    .EditControl(Depth=1, foundIndex=1)
            else:
                addr_pane = win_pane.PaneControl(Depth=1, foundIndex=2).PaneControl(Depth=1, foundIndex=1) \
                    .PaneControl(Depth=1, Compare=lambda control, _depth: control.GetFirstChildControl() and control.GetFirstChildControl().ControlTypeName == 'ButtonControl')
            addr_bar = addr_pane.GroupControl(Depth=1, foundIndex=1).EditControl(Depth=1, foundIndex=1)
        assert addr_bar is not None
        self.addr_bar = addr_bar

    @property
    def current_tab_url(self):
        """Get current tab url."""
        try:
            return self.addr_bar.GetValuePattern().Value
        except Exception as e:
            print(e)

        return None

    @current_tab_url.setter
    def current_tab_url(self, value: str):
        """Set current tab url."""
        self.addr_bar.GetValuePattern().SetValue(value)


browser = BrowserWindow('Chrome')

while True:

    print(browser.current_tab_url)
    # browser.current_tab_url = 'www.google.com'
    # print(browser.current_tab_url)

    time.sleep(1)