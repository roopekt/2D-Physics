from pandas import read_excel
from dataclasses import dataclass
from itertools import count
import os.path as path

@dataclass
class ContactProperties:
    elasticity: float = 0.3
    rest_friction_coefficient: float = 0.3
    dynamic_friction_coefficient: float = 0.2

    @classmethod
    def from_string(cls, string):
        numbers = [float(e) for e in string.split(",")]
        assert len(numbers) == 3, f"Wrong number of numbers in cell. Expected 3, Actual {len(numbers)}"

        return cls(
            elasticity = numbers[0],
            rest_friction_coefficient = numbers[1],
            dynamic_friction_coefficient = numbers[2]
        )

class ContactPropertyTable:

    def __init__(self):
        self.materials = {}

        file_path = path.join(path.dirname(__file__), "contact_property_table.xlsx")
        table = read_excel(file_path, header=0, index_col=0)
        table.fillna("", inplace=True)
        
        for nameA, column in table.to_dict().items():
            for nameB, value in column.items():
                if value != "":
                    value = ContactProperties.from_string(value)
                    self.materials[(nameA, nameB)] = value
                    self.materials[(nameB, nameA)] = value

    def get_contact_properties(self, material_name_A, material_name_B):
        return self.materials[(material_name_A, material_name_B)]
