import argparse
from insightlog.lib import InsightLogAnalyzer


def main():
    parser = argparse.ArgumentParser(description="Analyze server log files (nginx, apache2, auth)")
    parser.add_argument('--service', required=True, choices=['nginx', 'apache2', 'auth'], help='Type of log to analyze')
    parser.add_argument('--logfile', required=True, help='Path to the log file')
    parser.add_argument('--filter', required=False, default=None, help='String to filter log lines')
    args = parser.parse_args()

    analyzer = InsightLogAnalyzer(args.service, filepath=args.logfile)
    if args.filter:
        analyzer.add_filter(args.filter)
    requests = analyzer.get_requests()
    for req in requests:
        print(req) 

if __name__ == '__main__':
    main() 
TODO: Add export to CSV
class InsightLogAnalyzer:
    def export_to_csv(self, path):
        """
        Export filtered results to a CSV file.

        :param path: string - Path where the CSV should be saved.
        """
        data = getattr(self, "filtered_requests", None) or self.get_requests()
        if not data:
            print(" No data to export.")
            return

        try:
            with open(path, mode='w', newline='', encoding='utf-8') as csvfile:
                if isinstance(data[0], dict):
                    # Write dictionaries directly
                    writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
                    writer.writeheader()
                    writer.writerows(data)
                else:
                    # Convert objects to dicts if needed
                    fieldnames = [attr for attr in dir(data[0]) if not attr.startswith(
                        '_') and not callable(getattr(data[0], attr))]
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    for item in data:
                        writer.writerow({f: getattr(item, f)
                                        for f in fieldnames})
            print(f" CSV export successful: {path}")
        except Exception as e:
            print(f" Failed to export CSV: {e}")
