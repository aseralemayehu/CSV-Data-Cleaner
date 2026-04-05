import csv
import statistics
import argparse

class CSVCleaner:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self.read_csv()
        self.fieldnames = self.data[0].keys() if self.data else []
        self.duplicates_removed = 0
        self.missing_filled = 0
        self.smoothed_cols = []

    def read_csv(self):
        with open(self.file_path, newline='') as f:
            return list(csv.DictReader(f))

    def write_csv(self, output_path):
        with open(output_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writeheader()
            writer.writerows(self.data)
        print(f"[INFO] Cleaned CSV saved to {output_path}")

    def detect_column_types(self):
        self.numeric_cols = []
        self.text_cols = []
        for col in self.fieldnames:
            try:
                [float(row[col]) for row in self.data if row[col] != '']
                self.numeric_cols.append(col)
            except ValueError:
                self.text_cols.append(col)

    def remove_duplicates(self, subset=None):
        seen = set()
        unique_data = []
        for row in self.data:
            key = tuple(row[col] for col in subset) if subset else tuple(row.items())
            if key not in seen:
                seen.add(key)
                unique_data.append(row)
            else:
                self.duplicates_removed += 1
        self.data = unique_data

    def fill_missing(self, numeric_strategy='mean', text_strategy='Unknown'):
        for col in self.numeric_cols:
            values = [float(row[col]) for row in self.data if row[col] != '']
            if not values:
                continue
            fill_value = {
                'mean': statistics.mean(values),
                'median': statistics.median(values),
                'zero': 0
            }.get(numeric_strategy, numeric_strategy)
            for row in self.data:
                if row[col] == '':
                    row[col] = fill_value
                    self.missing_filled += 1

        for col in self.text_cols:
            values = [row[col] for row in self.data if row[col] != '']
            fill_value = max(set(values), key=values.count) if text_strategy=='mode' else text_strategy
            for row in self.data:
                if row[col] == '':
                    row[col] = fill_value
                    self.missing_filled += 1

    def smooth_numeric(self, window=3):
        for col in self.numeric_cols:
            nums = [float(row[col]) for row in self.data]
            smoothed = [sum(nums[max(0,i-window+1):i+1])/min(i+1, window) for i in range(len(nums))]
            for i, row in enumerate(self.data):
                row[col] = smoothed[i]
            self.smoothed_cols.append(col)

    def clean(self, remove_dupes=True, subset=None, fill_numeric='mean', fill_text='Unknown', smooth_window=None):
        self.detect_column_types()
        if remove_dupes:
            self.remove_duplicates(subset=subset)
        self.fill_missing(numeric_strategy=fill_numeric, text_strategy=fill_text)
        if smooth_window:
            self.smooth_numeric(window=smooth_window)
        self.report_summary()

    def report_summary(self):
        print("===== Cleaning Summary =====")
        print(f"Duplicates removed: {self.duplicates_removed}")
        print(f"Missing values filled: {self.missing_filled}")
        print(f"Numeric columns smoothed: {', '.join(self.smoothed_cols) if self.smoothed_cols else 'None'}")
        print("============================")


# CLI Interface

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CSV Data Cleaning Tool")
    parser.add_argument("input_file", help="Path to input CSV file")
    parser.add_argument("output_file", help="Path to save cleaned CSV")
    parser.add_argument("--no-duplicates", action="store_true", help="Do not remove duplicates")
    parser.add_argument("--subset", nargs='+', help="Columns to check for duplicates")
    parser.add_argument("--fill-numeric", default="mean", help="Numeric fill strategy: mean, median, zero, or custom value")
    parser.add_argument("--fill-text", default="Unknown", help="Text fill strategy: mode, Unknown, or custom value")
    parser.add_argument("--smooth", type=int, help="Apply numeric smoothing with specified window size")

    args = parser.parse_args()

    cleaner = CSVCleaner(args.input_file)
    cleaner.clean(
        remove_dupes=not args.no_duplicates,
        subset=args.subset,
        fill_numeric=args.fill_numeric,
        fill_text=args.fill_text,
        smooth_window=args.smooth
    )
    cleaner.write_csv(args.output_file)