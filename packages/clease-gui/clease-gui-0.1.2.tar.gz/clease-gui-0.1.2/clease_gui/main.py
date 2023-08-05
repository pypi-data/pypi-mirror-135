from typing import Optional, Dict, Any


def display_ui(dev_mode: bool = False, return_dashboard: bool = False) -> Optional[Dict[str, Any]]:
    """The main CLEASE GUI function.
    Add the following lines in a Jupyter notebook cell use:

    from clease_gui import display_ui
    display_ui()
    """
    from clease_gui.app_data import AppDataKeys
    from clease_gui.main_dashboard import MainDashboard

    app_data = {AppDataKeys.DEV_MODE: dev_mode}
    main_dashboard = MainDashboard(app_data)
    main_dashboard.display()
    if dev_mode or return_dashboard:
        # Return the main dashboard for inspection
        return main_dashboard
    # Returning None ensures we don't print anything at the end of the cell
    # this is the default mode.
    return None
