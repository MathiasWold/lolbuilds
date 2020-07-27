from utils import config, files


class Source:

    def __init__(self, name):
        """
        Template for source classes. 
        The source should implement the methods described below, with the correct return values.  
        """
        self.name = name

    def get_champions(self):
        """
        - Returns a list of champions in dictonary format
            - Returned dictionary format: 
                {
                    "name": str, 
                    "display_name": str, 
                    "id": str, 
                    "roles": list
                }
        """
        raise NotImplementedError

    def get_items(self, champion, role):
        """
        Parameters:
        - champion (dict): dict returned from get_champions
        - role (str): role to apply items to

        Returns:
        - Dictionary with items for this champion and role
            - Returned dictionary format: 
                {
                    "frequent": {
                        "full": list, 
                        "starters": list
                    }, 
                    "highest": {
                        "full": list, 
                        "starters": list
                    }
                }
        """
        raise NotImplementedError

    def get_skill_order(self, champion, role):
        """
        Parameters:
        - champion (dict): dict returned from get_champions
        - role (str): role to apply skill order to

        Returns:
        - Dictionary with skill order for this champion and role
            - Returned dictionary format: 
                {
                    skill_order = {
                        "frequent": list,
                        "highest": list
                    }
                }
            -List example (length 18): ["Q", "W", "E", ..., "R", "E", "E"]
        """
        raise NotImplementedError

    def get_version(self):
        """
        Returns:
        - Current version of the source in string format, e.g. "10.14" or "2020.10.20"
        """
        raise NotImplementedError

    def get_item_sets(self, champion):
        """ Gets item sets with items and skill order for every role for a champion """

        item_sets = []

        for role, role_rank in champion["roles"]:

            items = self.get_items(champion, role)
            skill_order = self.get_skill_order(champion, role)

            item_set = {
                "role": role,
                "rank": role_rank,
                "frequent": {
                    "full": items["frequent"]["full"],
                    "starters": items["frequent"]["starters"],
                    "skill_order": skill_order["frequent"]
                },
                "highest": {
                    "full": items["highest"]["full"],
                    "starters": items["highest"]["starters"],
                    "skill_order": skill_order["highest"]
                }
            }

            item_sets.append(item_set)

        return item_sets

    def import_item_sets(self):
        """ Imports all item sets for all champions and roles """

        # first remove old item sets
        self.delete_item_sets()

        champions = self.get_champions()
        version = self.get_version()

        config.save(self.name, version)

        for champion in champions:
            print(
                f"Adding {champion['display_name']}'s item sets from {self.name}...", end="\r")

            item_sets = self.get_item_sets(champion)

            for item_set in item_sets:
                files.save(champion, item_set, version, self.name)

            print(" "*80, end="\r")

    def delete_item_sets(self):
        """ Deletes all item sets for all champions and roles generated by import_item_sets """

        print(f"Deleting item sets from {self.name}")

        config.save(self.name, None)

        champions = self.get_champions()

        for champion in champions:
            files.delete(champion, self.name)