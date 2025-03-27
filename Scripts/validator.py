import json
import logging
import os
import sys

# Setup logging configuration
logging.basicConfig(
    filename="Outputs/Validatior.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()

# Function to read the JSON file and return parsed data
def load_json_file(file_path):
    try:
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            raise FileNotFoundError(f"The file '{file_path}' does not exist.")
        
        with open(file_path, "r") as f:
            data = json.load(f)
        logger.info(f"Successfully loaded JSON file: {file_path}")
        return data
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON file {file_path}: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error while reading {file_path}: {e}")
        raise

# Array to push findings
discrepancy_report = []

# Recursive function to validate roll-up sums
def validate_rollup(items, parent_name=None):
    for item in items:
        name = item.get("name")
        value = item.get("value", "0.0")
        
        try:
            value = float(value)
        except ValueError:
            logger.warning(f"Invalid value found for '{name}': {value}. Skipping this item.")
            continue

        children = item.get("items", [])
        
        if children:
            validate_rollup(children, parent_name=name)

            child_sum = sum(float(child.get("value", 0.0)) for child in children)
            if abs(child_sum - value) > 0.01:
                discrepancy_report.append(
                    f"[DISCREPANCY] '{name}' (Parent: '{parent_name}') — "
                    f"Expected: {value}, Sum of Children: {child_sum:.2f}, "
                    f"Difference: {value - child_sum:.2f}"
                )
                logger.warning(f"Discrepancy found for '{name}' (Parent: '{parent_name}')")

# Main function to run the validation
def main(json_file_path):
    try:
        # Load data from the provided JSON file path
        data = load_json_file(json_file_path)

        # Validate roll-ups for top-level categories: assets, liabilities, and equity
        for section_name in ["assets", "liabilities", "equity"]:
            section = data.get(section_name, {})
            if "items" in section:
                logger.info(f"Validating {section_name.capitalize()} section")
                validate_rollup(section["items"], parent_name=section_name.capitalize())
            else:
                logger.warning(f"Section '{section_name}' is missing 'items'")

        # Save the report
        report_text = "\n".join(discrepancy_report) or "No discrepancies found. All roll-up calculations are correct."
        with open("rollup_discrepancy_report.txt", "w") as report_file:
            report_file.write(report_text)
        logger.info("Roll-up validation completed successfully. Report saved as 'rollup_discrepancy_report.txt'.")
        
    except Exception as e:
        logger.error(f"Validation failed: {e}")
        sys.exit(1)  # Exit the program if an error occurs

# Allow flexibility in specifying file paths via command-line argument or default to a given file
if __name__ == "__main__":
    json_file_path = sys.argv[1] if len(sys.argv) > 1 else "data/financial_data.json"
    main(json_file_path)
