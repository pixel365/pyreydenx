from . import Client
from .model.task import ActionResult, TaskStatus
from .model.launch_params import LaunchParams


class Action:
    @staticmethod
    def status(client: Client, order_id: int, task_id: str) -> TaskStatus:
        """
        See: https://api.reyden-x.com/docs#/Orders/order_get_task_status_v1_orders__order_id__task__task_id__status__get

        Parameters:
            client (Client): Instance of Client
            order_id (int): Number of order
            task_id (str): Task identifier

        Returns:
            TaskStatus: TaskStatus object
        """
        r = client.get(f"/orders/{order_id}/task/{task_id}/status/")
        return TaskStatus(**r)

    @staticmethod
    def run(client: Client, order_id: int) -> ActionResult:
        """
        See: https://api.reyden-x.com/docs#/Orders/order_run_v1_orders__order_id__action_run__patch

        Parameters:
            client (Client): Instance of Client
            order_id (int): Number of order

        Returns:
            ActionResult: Result object
        """
        r = client.patch(f"/orders/{order_id}/action/run/")
        return ActionResult(**r)

    @staticmethod
    def stop(client: Client, order_id: int) -> ActionResult:
        """
        See: https://api.reyden-x.com/docs#/Orders/order_stop_v1_orders__order_id__action_stop__patch

        Parameters:
            client (Client): Instance of Client
            order_id (int): Number of order

        Returns:
            ActionResult: Result object
        """
        r = client.patch(f"/orders/{order_id}/action/stop/")
        return ActionResult(**r)

    @staticmethod
    def cancel(client: Client, order_id: int) -> ActionResult:
        """
        See: https://api.reyden-x.com/docs#/Orders/order_cancel_v1_orders__order_id__action_cancel__patch

        Parameters:
            client (Client): Instance of Client
            order_id (int): Number of order

        Returns:
            ActionResult: Result object
        """
        r = client.patch(f"/orders/{order_id}/action/cancel/")
        return ActionResult(**r)

    @staticmethod
    def change_online_value(client: Client, order_id: int, value: int) -> ActionResult:
        """
        See: https://api.reyden-x.com/docs#/Orders/order_change_online_v1_orders__order_id__action_change_online__value___patch

        Parameters:
            client (Client): Instance of Client
            order_id (int): Number of order
            value (int): New value

        Returns:
            ActionResult: Result object
        """
        r = client.patch(f"/orders/{order_id}/action/change/online/{value}/")
        return ActionResult(**r)

    @staticmethod
    def change_increase_value(
        client: Client, order_id: int, value: int
    ) -> ActionResult:
        """
        See: https://api.reyden-x.com/docs#/Orders/change_increase_value_v1_orders__order_id__action_increase_change__value___patch

        Parameters:
            client (Client): Instance of Client
            order_id (int): Number of order
            value (int): New value

        Returns:
            ActionResult: Result object
        """
        r = client.patch(f"/orders/{order_id}/action/increase/change/{value}/")
        return ActionResult(**r)

    @staticmethod
    def increase_on(client: Client, order_id: int, value: int) -> ActionResult:
        """
        See: https://api.reyden-x.com/docs#/Orders/increase_on_v1_orders__order_id__action_increase_on__value___patch

        Parameters:
            client (Client): Instance of Client
            order_id (int): Number of order
            value (int): New value

        Returns:
            ActionResult: Result object
        """
        r = client.patch(f"/orders/{order_id}/action/increase/on/{value}/")
        return ActionResult(**r)

    @staticmethod
    def increase_off(client: Client, order_id: int) -> ActionResult:
        """
        See: https://api.reyden-x.com/docs#/Orders/increase_off_v1_orders__order_id__action_increase_off__patch

        Parameters:
            client (Client): Instance of Client
            order_id (int): Number of order

        Returns:
            ActionResult: Result object
        """
        r = client.patch(f"/orders/{order_id}/action/increase/off/")
        return ActionResult(**r)

    @staticmethod
    def add_views(client: Client, order_id: int, value: int) -> ActionResult:
        """
        See: https://api.reyden-x.com/docs#/Orders/add_views_v1_orders__order_id__action_add_views__value___patch

        Parameters:
            client (Client): Instance of Client
            order_id (int): Number of order
            value (int): The number of views to add to the order

        Returns:
            ActionResult: Result object
        """
        r = client.patch(f"/orders/{order_id}/action/add/views/{value}/")
        return ActionResult(**r)

    @staticmethod
    def change_launch_mode(
        client: Client, order_id: int, launch_params: LaunchParams
    ) -> ActionResult:
        """
        See: https://api.reyden-x.com/docs#/Orders/change_launch_params_v1_orders__order_id__action_change_launch__patch

        Parameters:
            client (Client): Instance of Client
            order_id (int): Number of order
            launch_params (LaunchParams): Launch Parameters

        Returns:
            ActionResult: Result object
        """
        r = client.patch(f"/orders/{order_id}/action/change/launch/", launch_params.model_dump())
        return ActionResult(**r)
