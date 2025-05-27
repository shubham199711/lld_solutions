import json
from dataclasses import dataclass

@dataclass
class OCRData:
    text: str
    bbox: list[int]

    def __repr__(self):
        return f"{self.text} -> {self.bbox}"

class OCRDataReader:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.ocr_data: list["OCRData"] = []

    def load_ocr_json(self):
        try:
            with open(self.file_path, 'r') as file:
                data = json.load(file)
                self.ocr_data = [OCRData(text=item['text'], bbox=item['bbox']) for item in data]
        except FileNotFoundError:
            print(f"Error: The file {self.file_path} was not found.")
        except json.JSONDecodeError:
            print(f"Error: The file {self.file_path} is not a valid JSON file.")

    def get_ocr_data(self) -> list[OCRData]:
        return self.ocr_data

class OCRDataController:
    def __init__(self, data: list[OCRData]):
        self.data = data
    
    def group_token_by_line(self, threshold: int) -> list[list[OCRData]]:
        lines: list[list[OCRData]] = []
        self.data.sort(key=lambda x: x.bbox[1])  # Sort by y-coordinate
        current_line: list[OCRData] = []
        for token in self.data:
            if not current_line or abs(token.bbox[1] - current_line[0].bbox[1]) <= threshold:
                current_line.append(token)
            else:
                lines.append(current_line)
                current_line = [token]
        if current_line:
            lines.append(current_line)
        return lines

def main():
    reader = OCRDataReader('./ocr_data.json')
    reader.load_ocr_json()
    ocr_data = reader.get_ocr_data()
    controller = OCRDataController(ocr_data)
    lines = controller.group_token_by_line(threshold=10)
    print(lines)

if __name__ == "__main__":
    main()