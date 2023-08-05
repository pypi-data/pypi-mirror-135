import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Text

from neuralspace.constants import TYPE
from neuralspace.datamodels import DatasetType


class DataConverter:
    LOOKUP_FILE = "lookup.json"
    REGEX_FILE = "regex.json"
    SYNONYM_FILE = "synonym.json"
    NLU_FILE = "nlu.json"

    @staticmethod
    def __training_data_converter(final_data) -> List[Dict[Text, Any]]:
        NotImplementedError("Training data converter is not implemented")
        pass

    def __regex_converter(self, final_data: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        NotImplementedError("Regex converter is not implemented")

    def __synonym_converter(self, final_data: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        NotImplementedError("synonym converter is not implemented")

    def __lookup_converter(self, final_data: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        NotImplementedError("lookup converter is not implemented")

    def convert(self, input_path: Path, output_path: Path, dataset_type: DatasetType):
        NotImplementedError("lookup converter is not implemented")

    def convert_multiple(
        self, input_path: List[Path], output_path: Path, dataset_type: DatasetType
    ):
        NotImplementedError("lookup converter is not implemented")

    @staticmethod
    def count(dataset):
        return len(dataset)

    @staticmethod
    def save_converted_data(
        output_directory: Path,
        lookup_data: Optional[List[Dict[Text, Any]]] = None,
        regex_data: Optional[List[Dict[Text, Any]]] = None,
        synonym_data: Optional[List[Dict[Text, Any]]] = None,
        nlu_data: Optional[List[Dict[Text, Any]]] = None,
    ):
        output_directory.mkdir(parents=True, exist_ok=True)

        if lookup_data is not None:
            with open(output_directory / DataConverter.LOOKUP_FILE, "w") as f:
                json.dump(lookup_data, f, indent=4)
        if regex_data is not None:
            with open(output_directory / DataConverter.REGEX_FILE, "w") as f:
                json.dump(regex_data, f, indent=4)
        if synonym_data is not None:
            with open(output_directory / DataConverter.SYNONYM_FILE, "w") as f:
                json.dump(synonym_data, f, indent=4)
        if nlu_data is not None:
            with open(output_directory / DataConverter.NLU_FILE, "w") as f:
                json.dump(nlu_data, f, indent=4)

    def set_data_type(self, dataset_type: DatasetType = "train"):
        for example in self.nlu_data:
            example[TYPE] = dataset_type
