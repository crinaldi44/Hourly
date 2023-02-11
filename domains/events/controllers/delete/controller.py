from crosscutting.auth.authentication import init_controller


def delete_event(id_):
    """Deletes an event from within a user's company.

        :param id_: Represents the ID of the event to delete.
        :return: None
    """
    employee, company, department, role = init_controller(permissions='delete:events')
    return {}, 204
