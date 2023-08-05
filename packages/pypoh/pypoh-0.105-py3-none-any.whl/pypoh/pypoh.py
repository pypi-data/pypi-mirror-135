#!
import requests
import json

_BASE_URL = "https://api.poh.dev"


def _profiles_api(
    amount: int, order_by: str, order_direction: str, include_unregistered: bool, start_cursor: str
) -> dict:
    """
    Internal method. It simply calls the profiles API. It was created to avoid code repetition.

    Args:
        amount: Amount of registered accounts to fetch. Unused.
        order_by: "registered_time" or "creation_time"
        order_direction: "desc" or "asc"
        include_unregistered: True or False
        start_cursor: Internal use only. This is the cursor returned by the precious _profile_api call if there was some

    Returns:
        A dict of with the key "meta" and the key "profiles"

    """
    include_unregistered_str = "true" if include_unregistered else "false"
    start_cursor_str = "&start_cursor={}".format(start_cursor) if start_cursor is not None else ""
    response_dict = json.loads(
        requests.get(
            "{}/profiles?order_by={}&order_direction={}&include_unregistered={}{}".format(
                _BASE_URL, order_by, order_direction, include_unregistered_str, start_cursor_str
            )
        ).text
    )
    return response_dict


def get_raw_list_of_humans(
    amount: int = 100,
    order_by: str = "registered_time",
    order_direction: str = "desc",
    include_unregistered: str = False,
) -> list:
    """
    It returns a list of dicts with each human information.

    Args:
        amount: Amount of registered accounts to fetch.
        order_by: "registered_time" or "creation_time"
        order_direction: "desc" or "asc"
        include_unregistered: True or False

    Returns:
        A list of dicts with each human information.

    """
    ultimate_list = []
    start_cursor = None
    for i in range((amount // 100) + 1):
        response_dict = _profiles_api(amount, order_by, order_direction, include_unregistered, start_cursor)
        start_cursor = response_dict["meta"]["next_cursor"] if response_dict["meta"]["has_more"] else None
        ultimate_list.extend(response_dict["profiles"])

    ultimate_list = ultimate_list[0:amount]
    return ultimate_list


def get_raw_set_of_addresses(
    amount: int = 100,
    order_by: str = "registered_time",
    order_direction: str = "desc",
    include_unregistered: bool = False,
) -> set:
    """
    It returns a set with all the addresses. This might be a bit quicker than calling the get_raw_list_of_humans method.
    The number of returned humans will always be a multiple of 100 for this specific method.
    If you specify an amount of 150, you will get a set of 200 humans instead.

    Args:
        amount: Amount of registered accounts to fetch.
        order_by: "registered_time" or "creation_time"
        order_direction: "desc" or "asc"
        include_unregistered: True or False

    Returns:
        A set with addresses (set of str).

    """

    ultimate_set = set()
    start_cursor = None
    for i in range((amount // 100) + 1):
        response_dict = _profiles_api(amount, order_by, order_direction, include_unregistered, start_cursor)
        start_cursor = response_dict["meta"]["next_cursor"] if response_dict["meta"]["has_more"] else None
        ultimate_set.update([j["eth_address"] for j in response_dict["profiles"]])

    return ultimate_set


def get_list_of_humans(
    amount: int = 100,
    order_by: str = "registered_time",
    order_direction: str = "desc",
    include_unregistered: bool = False,
) -> list:
    """
    It returns a list with objects of class Human(). Warning: This method is slow. I recomment to specify a number of amount < 30.

    Args:
        amount: Amount of registered accounts to fetch.
        order_by: "registered_time" or "creation_time"
        order_direction: "desc" or "asc"
        include_unregistered: True or False

    Returns:
        A list of humans (list of Human())

    """
    return [
        Human(address=i["eth_address"], check_existance=False)
        for i in get_raw_list_of_humans(amount, order_by, order_direction, include_unregistered)
    ]


def ping():
    """
    It checks if there is connection with the Rest API.

    Returns:
        A bool (True if there is ping, False if there is not)

    """
    response = requests.get("{}/ping".format(_BASE_URL))
    return True if "pong" in response.text else False


def is_registered(address: str, verbose: bool = False) -> bool:
    """
    It returns True if the given address is registered. It returns False if it is not registered.

    Args:
        address: The address which registration you want to check.
        verbose: True if you want to get the error prints, False if you don't.

    Returns:
        A bool. True if the given address is registered, False if it is not registered.

    """
    response_dict = json.loads(requests.get("{}/profiles/{}".format(_BASE_URL, address)).text)
    if "error" in response_dict:
        if verbose:
            print("Error: {}".format(response_dict["error"]))
        return False
    else:
        return response_dict["registered"]


def get_human_status_history(address: str) -> list:
    """
    It returns a list of dicts with this human history.

    Args:
        address: The address of the human which history you want to check.

    Returns:
        A list of dicts with this human history.

    """
    return json.loads(requests.get("{}/profiles/{}/status-history".format(_BASE_URL, address)).text)


def get_human_given_vouches(address: str) -> list:
    """
    It returns a list of dicts with this human given vouches.

    Args:
        address: The address of the human which given vouches you want to check.

    Returns:
        A list of dicts with this human given vouches.

    """
    return json.loads(requests.get("{}/profiles/{}/vouches".format(_BASE_URL, address)).text)["given"]


def get_human_received_vouches(address: str) -> list:
    """
    It returns a list of dicts with this human received vouches.

    Args:
        address: The address of the human which received vouches you want to check.

    Returns:
        A list of dicts with this human received vouches.

    """
    return json.loads(requests.get("{}/profiles/{}/vouches".format(_BASE_URL, address)).text)["received"]


def create_human(address: str, verbose: bool = False):
    """
    It returns an instanciated object of class Human() based on the given address.

    Args:
        address: The address which registration you want to check.
        verbose: Bool to specify if you want to see all the prints.

    Returns:
        An object of class Human() or None if there was error preventing the instanciation.

    """
    if "error" in json.loads(requests.get("{}/profiles/{}".format(_BASE_URL, address)).text):
        if verbose:
            print("This address is not registered.")
        return None
    else:
        return Human(address=address, check_existance=False)


class Human:
    def __init__(self, address: str, check_existance: bool = True, verbose: bool = False):
        """
        Initializes the Human.

        Args:
            address: The address of the human to instanciate.
            check_existance: Bool to specify if you want to check if this address is registered before intanciating the object.
            verbose: Bool to specify if you want to see all the prints.

        """
        response_dict = json.loads(requests.get("{}/profiles/{}".format(_BASE_URL, address)).text)
        self.address = address
        if check_existance:
            if "error" in response_dict:
                if verbose:
                    print("Error with address {}".format(self.address))
                    print(response_dict["error"])
                    print("Creating a mocking class")
                self.registered = False
            else:
                self.status = response_dict["status"]
                self.vanity_id = ""
                self.display_name = response_dict["display_name"]
                self.first_name = response_dict["first_name"]
                self.last_name = response_dict["last_name"]
                self.registered = response_dict["registered"]
                self.photo = response_dict["photo"]
                self.video = response_dict["video"]
                self.bio = response_dict["bio"]
                self.profile = response_dict["profile"]
                self.registered_time = response_dict["registered_time"]
                self.creation_time = response_dict["creation_time"]
        else:
            self.status = response_dict["status"]
            self.status = response_dict["status"]
            self.vanity_id = ""
            self.display_name = response_dict["display_name"]
            self.first_name = response_dict["first_name"]
            self.last_name = response_dict["last_name"]
            self.registered = response_dict["registered"]
            self.photo = response_dict["photo"]
            self.video = response_dict["video"]
            self.bio = response_dict["bio"]
            self.profile = response_dict["profile"]
            self.registered_time = response_dict["registered_time"]
            self.creation_time = response_dict["creation_time"]

    def is_registered(self) -> bool:
        """
        It returns True if this human is registered. It returns False if it is not registered.
        """
        return self.registered

    def get_status_history(self) -> list:
        """
        It returns a list of dicts with this human history.

        Returns:
            A list of dicts with this human history.

        """
        return json.loads(requests.get("{}/profiles/{}/status-history".format(_BASE_URL, self.address)).text)

    def get_given_vouches(self) -> list:
        """
        It returns a list of dicts with this human given vouches.

        Returns:
            A list of dicts with this human given vouches.

        """
        return json.loads(requests.get("{}/profiles/{}/vouches".format(_BASE_URL, self.address)).text)["given"]

    def get_received_vouches(self) -> list:
        """
        It returns a list of dicts with this human received vouches.

        Returns:
            A list of dicts with this human received vouches.

        """
        return json.loads(requests.get("{}/profiles/{}/vouches".format(_BASE_URL, self.address)).text)["received"]

    def todict(self) -> dict:
        """
        It returns a dict with all the data of this human.

        Returns:
            A dict with all this human data.

        """
        if self.is_registered:
            return {
                "is_registered": True,
                "status": self.status,
                "display_name": self.display_name,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "registered": self.registered,
                "photo": self.photo,
                "video": self.video,
                "bio": self.bio,
                "bio": self.profile,
                "registered_time": self.registered_time,
                "creation_time": self.creation_time,
            }
        else:
            return {
                "is_registered": False,
            }
