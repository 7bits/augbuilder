"""
Hack to add per-session state to Streamlit.

Usage
-----
>>> import SessionState
>>>
>>> session_state = SessionState.get(user_name='', favorite_color='black')
>>> session_state.user_name
''
>>> session_state.user_name = 'Mary'
>>> session_state.favorite_color
'black'
Since you set user_name above, next time your script runs this will be the
result:
>>> session_state = get(user_name='', favorite_color='black')
>>> session_state.user_name
'Mary'
"""

from streamlit import report_thread
from streamlit.server.server import Server


class SessionState(object):
    """Store current session state settings."""

    def __init__(self, **kwargs):
        """
        A new SessionState object.

        Parameters:
            **kwargs : Default values for the session state.

        Example
        -------
        >>> session_state = SessionState(user_name='', favorite_color='black')
        >>> session_state.user_name = 'Mary'
        ''
        >>> session_state.favorite_color
        'black'
        """
        for key, val in kwargs.items():
            setattr(self, key, val)


def get(**kwargs):
    """
    Get a SessionState object for the current session.

    Create a new object if necessary.

    Parameters:
        **kwargs : Default values you want to add to the session state

    Returns:
        this_session._custom_session_state: Current SessionState

    Example
    -------
    >>> session_state = get(user_name='', favorite_color='black')
    >>> session_state.user_name
    ''
    >>> session_state.user_name = 'Mary'
    >>> session_state.favorite_color
    'black'
    Since you set user_name above, next time your script runs this will be the
    result:
    >>> session_state = get(user_name='', favorite_color='black')
    >>> session_state.user_name
    'Mary'
    """
    # Hack to get the session object from Streamlit.

    ctx = report_thread.get_report_ctx()

    this_session = None

    current_server = Server.get_current()

    if hasattr(current_server, '_session_infos'):  # noqa: WPS421
        session_infos = current_server._session_infos.values()
    else:
        current_server = Server.get_current()
        session_info_id = current_server._session_info_by_id
        session_infos = session_info_id.values()

    for session_info in session_infos:
        s = session_info.session
        check = (s._uploaded_file_mgr == ctx.uploaded_file_mgr)
        if (not hasattr(s, '_main_dg') and check):  # noqa: WPS421 
            this_session = s

    if not hasattr(this_session, '_custom_session_state'):  # noqa: WPS421
        new_state = SessionState(**kwargs)
        this_session._custom_session_state = new_state

    return this_session._custom_session_state
