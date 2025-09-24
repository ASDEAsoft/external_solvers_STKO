
# a global singleton to manage parameters
class ParameterManager:
    # define a global counter for unique parameter IDs
    param_counter = 0

    @staticmethod
    def reset():
        ParameterManager.param_counter = 0

    @staticmethod
    def get_new_param_id():
        ParameterManager.param_counter += 1
        return ParameterManager.param_counter