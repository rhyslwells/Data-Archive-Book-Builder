import os

# Path to the content folder
content_folder = './content'

# Output summary file
summary_file = 'SUMMARY.md'

# Function to generate the summary
def generate_summary(content_folder, summary_file):
    # Initialize the summary content with a title
    summary_content = "# Summary\n\n"

    # Walk through the content folder to find .md files
    for root, dirs, files in os.walk(content_folder):
        for file in files:
            if file.endswith('.md') and file != 'README.md':  # Avoid including README.md itself
                file_name_without_ext = os.path.splitext(file)[0]  # Remove .md extension
                # Create the markdown link with the relative .md path, keeping spaces
                summary_content += f"* [{file_name_without_ext}](./content/{file_name_without_ext}.md)\n"

    # Write the summary content to the summary.md file
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(summary_content)

    print(f"Summary generated successfully in {summary_file}")

# Generate the summary
generate_summary(content_folder, summary_file)
