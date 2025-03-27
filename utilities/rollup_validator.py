import json

# Reading json file and return into python readable data
with open("balance_sheet.json", "r") as f:
    data = json.load(f)

# array to push findings
discrepancy_report = []

# Recursive function to validate roll-up sums
# It takes a list of items 
# initally there is no parent
def validate_rollup(items, parent_name=None):
    # Loops through each item
    for item in items:
        name = item.get("name")
        value = float(item.get("value", 0.0))
        children = item.get("items", [])

        if children:
            # Recursively check children
            # the parent is known
            validate_rollup(children, parent_name=name)

            # Calculate the sum of children’s values
            child_sum = sum(float(child.get("value", 0.0)) for child in children)

            # Compare parent value to child sum with float tolerance by difference absolute value of a parent and child.
            if abs(child_sum - value) > 0.01:
                discrepancy_report.append(
                    f"[DISCREPANCY] '{name}' (Parent: '{parent_name}') — "
                    f"Expected: {value}, Sum of Children: {child_sum:.2f}, "
                    f"Difference: {value - child_sum:.2f}"
                )

# Loop through the top-level categories in the JSON
for section_name in ["assets", "liabilities", "equity"]:
    # get related section
    section = data.get(section_name, {})
    if "items" in section:
        validate_rollup(section["items"], parent_name=section_name.capitalize())

#  Save the results
report_text = "\n".join(discrepancy_report) or " No discrepancies found. All roll-up calculations are correct."

# write the result in a separate file
with open("rollup_discrepancy_report.txt", "w") as report_file:
    report_file.write(report_text)

print("Roll-up check complete. See 'rollup_discrepancy_report.txt' for results.")
