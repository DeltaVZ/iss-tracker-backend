from configparser import ConfigParser, NoSectionError, NoOptionError


class ConfigUtils:
    """
    Utils class for config parsing
    """
    __slots__ = ['_config']

    _outbound_requests_section = 'OutboundRequestConfig'
    _inbound_requests_section = 'InboundRequestConfig'
    _fast_api_section = 'FastAPIConfig'
    _user_agent_key = 'User-Agent'
    _wait_time_key = 'wait_time_seconds'
    _iss_position_url_key = 'iss_position_url'
    _iss_router_rate_limit = 'iss_router_rate_limit'
    _limits_enabled = 'limits_enabled'
    _default_positions_time_window_seconds = 'default_positions_time_window_seconds'

    def __init__(self, config_path: str = './challenge/config.ini'):
        self._config = ConfigParser()
        self._config.read(config_path)

    def get_wait_time(self) -> int:
        """
        Provides the wait time between two requests
        :return: the wait_time as int
        """
        try:
            return self._config.getint(section=ConfigUtils._outbound_requests_section, option=ConfigUtils._wait_time_key)
        except (NoSectionError, NoOptionError):
            return 20

    def get_user_agent(self) -> str:
        """
        Provides the user agent to use for requests
        :return: the user agent as string
        """
        try:
            return self._config.get(section=ConfigUtils._outbound_requests_section, option=ConfigUtils._user_agent_key)
        except (NoSectionError, NoOptionError):
            return "Mozilla/5.0"

    def get_iss_position_url(self) -> str:
        """
        Provides the URL to be used for getting the ISS position
        :return: the URL as string
        """
        try:
            return self._config.get(section=ConfigUtils._outbound_requests_section,
                                    option=ConfigUtils._iss_position_url_key)
        except (NoSectionError, NoOptionError):
            return 'https://api.wheretheiss.at/v1/satellites/25544'

    def get_iss_router_rate_limit(self) -> str:
        """
        Provides the rate limit for all endpoints of the iss router
        :return: the rate limit as string
        """
        try:
            return self._config.get(section=ConfigUtils._fast_api_section,
                                    option=ConfigUtils._iss_router_rate_limit)
        except (NoSectionError, NoOptionError):
            return '1/20seconds'

    def get_limits_enabled(self) -> bool:
        """
        Provides the boolean value for limits_enabled
        :return: true or false
        """
        try:
            return self._config.getboolean(section=ConfigUtils._fast_api_section,
                                           option=ConfigUtils._limits_enabled)
        except (NoSectionError, NoOptionError):
            return False
