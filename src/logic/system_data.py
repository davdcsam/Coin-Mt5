from os import getcwd
from uuid import uuid4
from json import load, dump


class InternalData:
    """
    Singleton class for managing internal data.

    Attributes:
        _instance (InternalData): The singleton instance of the class.
    """

    _instance = None

    class AutoDict(dict):
        """
        Dictionary subclass that returns a default value for missing keys.
        """

        def __missing__(self, key):
            return self.setdefault(key, None)

    def __new__(
        cls,
        files: str = [
            "UUID_tag_window.json",
            "UUID_tag_button.json",
            "UUID_tag_item.json",
            "UUID_tag_input.json",
            "UUID_tag_not_classified.json",
        ],
        unit_files_restore: str = "UUID_unit.json"
    ):
        # Check if an instance of the class already exists
        if cls._instance is None:
            # If not, create a new instance
            cls._instance = super(InternalData, cls).__new__(cls)
            # Load all the files to get data
            for file in files:
                try:
                    # Try to open and load the JSON file
                    with open(f"{getcwd()}/.data/{file}", "r+") as f:
                        json_data = load(f)
                except FileNotFoundError:
                    """
                    If the file is not found, try to
                    load the unit_files_restore restore file
                    """
                    print(f"File {file} not found.")
                    try:
                        with open(f"{getcwd()}/.data/{unit_files_restore}", "r+") as f:
                            json_data = load(f)[file]
                    except Exception as e:
                        print(f"An error occurred: {str(e)}")
                        continue
                except Exception as e:
                    print(f"An error occurred: {str(e)}")
                    continue

                # Add the loaded data to the class instance
                cls._instance.__dict__[file] = {}
                for element in json_data:
                    cls._instance.__dict__[file][element] = cls._instance.AutoDict(
                        label=json_data[element]["label"], tag=str(uuid4())
                    )
        # Return the class instance
        return cls._instance

    def __getattr__(self, name, file=None, **kwargs):
        """
        Retrieves an attribute value, creating it if it doesn't exist.

        Args:
            name (str): The name of the attribute.
            file (str, optional): The file where the attribute is stored.
            **kwargs: Additional keyword arguments.
        """
        # If a specific file is provided, look for the attribute in that file
        if file:
            # If the attribute does not exist in the file, create it
            if name not in self.__dict__[file]:
                self.__dict__[file][name] = self.AutoDict(
                    label=name.replace("_", " ").title(), tag=str(uuid4())
                )
            # Return the attribute from the specified file
            return self.__dict__[file][name]
        else:
            """
            If the file is not found, try to
            load the unit_files_restore restore file
            """
            for file in self.__dict__:
                if name in self.__dict__["UUID_tag_not_classified.json"]:
                    return self.__dict__["UUID_tag_not_classified.json"][name]
            # If the attribute does not exist in any file, create it
            self.__dict__[name] = self.AutoDict(
                label=name.replace("_", " ").title(), tag=str(uuid4())
            )
            # Return the newly created attribute
            return self.__dict__[name]

    def restore_files(self, unit_files_restore, json_data, file):
        # Try to open and load the restore file
        try:
            with open(f"{getcwd()}/.data/{unit_files_restore}", "r+") as f:
                return load(f)[file]
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def get_all(self):
        """
        Retrieves all attributes.

        Returns:
            dict: Dictionary of all attributes.
        """
        result = {}
        # Iterate over all files and add their attributes to the result
        for file in self.__dict__:
            result.update(self.__dict__[file])
        return result

    def get_all_internal(self):
        """
        Retrieves all internal attributes.

        Returns:
            dict: Dictionary of all internal attributes.
        """
        # Return all internal attributes
        return self.__dict__

    def save_to_json_files(self, path_dir: str = getcwd()):
        """
        Saves all attributes to JSON files.

        Args:
            path_dir (str): The directory where the files should be saved.
        """
        # Get all attributes that start with "UUID"
        all_atributes = {
            key: value
            for key, value in self.get_all_internal().items()
            if key.startswith("UUID")
        }

        # Iterate over all attributes and save them to JSON files
        for file, content in all_atributes.items():
            try:
                with open(f"{path_dir}/.data/{file}", "w") as f:
                    dump(content, f, indent=4)
            except FileNotFoundError:
                print(f"Directory {path_dir}/.data/ not found.")
            except Exception as e:
                print(f"An error occurred: {str(e)}")

    def save_to_unit_json_file(
        self, name: str = "UUID_unit", path_dir: str = getcwd()
    ):
        """
        Saves all attributes to a single JSON file.

        Args:
            name (str): The name of the JSON file.
            path_dir (str): The directory where the file should be saved.
        """
        # Get all attributes that start with "UUID"
        all_atributes = {
            key: value
            for key, value in self.get_all_internal().items()
            if key.startswith("UUID")
        }
        # Save all attributes to a single JSON file
        try:
            with open(f"{path_dir}/.data/{name}.json", "w") as f:
                dump(all_atributes, f, indent=4)
        except FileNotFoundError:
            print(f"Directory {path_dir}/.data/ not found.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
